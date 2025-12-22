import argparse
import json
import os
import openai
import re
from pathlib import Path
from dotenv import load_dotenv
import anthropic
import ast
import nbformat

from prompts.code_matcher import code_matcher_prompt
from prompts.code_generator import code_generator_prompt
from utils.append_tree_to_prompt import inject_tree_into_prompt_text

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

OPENAI_MODEL_DEFAULT = "gpt-4o"
CLAUDE_MODEL_DEFAULT = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = {
    "claude-sonnet-4-20250514": 16384,
}


def call_gpt(prompt, model=OPENAI_MODEL_DEFAULT, temperature=0.3, json_output=False):
    kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    if json_output:
        kwargs["response_format"] = {"type": "json_object"}

    response = openai.chat.completions.create(**kwargs)
    return response.choices[0].message.content

def call_claude(prompt, model=CLAUDE_MODEL_DEFAULT, temperature=0.3, json_output=False):
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    messages = [{"role": "user", "content": prompt}]
    try:
        response = client.messages.create(
            model=model,
            max_tokens=CLAUDE_MAX_TOKENS[model],
            temperature=temperature,
            messages=messages
        )
        
        return response.content[0].text
    except Exception as e:
        print(f"Claude API call failed: {e}")
        return ""

def call_llm(prompt, model_call="gpt", temperature=0.3):
    return call_gpt(prompt, temperature=temperature) if model_call == "gpt" else call_claude(prompt, temperature=temperature)

def call_llm_with_json(prompt, model_call="gpt", temperature=0.3):
    return call_gpt(prompt, temperature=temperature, json_output=True) if model_call == "gpt" else call_claude(prompt, temperature=temperature)


def parse_insights_v2(insights_txt_path):
    insights = []
    with open(insights_txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex pattern to match each insight block
    pattern = re.compile(
        r"\*\*Insight #\d+\*\*\n\n"                           # Insight header
        r"\*Summary:\*\n(.*?)\n\n"                            # Summary
        r"\*How it was derived:\*\n(.*?)\n\n"                 # How it was derived
        r"\*Relevant text paragraphs:\*\n(.*?)(?=\n\n\*\*Insight #\d+\*\*|\Z)",  # Relevant paragraphs
        re.DOTALL
    )

    for match in pattern.finditer(content):
        summary = match.group(1).strip()
        description = match.group(2).strip()
        relevant_text = match.group(3).strip()
        insights.append({
            "summary": summary,
            "description": description,
            "relevant_text": relevant_text
        })

    return insights


def retrieve_relevant_files(insight, code_summary_dict, model_call):
    code_descriptions = "\n".join([f"`{path}`:\n{desc}" for path, desc in code_summary_dict.items()])
    
    prompt = code_matcher_prompt + \
    "\n\n" + f"High-Level Insight:\n *Summary*:\n{insight['summary']}\n\n *Description*:\n{insight['description']}\n\n *Relevant text*:\n{insight['relevant_text']}\n\n Code Files and Their Descriptions:\n{code_descriptions}\n\n"
    
    output = call_llm(prompt, model_call=model_call)
    if not output:
        return []
    
    cleaned_output = output.strip()

    match = re.search(r"\[.*?\]", cleaned_output)
    if match:
        list_str = match.group(0)
        list_str = list_str.replace('`', "'")

        paths = ast.literal_eval(list_str)
        return paths

    if cleaned_output.startswith('```python'):
        cleaned_output = cleaned_output[9:]
    if cleaned_output.endswith('```'):
        cleaned_output = cleaned_output[:-3]
    cleaned_output = cleaned_output.strip()
    

    try:
        return json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Trying with ast...")
        try:
            return ast.literal_eval(cleaned_output)
        except Exception as e:
            print(f"AST literal eval failed: {e}")
            try: 
                print(f"Trying to replace backticks...")
                output_fixed = cleaned_output.replace('`', "'")
                return ast.literal_eval(output_fixed)
            except Exception as e:
                print(f"Returning empty list.")
                return []


def match_code_to_insight(insight, script_dict, model_call, root_dir):
    mi_prompt = inject_tree_into_prompt_text(code_generator_prompt, root_dir=root_dir)

    prompt = mi_prompt + \
    "\n\n" + f"High-Level Insight:\n *Summary*:\n{insight['summary']}\n\n *Description*:\n{insight['description']}\n\n" + \
    "\n\n" + f"Relevant Code:\n{script_dict}\n\n"

    return call_llm_with_json(prompt, model_call=model_call, temperature=1.0)


def main(paper_dir, output_file, model_call):
    openai.api_key = OPENAI_API_KEY

    insight_file = os.path.join(paper_dir, f"insights_paragraphs_gpt.txt")
    insights = parse_insights_v2(insight_file)
    print(f"Parsed {len(insights)} insights from '{insight_file}'.")
    
    if not os.path.exists(os.path.join(paper_dir, f"code_insights_{model_call}.json")):
        print(f"Code insights file not found for {paper_dir}. Please run the code insights extraction first.")
        return
    
    with open(os.path.join(paper_dir, f"code_insights_{model_call}.json"), "r") as f:
        code_summary_dict = json.load(f)

    output = {}
    existing_codes_for_insights = json.load(open(output_file, "r"))

    for idx, insight in enumerate(insights):
        print(f"\nProcessing Insight #{idx+1}...")
        if f"Insight Summary #{idx+1}" in existing_codes_for_insights:
            print(f"Insight #{idx+1} already has code. Skipping...")
            continue

        
        relevant_files = retrieve_relevant_files(insight, code_summary_dict, model_call=model_call)
        if not relevant_files:
            print(f"No relevant files found for Insight #{idx+1}. Using all files in the code directory.")
            relevant_files = code_summary_dict.keys()
        script_dict = {}
        for path in relevant_files:
            file_path = Path(os.path.join(paper_dir, "code", path))
            if file_path.exists():
                if file_path.suffix not in ['.ipynb']:
                    script_dict[path] = file_path.read_text()
                else:
                    # convert ipynb to python script
                    try:
                        with open(file_path, "r") as f:
                            nb = nbformat.read(f, as_version=4)
                        code_cells = [cell.source for cell in nb.cells if cell.cell_type == "code"]
                        script = "\n\n".join(code_cells)
                        script_dict[path] = script
                    except Exception as e:
                        print(f"Error reading {path}: {e}")
            else:
                print(f"Warning: File {path} not found!")

        if not script_dict:
            print(f"No code found for Insight #{idx+1}. Skipping... Relevent files: {relevant_files}")
            continue

        matched_result = match_code_to_insight(insight, script_dict, model_call=model_call, root_dir=os.path.join(paper_dir, "code"))
        # delete everything before the first ```json in the matched_result
        if matched_result:
            matched_result = matched_result.split("```json", 1)[-1]
            if matched_result.endswith("```"):
                matched_result = matched_result[:-3].strip()
            else:
                matched_result = matched_result.strip()
        try:
            
            parsed = json.loads(matched_result) if matched_result else {}
            
            output.update({
                f"Insight Summary #{idx+1}": parsed[f"Insight Summary"]
            })
        except json.JSONDecodeError:
            print("Warning: LLM output was not valid JSON. Trying to clean the output.")
            try:
                # get only part starting with ```json
                if matched_result.startswith("```json"):
                    matched_result = matched_result.split("```json")[1]
                    if matched_result.endswith("```"):
                        matched_result = matched_result[:-3]
                        
                cleaned_output = matched_result.strip().removeprefix("```json").removesuffix("```").strip()
                parsed = json.loads(cleaned_output)
                output.update({
                    f"Insight Summary #{idx+1}": parsed[f"Insight Summary"]
                })
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                print(f"LLM output was: {matched_result}")
                continue
        except Exception as e:
            print(f"Unexpected error while processing Insight #{idx+1}: {e}")
            continue
        
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)

    print(f"\n All insights processed and saved to '{output_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", type=str, required=True)
    parser.add_argument("--model_call", type=str, default="claude", choices=["gpt", "claude"])
    args = parser.parse_args()

    paper_dirs = [os.path.join(args.base_dir, d) for d in os.listdir(args.base_dir) if os.path.isdir(os.path.join(args.base_dir, d))]
    model_call = args.model_call
    
    for paper_dir in paper_dirs:
        output_file = os.path.join(paper_dir, f"final_insight_code_mapping_{model_call}.json")
        main(paper_dir, output_file, model_call=model_call)