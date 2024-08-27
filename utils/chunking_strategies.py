from langchain_text_splitters import (
    RecursiveCharacterTextSplitter, 
    CharacterTextSplitter, 
    Language,
    MarkdownHeaderTextSplitter,
    TokenTextSplitter,
    SpacyTextSplitter,
    SentenceTransformersTokenTextSplitter
)

def recursive_character_chunking(text, separator, chunk_size, overlap_size):
    print(f'List of Seprators choosen in RCC: {list(map(eval, separator.split(",")))}')
    splitter = RecursiveCharacterTextSplitter(
                    separators= list(map(eval, separator.split(","))),
                    chunk_size=chunk_size, 
                    chunk_overlap=overlap_size
                )
    return splitter.split_text(text)

def character_based_chunking(text, separator, chunk_size, overlap_size):
    splitter = CharacterTextSplitter(
                    # separator=separator.replace("\\n", "\n"),
                    separator=separator,
                    chunk_size=chunk_size,
                    chunk_overlap=overlap_size,
                    is_separator_regex=False,
                )
    return splitter.split_text(text)

def code_language_based_chunking(text, language, chunk_size, overlap_size):
    # print(getattr(Language, language))
    splitter = RecursiveCharacterTextSplitter.from_language(
                    language=getattr(Language, language), 
                    chunk_size=chunk_size, 
                    chunk_overlap=overlap_size
    )
    return splitter.split_text(text), language.lower()

def markdown_based_chunking(text, strip_headers):
    # strip_headers True/False
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=strip_headers)
    return splitter.split_text(text)

def token_based_chunking(text, chunk_size, overlap_size, model_name):
    splitter = TokenTextSplitter(model_name=model_name,
                                    chunk_size=chunk_size,
                                    chunk_overlap=overlap_size)

    return splitter.split_text(text)

def spacy_based_chunking(text, chunk_size, overlap_size):
    splitter = SpacyTextSplitter(chunk_size=chunk_size,
                                    chunk_overlap=overlap_size)

    return splitter.split_text(text)

def sentence_transformer_based_chunking(text, model_name, tokens_per_chunk, overlap_size):
    splitter = SentenceTransformersTokenTextSplitter(
                                    model_name=f"sentence-transformers/{model_name}",
                                    tokens_per_chunk=tokens_per_chunk,
                                    chunk_overlap=overlap_size)
    return splitter.split_text(text)