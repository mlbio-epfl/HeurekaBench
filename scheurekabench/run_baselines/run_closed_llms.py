import re
import os
import json
from openai import OpenAI
import dotenv
import anthropic
import argparse
from collections import defaultdict
from llms_prompts.mcq_initial_prompt import mcq_initial_prompt
from llms_prompts.oe_initial_prompt import oe_initial_prompt

# Load environment variables from .env file
dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

OPENAI_MODEL_DEFAULT = "gpt-4o"
CLAUDE_MODEL_DEFAULT = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = {
    "claude-sonnet-4-20250514": 16384,
}


def clean_answers_in_json(file_path: str, output_path: str = None):
    # Load JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def is_valid_answer(ans: str) -> bool:
        # Valid if it matches letters A-D separated by commas, e.g. "A", "A,B", "A,B,C,D"
        return bool(re.fullmatch(r"(?:[A-D](?:,[A-D])*)", ans.strip()))

    # Recursive dictionary cleaning
    def process_dict(d: dict):
        keys_to_delete = []
        for key, value in d.items():
            if isinstance(value, dict):
                process_dict(value)
                # Remove empty dicts as well
                if not value:
                    keys_to_delete.append(key)
            elif isinstance(value, str):
                if not is_valid_answer(value):
                    keys_to_delete.append(key)
        for k in keys_to_delete:
            del d[k]

    process_dict(data)

    # Save cleaned JSON
    if not output_path:
        output_path = file_path.replace(".json", "_cleaned.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Cleaned JSON saved to {output_path}")

def parse_mcq_question(text):
    pattern = r"\*\*Question(\d+):\*\*\s*(.*?)\s*((?:[A-D]\).*?(?:\s+))+?)\*\*Answer\1:\*\*\s*([A-D](?:,[A-D])*)"
    matches = re.findall(pattern, text, re.DOTALL)

    questions_dict = {}
    for num, q_text, options_block, ans in matches:
        options = dict(re.findall(r"([A-D])\)\s*(.*)", options_block))
        questions_dict[f"Question{num}"] = {
            "question": q_text.strip(),
            "options": options,
        }
    return questions_dict

def parse_oe_questions(text):
    pattern = r"\*\*Question(\d+):\*\*\s*(.*?)(?=\s*\*\*Answer\d+:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)

    questions_dict = {}
    for num, q_text in matches:
        questions_dict[f"Question{num}"] = {"question": q_text.strip()}
    return questions_dict

def create_prompts(insight_dict, q_type):
    if q_type == 'oe':
        qs_dict = parse_oe_questions(insight_dict[f'{q_type}_question'])
    else:
        qs_dict = parse_mcq_question(insight_dict[f'{q_type}_question'])

    if len(qs_dict) == 0:
        print(f"No {q_type} questions found, skipping.")
        return {}

    curr_prompts = {}
    for q_id, q_dict in qs_dict.items():
        if q_type == 'oe':
            curr_prompt = oe_initial_prompt.format(question=q_dict['question'])
        else:
            curr_prompt = mcq_initial_prompt.format(
                question=q_dict['question'],
                answer_choices='\n'.join([f"{k}) {v}" for k, v in q_dict['options'].items()])
            )
            # save prompt for each question
            with open("./tmp.txt", "w") as f:
                f.write(curr_prompt)
        curr_prompts[q_id] = curr_prompt
    return curr_prompts

def run_prompt(client, llm_name, model, prompt):
    if "GPT" in llm_name:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
        )
        content = response.choices[0].message.content
    else:
        response = client.messages.create(
            model=model,
            max_tokens=CLAUDE_MAX_TOKENS[model],
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
        )
        content = "\n".join([c.text for c in response.content])

    if "<solution>" in content and "</solution>" in content:
        content = re.search(r"<solution>(.*?)</solution>", content, re.DOTALL).group(1).strip()
    else:
        content = content.replace("<solution>", "").replace("</solution>", "").strip()
    return content

def main(dataset_json_path, output_dir, llm_name, q_type):
    if llm_name == "GPT":
        MODEL_DEFAULT = OPENAI_MODEL_DEFAULT
        client = OpenAI(api_key=OPENAI_API_KEY)
    elif llm_name == "CLAUDE":
        MODEL_DEFAULT = CLAUDE_MODEL_DEFAULT
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    elif llm_name == "GPT-5":
        MODEL_DEFAULT = "gpt-5"
        client = OpenAI(api_key=OPENAI_API_KEY)    

    with open(dataset_json_path, 'r') as f:
        dataset_dict = json.load(f)

    results = defaultdict(dict)

    for p_id, p_dict in dataset_dict.items():
        print(f"Processing paper: {p_id}")
        for i_id, i_dict in p_dict.items():
            if f"{q_type}_question" in i_dict:
                question_prompts = create_prompts(i_dict, q_type)
                for q_idx, prompt in question_prompts.items():
                    try:
                        content = run_prompt(client, llm_name, MODEL_DEFAULT, prompt)
                    except Exception as e:
                        print(f"Error processing {p_id}-{i_id}-{q_idx}: {e}")
                        content = ""
                    if i_id not in results[p_id]:
                        results[p_id][i_id] = {}
                    results[p_id][i_id][q_idx] = content
            else:
                print(f"No {q_type} questions found for {p_id} - {i_id}, skipping.")

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("Results saved to", output_dir)

    if q_type == 'mcq': 
        clean_answers_in_json(file_path=os.path.join(output_dir, "results.json"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Biomni agent on datasets without batch API.')
    parser.add_argument('--dataset_json', type=str, required=True, help='Path to the dataset JSON file.')
    parser.add_argument('--output_dir', type=str, required=False, default='./output', help='Path to save the output.')
    parser.add_argument('--llm_name', type=str, required=False, default="GPT", choices=['GPT', 'CLAUDE'], help='LLM to use')
    parser.add_argument('--q_type', type=str, required=True, choices=['mcq', 'oe'], help='Question type')
    args = parser.parse_args()

    out_path = os.path.join(args.output_dir, os.path.basename(os.path.dirname(args.dataset_json)), args.llm_name, args.q_type)
    main(args.dataset_json, out_path, args.llm_name, args.q_type)

