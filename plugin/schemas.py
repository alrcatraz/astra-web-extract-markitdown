"""Tool schemas — what the LLM sees for web_extract."""

WEB_EXTRACT = {
    "name": "web_extract",
    "description": (
        "Extract the main content of one or more web pages and return it as clean markdown. "
        "Uses the Microsoft MarkItDown library for conversion — supports HTML pages, PDFs, "
        "Word/Excel/PowerPoint documents, images (OCR via GLM vision model), and scanned PDFs. "
        "Audio and video files are not yet supported."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of URLs to extract content from.",
            },
            "char_limit": {
                "type": "integer",
                "description": "Optional maximum characters per page. Not yet implemented — "
                               "full content is returned.",
            },
        },
        "required": ["urls"],
    },
}
