---
name: web-extract-markitdown
description: >-
  Plugin that overrides Hermes's built-in web_extract tool to use
  ctx.dispatch_tool → mcp_markitdown_convert_to_markdown, replacing
  Firecrawl/Tavily/Exa API calls with a local Microsoft MarkItDown backend.
  Inherits GLM vision model for OCR via the existing markitdown-mcp config.
category: devops
version: 1.0.0
---

# Web Extract via MarkItDown

## What it does

Replaces the built-in `web_extract` tool so Hermes converts URLs to markdown
using the **Microsoft MarkItDown library** (via the already-running
`markitdown-mcp` MCP server) instead of requiring a paid API key for
Firecrawl, Tavily, or Exa.

## How it works

```
User asks "extract this page"
  → LLM calls web_extract(urls=[...])
  → Plugin handler (override=True)
    → ctx.dispatch_tool("mcp_markitdown_convert_to_markdown", {"uri": url})
    → markitdown-mcp (managed by Hermes, already running)
      → GLM-4.6V-Flash OCR for images/scanned PDFs
    → Returns markdown text
  → Returns results to LLM
```

## Architecture

```
~/.hermes/plugins/web-extract-markitdown/    (or symlinked from repo)
├── plugin.yaml      # Manifest
├── __init__.py      # register() — wires override
├── schemas.py       # web_extract tool schema
└── tools.py         # Handler that dispatches to markitdown-mcp
```

## Dependencies

- **markitdown-mcp** — configured in `~/.hermes/config.yaml` under `mcp_servers.markitdown`
- **ZAI_API_KEY** — for GLM vision model OCR (already configured)
- The plugin itself has **zero Python dependencies** — it uses `ctx.dispatch_tool`
  which is part of the Hermes plugin SDK.

## Limitations

| Limitation | Status |
|:-----------|:-------|
| Audio extraction | ❌ Planned (STT via whisper) |
| Video extraction | ❌ Planned |
| `char_limit` parameter | ❌ Ignored (full content returned) |
| URL-only (no raw HTML upload) | ⚠️ Use `file:` URIs for local files |

## Maintenance

If the markitdown-mcp MCP server is not running, `dispatch_tool` will raise an
error. Check with:

```bash
hermes mcp status    # Should show markitdown as enabled
```

The plugin registers with `override=True` — to disable the override and
restore the built-in web_extract:

```bash
hermes plugins disable web-extract-markitdown
```
