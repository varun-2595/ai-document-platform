import re


def clean_text(text: str) -> str:
    # Fix broken words across newlines
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)

    # Merge split words caused by line breaks
    text = re.sub(r'(\w)\n(\w)', r'\1 \2', text)

    # Replace multiple newlines with single space
    text = re.sub(r'\n+', ' ', text)

    # Remove excessive spaces
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text