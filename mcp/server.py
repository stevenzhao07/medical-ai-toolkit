#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lgd-mcp — a zero-dependency MCP server for this routing table.

Exposes the module matrix to any MCP-capable client (Claude Code, Cursor, and
others) over stdio, using only the Python standard library. No third-party
packages, no network: consistent with the rest of this matrix.

Transport: newline-delimited JSON-RPC 2.0 on stdin/stdout (the MCP stdio
transport). Diagnostics go to stderr so they never corrupt the stream.

Tools
  list_modules  — the 21 modules with entry points, triggers and licence
  route         — rank modules against an intent string, using the same
                  keyword/intent matching the matrix's router.py uses
  module_info   — the clone-and-run command for one module

Run:
    python mcp/server.py            # speaks MCP on stdio
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKELETON = os.path.join(ROOT, 'skeleton.json')
SERVER_INFO = {'name': 'lgd-mcp', 'version': '1.0.0'}
DEFAULT_PROTOCOL = '2024-11-05'

TOOLS = [
    {
        'name': 'list_modules',
        'description': ('List every module in the matrix: id, title, entry script, '
                        'triggers and licence. Use this to discover what the toolkit '
                        'covers before routing an intent.'),
        'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False},
    },
    {
        'name': 'route',
        'description': ('Given a free-text intent, return the modules whose triggers '
                        'match, ranked by score. Matching is keyword/intent based and '
                        'deterministic — no model is involved.'),
        'inputSchema': {
            'type': 'object',
            'properties': {'intent': {'type': 'string', 'description': 'What the user wants to do'}},
            'required': ['intent'],
            'additionalProperties': False,
        },
    },
    {
        'name': 'module_info',
        'description': 'Return the entry script and the clone-and-run command for one module id.',
        'inputSchema': {
            'type': 'object',
            'properties': {'module_id': {'type': 'string', 'description': 'Module id from list_modules'}},
            'required': ['module_id'],
            'additionalProperties': False,
        },
    },
]


def load_modules() -> list:
    with open(SKELETON, encoding='utf-8') as fh:
        data = json.load(fh)
    mods = data.get('modules')
    if isinstance(mods, dict):
        return [dict(v, id=k) if isinstance(v, dict) else {'id': k} for k, v in mods.items()]
    if isinstance(mods, list):
        return mods
    routing = data.get('routing') or {}
    return [dict(v, id=k) if isinstance(v, dict) else {'id': k} for k, v in routing.items()]


def _triggers(mod: dict):
    """skeleton.json 的模块项可能把 keywords/intents 放在顶层，也可能嵌在 triggers 下。"""
    t = mod.get('triggers')
    if isinstance(t, dict):
        return (t.get('keywords') or []), (t.get('intents') or [])
    return (mod.get('keywords') or []), (mod.get('intents') or [])


def score(mod: dict, intent: str) -> int:
    text = intent.lower()
    kws, intents = _triggers(mod)
    hits = 0
    for k in kws:
        if str(k).lower() in text:
            hits += 3
    for i in intents:
        if str(i).lower() in text:
            hits += 5
    for kw in (str(mod.get('id', '')), str(mod.get('title', ''))):
        for tok in kw.lower().replace('-', ' ').split():
            if len(tok) > 3 and tok in text:
                hits += 1
    return hits


def call_tool(name: str, args: dict) -> str:
    mods = load_modules()
    if name == 'list_modules':
        rows = [{'id': m.get('id'), 'title': m.get('title'), 'entry': m.get('entry'),
                 'licence': m.get('license'), 'triggers': m.get('triggers')} for m in mods]
        return json.dumps({'count': len(rows), 'modules': rows}, ensure_ascii=False, indent=2)
    if name == 'route':
        intent = str(args.get('intent', ''))
        ranked = sorted(((score(m, intent), m) for m in mods), key=lambda x: -x[0])
        hits = [{'id': m.get('id'), 'title': m.get('title'), 'entry': m.get('entry'),
                 'score': s} for s, m in ranked if s > 0][:8]
        return json.dumps({'intent': intent, 'matches': hits,
                           'note': ('No match — the matrix covers medical-device lifecycle and '
                                    'medical-AI governance. Try naming a stage, e.g. '
                                    '"sterilisation validation" or "UDI".' if not hits else '')},
                          ensure_ascii=False, indent=2)
    if name == 'module_info':
        mid = str(args.get('module_id', ''))
        for m in mods:
            if m.get('id') == mid:
                entry = m.get('entry') or '(portal)'
                return json.dumps({
                    'id': mid, 'title': m.get('title'), 'licence': m.get('license'),
                    'upstream': m.get('upstream'),
                    'commands': ['git clone https://github.com/stevenzhao07/%s.git' % mid,
                                 'cd %s' % mid,
                                 'python %s --demo' % entry,
                                 'python %s --help' % entry],
                    'note': 'Zero third-party dependencies; standard library only.',
                }, ensure_ascii=False, indent=2)
        return json.dumps({'error': 'unknown module_id: %s' % mid,
                           'hint': 'call list_modules first'}, ensure_ascii=False)
    raise ValueError('unknown tool: %s' % name)


def handle(msg: dict):
    mid = msg.get('id')
    method = msg.get('method')
    params = msg.get('params') or {}

    if method == 'initialize':
        pv = params.get('protocolVersion') or DEFAULT_PROTOCOL
        return {'jsonrpc': '2.0', 'id': mid, 'result': {
            'protocolVersion': pv, 'capabilities': {'tools': {}}, 'serverInfo': SERVER_INFO}}
    if method in ('notifications/initialized', 'initialized'):
        return None
    if method == 'ping':
        return {'jsonrpc': '2.0', 'id': mid, 'result': {}}
    if method == 'tools/list':
        return {'jsonrpc': '2.0', 'id': mid, 'result': {'tools': TOOLS}}
    if method == 'tools/call':
        name = params.get('name')
        args = params.get('arguments') or {}
        try:
            text = call_tool(name, args)
            return {'jsonrpc': '2.0', 'id': mid,
                    'result': {'content': [{'type': 'text', 'text': text}], 'isError': False}}
        except Exception as exc:
            return {'jsonrpc': '2.0', 'id': mid,
                    'result': {'content': [{'type': 'text', 'text': 'error: %r' % exc}], 'isError': True}}
    return {'jsonrpc': '2.0', 'id': mid,
            'error': {'code': -32601, 'message': 'method not found: %s' % method}}


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            print('bad json: %r' % exc, file=sys.stderr)
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + '\n')
            sys.stdout.flush()
    return 0


if __name__ == '__main__':
    sys.exit(main())
