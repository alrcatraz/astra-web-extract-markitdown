"""Web Extract via MarkItDown — plugin registration.

Overrides the built-in web_extract tool to use ctx.dispatch_tool →
mcp_markitdown_convert_to_markdown, avoiding the need for Firecrawl/Tavily/Exa
API keys. Inherits the existing Hermes-managed markitdown-mcp server with
GLM vision model for OCR on images and scanned PDFs.

Audio and video extraction is planned but not yet implemented.
"""

import logging

from . import schemas, tools

logger = logging.getLogger(__name__)


def register(ctx):
    """Wire schemas to handler, override built-in web_extract."""

    # Inject ctx.dispatch_tool into the tools module so handlers can call
    # the Hermes-managed markitdown-mcp server without managing their own
    # subprocess or MCP protocol.
    tools.set_dispatcher(ctx.dispatch_tool)

    ctx.register_tool(
        name="web_extract",
        toolset="plugin_web_extract",
        schema=schemas.WEB_EXTRACT,
        handler=tools.web_extract,
        override=True,  # Replace the built-in
    )

    logger.info(
        "web-extract-markitdown: web_extract overridden — "
        "now uses ctx.dispatch_tool → mcp_markitdown_convert_to_markdown"
    )
