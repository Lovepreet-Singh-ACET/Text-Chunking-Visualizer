import streamlit as st
from utils.file_handlers import extract_text_from_pdf, extract_text_from_file
from utils.chunking_strategies import (
    recursive_character_chunking,
    token_based_chunking
)

# Streamlit UI Components
st.title("Text Chunking Visualizer")

# Sidebar for Input Options
st.sidebar.title("Input Options")
input_method = st.sidebar.selectbox("Choose Input Method", ["Paste Text", "Upload PDF", "Upload Text File"])

# Input text based on the selected method
text = ""
uploaded_file = None

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

# Show extracted text preview only for file uploads
if text and input_method != "Paste Text":
    with st.expander("Preview Extracted Text"):
        st.write(text)

# Sidebar for Chunking Strategy Options
st.sidebar.title("Chunking Strategy Options")
strategy = st.sidebar.selectbox("Choose a Chunking Strategy", ["Recursive Character", "Token-Based"])

# Dynamic sidebar options based on chosen strategy
if strategy == "Recursive Character":
    chunk_size = st.sidebar.number_input("Chunk Size", min_value=1, max_value=2000, value=500)
    overlap_size = st.sidebar.number_input("Overlap Size", min_value=0, max_value=500, value=100)
elif strategy == "Token-Based":
    max_tokens = st.sidebar.number_input("Max Tokens", min_value=1, max_value=1000, value=100)

# Process the input text if any is provided
if st.button("Chunk Text"):
    if text:
        if strategy == "Recursive Character":
            chunks = recursive_character_chunking(text, chunk_size, overlap_size)
        elif strategy == "Token-Based":
            chunks = token_based_chunking(text, max_tokens)

        st.write("### Chunked Text")
        for i, chunk in enumerate(chunks):
            # Using expander to make chunks collapsible
            with st.expander(f"Chunk {i+1} (Length: {len(chunk)} chars)"):
                # Different background colors for alternating chunks
                bg_color = "#F5F5DC" if i % 2 == 0 else "#D3D3D3"  # Light yellow and light gray
                st.markdown(f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 5px; color: black;'>{chunk}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please provide some text through your chosen input method.")
