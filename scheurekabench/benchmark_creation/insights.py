import openai
import anthropic
import fitz  # PyMuPDF
import os
import re   
import argparse 
import json
import dotenv

from prompts.insight_extractor import insight_extractor_prompt

# Load environment variables from .env file
dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = {
    "claude-3-5-haiku-latest": 8192,
    "claude-opus-4-20250514": 16384,
    "claude-sonnet-4-20250514": 16384,
}

def clean_text(text):
    text = re.sub(r'^.*?(?:(?:, [A-Z][a-z]+){3,}).*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'(bioRxiv|Springer|Elsevier|doi:|arXiv|All rights reserved|et\xa0al.).*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def extract_text_from_pdf_cleaned(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = []

    for page in doc:
        blocks = page.get_text("blocks")
        page_text = []

        if page.number >= 20:
            break

        if blocks[0][4].startswith("Article\nMethods\n"):
            break

        breaking_content_found = False
        for block in blocks:
            if block[4].lower().startswith("online content") or block[4].lower().startswith("references"):
                breaking_content_found = True
                break

        if breaking_content_found:
            break

        for block_index, block in enumerate(blocks):
            text_block = block[4]
            if block_index == 0 or re.search(r'(Springer|bioRxiv|doi|license)', text_block, re.IGNORECASE):
                continue
            page_text.append(text_block.strip())

        cleaned = clean_text("\n".join(page_text))
        all_text.append(cleaned)

    return "\n\n".join(all_text)

def query_gpt(prompt, paper):
    full_prompt = f"{prompt}\n\n---\n\n{paper}"
    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.3,
            max_tokens=16384
        )
        return response.choices[0].message.content
    except Exception as e:
        print("API call failed:", e)
        return ""

def query_claude(prompt, paper):
    full_prompt = f"{prompt}\n\n---\n\n{paper}"
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS[CLAUDE_MODEL],
            temperature=0.3,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print("API call failed:", e)
        return ""

def main(paper_pdf, output_file, model_call):
    openai.api_key = OPENAI_API_KEY

    print(f"Reading and extracting from: {paper_pdf}")
    paper = extract_text_from_pdf_cleaned(paper_pdf)
    print("PDF text extracted.")

    if model_call == "gpt":
        insights = query_gpt(insight_extractor_prompt, paper)
    elif model_call == "claude":
        insights = query_claude(insight_extractor_prompt, paper)
    print(f"Insights extracted from paper.") if insights else print(f"No insights returned for paper.")
    insights = insights or "No insights returned for paper."
    with open(output_file, "w") as f:
        f.write(insights)

def batch_process_all_papers(base_folder, model_call):
    subdirs = [os.path.join(base_folder, d) for d in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, d))]
    for subdir in sorted(subdirs):
        paper_pdf = os.path.join(subdir, "paper.pdf")
        output_file = os.path.join(subdir, f"insights_paragraphs_{args.model_call}.txt")
        main(paper_pdf, output_file, model_call)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", type=str, required=True)
    parser.add_argument("--model_call", type=str, default="gpt", choices=["gpt", "claude"],)
    args = parser.parse_args()

    batch_process_all_papers(args.base_dir, args.model_call)
    print("All papers processed.")