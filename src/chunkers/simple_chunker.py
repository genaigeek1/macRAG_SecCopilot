
def chunk_text(text: str, max_tokens: int = 500) -> list:
    """Simple chunking of text into smaller pieces."""
    import textwrap
    return textwrap.wrap(text, width=max_tokens)
