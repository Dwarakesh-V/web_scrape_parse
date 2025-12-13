import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

# Load model and tokenizer from local directory
model_path = "./Llama-3.2-3B-Instruct"
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=torch.bfloat16,
    device_map="auto",
)
print("Model loaded successfully!\n")

# System prompt
system_prompt = """
You are a data extraction engine that receives raw, noisy webpage text (e-commerce or content-heavy) containing navigation, promotions, reviews, and duplicated sections; your task is to discard all UI, branding, accessibility, and marketing noise and output only high-signal structured data: identify the core item (canonical product name, brand, generic item type, primary use, explicit secondary uses only if stated), pricing and purchase metadata (current price, list price, discount, currency, delivery/return policies that affect the buyer), available variants (sizes, colors, options as lists only), category taxonomy (full hierarchy from broad to specific plus any ranking/bestseller metadata), review metadata (overall rating, rating count, normalized sentiment themes as positive/mixed/negative without quoting reviews), package contents, and finally infer high-level user interest signals strictly from evidence (activity or sport, price sensitivity tier, skill level if implied, brand flexibility, purchase intent); remove adjectives, slogans, repeated phrases, comparisons, bank names, keyboard shortcuts, footers, social links, and unrelated product lists; do not summarize the page, do not speculate, do not use conversational language, and structure the output into clear labeled sections suitable for direct conversion to JSON. You have to send the extracted metadata, not the script to do so. Do not output anything other than the JSON.
"""

# Conversation history
messages = [
    {"role": "system", "content": system_prompt}
]

def generate_response(messages):
    """Generate a response from the model"""
    # Apply chat template
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode only the new tokens
    response = tokenizer.decode(
        outputs[0][inputs['input_ids'].shape[1]:], 
        skip_special_tokens=True
    )
    
    return response


# Get user input
with open("sections_site.txt","r") as f:
    site_data = f.read()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": site_data}
]

# Generate response
try:
    response = generate_response(messages)
except Exception as e:
    print(f"Unable to generate response from local model because of error {e}")

# Add assistant response to history
# messages.append({"role": "assistant", "content": response})

# Parse json entry to JSON
start = response.find("{")
end = response.rfind("}")

if start == -1 or end == -1:
    raise ValueError("No JSON object found in response")

json_str = response[start:end + 1]
data = json.loads(json_str)

with open("sections_site.json", "w") as f:
    json.dump(data, f, indent=2)
