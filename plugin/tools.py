"""Tool handlers — dispatch to the Hermes-managed markitdown-mcp server."""

import json
import logging

logger = logging.getLogger(__name__)

# Audio/video extensions — not yet supported
_MEDIA_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma",
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm",
}

# mcp_markitdown_convert_to_markdown accepts: http:, https:, file:, data: URIs
# Dispatch function is injected by __init__.py at registration time
_dispatch = None


def set_dispatcher(fn):
    """Inject ctx.dispatch_tool at registration time."""
    global _dispatch
    _dispatch = fn


def _has_media_ext(uri: str) -> bool:
    """Check if a URI has an audio/video file extension."""
    path = uri.split("?")[0].split("#")[0].lower()
    for ext in _MEDIA_EXTENSIONS:
        if path.endswith(ext):
            return True
    return False


def web_extract(args: dict, **kwargs) -> str:
    """Extract URLs via ctx.dispatch_tool → markitdown-mcp → convert_to_markdown."""
    urls = args.get("urls", [])
    if not urls:
        return json.dumps({"error": "No URLs provided", "results": []})

    results = []
    for url in urls:
        try:
            if _has_media_ext(url):
                results.append({
                    "url": url,
                    "content": None,
                    "error": (
                        "Audio/video extraction is not yet supported. "
                        "Planned for future implementation via STT/ASR."
                    ),
                })
                continue

            raw = _dispatch("mcp_markitdown_convert_to_markdown", {"uri": url})
            if raw is None:
                results.append({
                    "url": url,
                    "error": "markitdown-mcp returned no result",
                })
                continue

            # dispatch_tool returns a string — it's the markdown content
            results.append({
                "url": url,
                "content": raw,
            })

        except Exception as exc:
            logger.warning("web_extract failed for %s: %s", url, exc)
            results.append({
                "url": url,
                "error": str(exc),
            })

    return json.dumps({"results": results})
