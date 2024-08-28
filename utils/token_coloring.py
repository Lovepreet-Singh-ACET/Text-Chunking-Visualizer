import tiktoken
import random

# Function to color tokens using Tiktoken
def color_tokens_with_tiktoken(text, model_name):
    encoder = tiktoken.encoding_for_model(model_name=model_name)
    tokens = encoder.encode(text)  # Tokenize text using tiktoken
    decoded_tokens = encoder.decode_tokens_bytes(tokens)  # Decode tokens to their string representation

    colors = ['#FF6666', '#FFCC66', '#99FF66', '#66FFCC', '#66CCFF', '#CC99FF']
    colored_tokens = []
    for token in decoded_tokens:
        color = random.choice(colors)
        colored_tokens.append(f"<span style='color: {color};'>{token.decode()}</span>")
    
    return ' '.join(colored_tokens)

# Function to color tokens using Sentence-Transformer tokenizer
def color_tokens_with_sentence_transformer_tokenizer(text, model_name):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    colors = ['#FF6666', '#FFCC66', '#99FF66', '#66FFCC', '#66CCFF', '#CC99FF']

    colored_tokens = []
    for token in tokens:
        color = random.choice(colors)
        colored_tokens.append(f"<span style='color: {color};'>{token}</span>")
    
    return ' '.join(colored_tokens)