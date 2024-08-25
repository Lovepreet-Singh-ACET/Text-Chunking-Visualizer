from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter

def recursive_character_chunking(text, chunk_size, overlap_size):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap_size)
    return splitter.split_text(text)

def token_based_chunking(text, max_tokens):
    splitter = TokenTextSplitter()
    return splitter.split_text(text)

