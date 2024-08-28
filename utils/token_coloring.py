import tiktoken
import random

# Function to color tokens using Tiktoken
def color_tokens_with_tiktoken(text, model_name):
    encoder = tiktoken.encoding_for_model(model_name=model_name)
    tokens = encoder.encode(text)  # Tokenize text using tiktoken
    decoded_tokens = encoder.decode_tokens_bytes(tokens)  # Decode tokens to their string representation

    # colors = ['#FF6666', '#FFCC66', '#99FF66', '#66FFCC', '#66CCFF', '#CC99FF']
    colors = ['#6B40D84D', '#68DE7A66', '#F4AC3666', '#EF414666', '#27B5EA66']
    colored_tokens = []
    for idx, token in enumerate(decoded_tokens):
        color = colors[idx%5]
        colored_tokens.append(f"<span style='background-color: {color};color: #D9D9E3'>{token.decode()}</span>")
    
    return ' '.join(colored_tokens)

# Function to color tokens using Sentence-Transformer tokenizer
def color_tokens_with_sentence_transformer_tokenizer(text, model_name):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    # colors = ['#FF6666', '#FFCC66', '#99FF66', '#66FFCC', '#66CCFF', '#CC99FF']
    colors = ['#6B40D84D', '#68DE7A66', '#F4AC3666', '#EF414666', '#27B5EA66']
    colored_tokens = []
    for idx, token in enumerate(tokens):
        color = colors[idx%5]
        colored_tokens.append(f"<span style='background-color: {color};color: #D9D9E3'>{token}</span>")
    
    return ' '.join(colored_tokens)