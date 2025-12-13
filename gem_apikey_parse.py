import google.generativeai as genai
import json
from os import environ

# 1. Configure with your API key
genai.configure(api_key=environ["WEB_SCRAPE_PARSE_GEMKEY"])

# 2. Create the model with a system prompt
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
        "You are a data extraction engine that receives raw, noisy webpage text (e-commerce or content-heavy) containing navigation, promotions, reviews, and duplicated sections; your task is to discard all UI, branding, accessibility, and marketing noise and output only high-signal structured data: identify the core item (canonical product name, brand, generic item type, primary use, explicit secondary uses only if stated), pricing and purchase metadata (current price, list price, discount, currency, delivery/return policies that affect the buyer), available variants (sizes, colors, options as lists only), category taxonomy (full hierarchy from broad to specific plus any ranking/bestseller metadata), review metadata (overall rating, rating count, normalized sentiment themes as positive/mixed/negative without quoting reviews), package contents, and finally infer high-level user interest signals strictly from evidence (activity or sport, price sensitivity tier, skill level if implied, brand flexibility, purchase intent); remove adjectives, slogans, repeated phrases, comparisons, bank names, keyboard shortcuts, footers, social links, and unrelated product lists; do not summarize the page, do not speculate, do not use conversational language, and structure the output into clear labeled sections suitable for direct conversion to JSON. You have to send the extracted metadata, not the script to do so. Do not output anything other than the JSON."
    )
)

# 3. User prompt
with open("sections_site.txt") as f:
    user_prompt = f.read()

# 4. Generate
responseModel = model.generate_content(user_prompt)
response = responseModel.text

# Parse json entry to JSON
start = response.find("{")
end = response.rfind("}")

if start == -1 or end == -1:
    raise ValueError("No JSON object found in response")

json_str = response[start:end + 1]
data = json.loads(json_str)

with open("sections_site_gemParse.json", "w") as f:
    json.dump(data, f, indent=2)
