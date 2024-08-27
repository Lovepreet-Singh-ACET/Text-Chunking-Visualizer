import streamlit as st
from utils.file_handlers import extract_text_from_pdf, extract_text_from_file
from utils.model_names import OPEN_AI_MODEL_NAMES
from utils.chunking_strategies import (
    recursive_character_chunking,
    character_based_chunking,
    code_language_based_chunking,
    markdown_based_chunking,
    token_based_chunking,
    spacy_based_chunking,
    sentence_transformer_based_chunking
)

# Streamlit UI Components
st.title("Text Chunking Visualizer")

# Sidebar for Chunking Strategy Options
st.sidebar.title("Chunking Strategy Options")
strategy = st.sidebar.selectbox("Choose a Chunking Strategy", ["Recursive-Character", "Character-Based", "Code-Based", "Markdown-Based", "Token-Based(tiktoken)", "Spacy-Based", "Sentence-Transformer-Based"])

# Dynamic input options based on the chosen strategy
input_method = None
text = ""
uploaded_file = None
content_type = "text"

# Show relevant input options based on the chunking strategy
if strategy in ["Recursive-Character", "Character-Based", "Token-Based(tiktoken)", "Spacy-Based", "Sentence-Transformer-Based"]:
    input_method = st.sidebar.selectbox("Choose Input Method", ["Paste Text", "Upload PDF", "Upload Text File"])
elif strategy == "Markdown-Based":
    input_method = "Upload Markdown"  # Force PDF input for this strategy
elif strategy == "Code-Based":
    input_method = "Paste Text"

if input_method == "Paste Text":
    text = st.text_area("Enter the text to chunk", height=200)
elif input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
elif input_method == "Upload Text File":
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    if uploaded_file is not None:
        text = extract_text_from_file(uploaded_file)
elif input_method == "Upload Markdown":
    uploaded_file = st.file_uploader("Upload a Markdown file", type=["txt"])
    if uploaded_file is not None:
        text = extract_text_from_file(uploaded_file)

# Show extracted text preview only for file uploads
if text and input_method != "Paste Text":
    with st.expander("Preview Extracted Text"):
        st.write(text)

# Dynamic sidebar options based on chosen strategy
if strategy == "Recursive-Character":
    separator = st.sidebar.text_input(label="Separators", 
                                      value=r'"\n\n", "\n", " ", ""',
                                      help="The chunking is done based on the provided separators. Make sure to these seperated by ',' and strictly enclosed within \"\".") 
    chunk_size = st.sidebar.number_input("Chunk Size", min_value=1, max_value=10000, value=500)
    overlap_size = st.sidebar.number_input("Overlap Size", min_value=0, max_value=500, value=100)
elif strategy == "Character-Based":
    # separator = st.sidebar.text_input(label="Separators", value=r'"\n"')
    chunk_size = st.sidebar.number_input("Chunk Size", min_value=1, max_value=10000, value=500)
    overlap_size = st.sidebar.number_input("Overlap Size", min_value=0, max_value=500, value=100)
elif strategy == "Code-Based":
    content_type = "code"
    selected_language = st.sidebar.selectbox("Choose a language", ["CPP", "GO", "JAVA", "KOTLIN", "JS", "TS", "PHP", "PROTO", "PYTHON", "RST", "RUBY", "RUST", "SCALA", "SWIFT", "MARKDOWN", "LATEX", "HTML", "SOL", "CSHARP", "COBOL", "C", "LUA", "PERL", "HASKELL", "ELIXIR"])
    chunk_size = st.sidebar.number_input("Chunk Size", min_value=1, max_value=10000, value=500)
    overlap_size = st.sidebar.number_input("Overlap Size", min_value=0, max_value=500, value=100)
elif strategy == "Markdown-Based":
    pass
elif strategy == "Token-Based(tiktoken)":
    selected_model = st.sidebar.selectbox("Choose a model", OPEN_AI_MODEL_NAMES)
    chunk_size = st.sidebar.number_input("Chunk Size", min_value=1, max_value=10000, value=500, help="Here Chunk size refers to the number of tokens.")
    overlap_size = st.sidebar.number_input("Overlap Size", min_value=0, max_value=500, value=100, help="This signifies the number of tokens to overlap")
elif strategy == "Spacy-Based":
    chunk_size = st.sidebar.number_input("Chunk Size", min_value=1, max_value=10000, value=500)
    overlap_size = st.sidebar.number_input("Overlap Size", min_value=0, max_value=500, value=100)
elif strategy == "Sentence-Transformer-Based":
    pass

# Process the input text if any is provided
if st.button("Chunk Text"):
    if text:
        if strategy == "Recursive-Character":
            chunks = recursive_character_chunking(
                                text=text,
                                separator=separator, 
                                chunk_size=chunk_size,
                                overlap_size=overlap_size
                                )
        elif strategy == "Character-Based":
            chunks = character_based_chunking(
                                text=text,
                                separator="\n",
                                chunk_size=chunk_size, 
                                overlap_size=overlap_size
                                )
        elif strategy == "Code-Based":
            chunks, code_language = code_language_based_chunking(
                                text=text,
                                language=selected_language,
                                chunk_size=chunk_size,
                                overlap_size=overlap_size
                                )
        elif strategy == "Markdown-Based":
            chunks = markdown_based_chunking(
                                text=text
                                )
        elif strategy == "Token-Based(tiktoken)":
            chunks = token_based_chunking(
                                text=text,
                                model_name=selected_model,
                                chunk_size=chunk_size,
                                overlap_size=overlap_size
                                )
        elif strategy == "Spacy-Based":
            chunks =  spacy_based_chunking(
                                text=text,
                                chunk_size=chunk_size,
                                overlap_size=overlap_size
                                )   
        elif strategy == "Sentence-Transformer-Based":
            chunks = sentence_transformer_based_chunking(
                                text=text,
                                model_name=model_name,
                                tokens_per_chunk=token_per_chunk,
                                overlap_size=overlap_size 
                                )

        st.write("### Chunked Text")
        for i, chunk in enumerate(chunks):
            # Using expander to make chunks collapsible
            with st.expander(f"Chunk {i+1} (Length: {len(chunk)} chars)"):
                print(content_type)
                if content_type == "code":
                    print(code_language)
                    # Display chunk using st.code to preserve formatting for code
                    st.code(chunk, language=code_language)
                else:
                    # Different background colors for alternating chunks
                    bg_color = "#F5F5DC" if i % 2 == 0 else "#D3D3D3"  # Light yellow and light gray
                    st.markdown(f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 5px; color: black;'>{chunk}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please provide some text through your chosen input method.")
