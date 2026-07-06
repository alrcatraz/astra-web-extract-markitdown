# astra-web-extract-markitdown

A [Hermes Agent](https://hermes-agent.nousresearch.com) plugin that replaces
the built-in `web_extract` tool with a local backend powered by
[Microsoft MarkItDown](https://github.com/microsoft/markitdown).

<div align="center">

[![License](https://badgen.net/github/license/alrcatraz/astra-web-extract-markitdown)](LICENSE)
[![GitHub stars](https://badgen.net/github/stars/alrcatraz/astra-web-extract-markitdown)](https://github.com/alrcatraz/astra-web-extract-markitdown)
[![GitHub last commit](https://badgen.net/github/last-commit/alrcatraz/astra-web-extract-markitdown)](https://github.com/alrcatraz/astra-web-extract-markitdown/commits)
[![Sponsor](https://img.shields.io/github/sponsors/alrcatraz?label=Sponsor&logo=github&color=ea4aaa&logoColor=white)](https://github.com/sponsors/alrcatraz)

</div>

## Why

The built-in `web_extract` requires an API key for Firecrawl, Tavily, or Exa.
This plugin redirects extraction through the already-configured
`markitdown-mcp` MCP server — **no extra API keys, no external services**.

It also inherits the GLM-4.6V-Flash vision model for **OCR on images and
scanned PDFs**, configured via the existing `markitdown-mcp` setup.

## Installation

```bash
# Ensure markitdown-mcp is configured in ~/.hermes/config.yaml:
#   mcp_servers:
#     markitdown:
#       command: markitdown-mcp
#       enabled: true

# Enable the plugin
hermes plugins enable web-extract-markitdown

# Start a new session
hermes chat
```

## How it works

```
web_extract(urls=[...])
  → ctx.dispatch_tool("mcp_markitdown_convert_to_markdown", {"uri": url})
  → markitdown-mcp → MarkItDown → Markdown
  → GLM-4.6V-Flash OCR (for images / scanned PDFs)
```

## Architecture

```
plugin/
├── plugin.yaml      # Manifest
├── __init__.py      # register() — override=True on web_extract
├── schemas.py       # Tool schema (matching built-in interface)
└── tools.py         # Handler: dispatch to markitdown-mcp via ctx
```

## Status

| Feature | Status |
|:--------|:-------|
| HTML → Markdown | ✅ |
| PDF → Markdown | ✅ (native MarkItDown) |
| Image OCR | ✅ (via GLM-4.6V-Flash) |
| Scanned PDF OCR | ✅ |
| Audio → Text | ❌ Planned |
| Video → Text | ❌ Planned |
| `char_limit` parameter | ❌ Ignored (returns full content) |

## License

MIT
