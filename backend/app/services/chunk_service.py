def chunk_text(text: str, chunk_size: int = 500) -> list:
    """
    Split the input text into smaller chunks of specified size.
    
    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk. Default is 500 characters.
        
    Returns:
        list: A list of text chunks.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]