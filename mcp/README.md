# lgd-mcp — a zero-dependency MCP server for this matrix

Exposes the module matrix to any MCP-capable client (Claude Code, Cursor, and others) so an agent can discover and route the toolkit without being handed a list.

Standard library only — no `pip install`, no network. That is the same constraint the rest of the matrix holds itself to, and the reason the server is written against the MCP stdio transport by hand rather than pulling in an SDK.

## Tools

| Tool | What it returns |
|---|---|
| `list_modules` | Every module: id, title, entry script, licence, triggers |
| `route` | Given a free-text intent, the modules whose triggers match, ranked by score. Deterministic keyword/intent matching — no model is involved |
| `module_info` | The exact clone-and-run commands for one module id |

## Run

```bash
python mcp/server.py            # speaks MCP over stdio (newline-delimited JSON-RPC 2.0)
```

Client configuration (Claude Code / Cursor style, `mcpServers` entry):

```json
{
  "mcpServers": {
    "lgd-matrix": {
      "command": "python",
      "args": ["<path-to-clone>/mcp/server.py"]
    }
  }
}
```

It reads `skeleton.json` from the repository root, so clone the repository rather than copying this folder alone.

## Try it without a client

MCP is newline-delimited JSON-RPC 2.0 on stdin/stdout, so a pipe is enough:

```bash
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"route","arguments":{"intent":"sterilisation validation"}}}' \
 | python mcp/server.py
```

## Scope

This server exposes **metadata and routing only**. It does not execute module code, does not touch the network, and returns no regulatory or clinical conclusions. Diagnostics go to stderr so they cannot corrupt the protocol stream.

---

## 中文

把模块矩阵暴露给任意支持 MCP 的客户端（Claude Code、Cursor 等），让 agent 无需被告知清单即可发现并路由本工具链。

**仅标准库** —— 不需要 `pip install`、不需要联网。这与矩阵其余部分遵循同一条约束，也是本 server 手写 MCP stdio 传输、而非引入 SDK 的原因。

**三个工具**：`list_modules`（全部模块的 id/标题/入口/许可/触发词）、`route`（给定意图 → 按触发词评分排序命中模块；纯确定性匹配，无模型参与）、`module_info`（某个模块的 clone-and-run 命令）。

**运行**：`python mcp/server.py`（在 stdin/stdout 上讲 MCP，换行分隔的 JSON-RPC 2.0）。客户端配置见英文段的 `mcpServers` 示例；它读取仓库根的 `skeleton.json`，因此请克隆整个仓库而不是只复制本目录。

**边界**：本 server **只暴露元数据与路由**。它不执行模块代码、不访问网络、不给出法规或临床结论。诊断信息走 stderr，以免污染协议流。
