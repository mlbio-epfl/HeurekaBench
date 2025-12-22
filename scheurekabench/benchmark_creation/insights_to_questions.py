import openai
import anthropic
import os
import time
import re
import argparse
import json
import dotenv
from prompts.insight2question_prompt import insight2question_prompt_text as insight2mcq_question_prompt_text
from prompts.insight2open_question_prompt import insight2question_prompt_text as insight2open_question_prompt_text

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

def query_gpt(full_prompt):
    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.3,
            max_tokens=16384
        )
        return response.choices[0].message.content
    except Exception as e:
        print("GPT API call failed:", e)
        return ""

def query_claude(full_prompt):
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS[CLAUDE_MODEL],
            temperature=0.3,
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print("Claude API call failed:", e)
        return ""

def main(insight_json_path, model_call, q_type):
    with open(insight_json_path, "r") as f:
        insights_data = json.load(f)

    output_dir = os.path.dirname(insight_json_path)
    output_path = os.path.join(output_dir, f"{q_type}_questions.json")
    output_txt_path = os.path.join(output_dir, f"{q_type}_questions.txt")

    all_questions = ""
    output_dict = {}
    for paper_id, paper_content in insights_data.items():
        insight_text4prompt = ""
        for insight_idx, (insight_id, insight_content) in enumerate(paper_content.items()):
            summary = insight_content["summary"]
            how = insight_content["how"]
            relevant = insight_content["relevant"]

            insight_text4prompt += f"#### Insight #{insight_idx + 1}\n\n* Summary: {summary}\n\n* How it was derived: {how}\n\n* Associated paragraphs from the paper: {relevant}\n\n\n"

        insight_text4prompt = insight_text4prompt.strip()
        if q_type == "mcq":
            full_prompt = insight2mcq_question_prompt_text.format(insights=insight_text4prompt)
        else:
            full_prompt = insight2open_question_prompt_text.format(insights=insight_text4prompt)
            
        if model_call == "gpt":
            questions = query_gpt(full_prompt)
        else:
            questions = query_claude(full_prompt)
        if questions:
            print(f"Question generated for paper {paper_id}.")
        else:
            print(f"No question returned for paper {paper_id}.")
            questions = "No question generated."

        # parse questions into list for each insight; between each insight is ---
        q_per_insight_list = [q.strip() for q in questions.split('---') if q.strip()]

        for idx, (insight_id, insight_content) in enumerate(paper_content.items()):
            if idx < len(q_per_insight_list):
                insight_content[f"{q_type}_question"] = q_per_insight_list[idx]
            else:
                insight_content[f"{q_type}_question"] = "No question generated."
        output_dict[paper_id] = paper_content
        all_questions += f"Paper ID: {paper_id}\n{questions}\n==========\n\n"

        time.sleep(60)
    with open(output_txt_path, "w") as out_txt_f:
        out_txt_f.write(all_questions)

    with open(output_path, "w") as out_f:
        json.dump(output_dict, out_f, indent=2)
    
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--insight_json_path", type=str, required=True, help="Path to insights.json file")
    parser.add_argument("--model_call", type=str, default="gpt", choices=["gpt", "claude"])
    parser.add_argument("--qtype", type=str, choices=["mcq", "oe"])
    args = parser.parse_args()

    main(args.insight_json_path, args.model_call, args.qtype)
