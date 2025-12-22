import re
import os
import json
import argparse
from collections import defaultdict
from llms_prompts.mcq_initial_prompt import mcq_initial_prompt
from llms_prompts.oe_initial_prompt import oe_initial_prompt
from transformers import AutoModelForCausalLM, AutoTokenizer

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
    pattern = r"\*\*Question(\d+):\*\*\s*(.*?)\s*((?:[A-D]\).*?(?:\s+))+)\*\*Answer\1:\*\*\s*([A-D](?:,[A-D])*)"

    matches = re.findall(pattern, text, re.DOTALL)

    questions_dict = {}
    for num, q_text, options_block, ans in matches:
        options = dict(re.findall(r"([A-D])\)\s*(.*)", options_block))
        questions_dict[f"Question{num}"] = {
            "question": q_text.strip(),
            "options": options,
            "answer": ans
        }

    return questions_dict

def parse_oe_questions(text):
    pattern = r"\*\*Question(\d+):\*\*\s*(.*?)\s*\*\*Answer\1:\*\*\s*(.*?)(?=\s*\*\*Question\d+:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)

    questions_dict = {}
    for num, question, answer in matches:
        questions_dict[f"Question{num}"] = {
            "question": question.strip(),
            "answer": answer.strip()
        }
    return questions_dict

def create_dataset_element(insight_dict, q_type):
    if q_type == 'oe':
        qs_dict = parse_oe_questions(insight_dict[f'{q_type}_question'])
    else:
        qs_dict = parse_mcq_question(insight_dict[f'{q_type}_question'])

    if len(qs_dict) == 0:
        print(f"No {q_type} questions found, skipping.")
        return
    
    curr_qs = defaultdict(str)
    for q_id, q_dict in qs_dict.items():
        curr_qs[q_id] = q_dict

    return curr_qs

def get_dataset(dataset_json_path, q_type):
    eval_dataset_dict = defaultdict(dict)

    with open(dataset_json_path, 'r') as f:
        dataset_dict = json.load(f)
   
    for p_id, p_dict in dataset_dict.items(): 
        eval_dataset_dict[p_id] = defaultdict(dict)
        for i_id, i_dict in p_dict.items():
            if f"{q_type}_question" in i_dict:
                curr_qs = create_dataset_element(i_dict, q_type)
                eval_dataset_dict[p_id][i_id] = curr_qs
            else:
                print(f"No {q_type} questions found for {p_id} - {i_id}, skipping.")
    return eval_dataset_dict

def main(dataset_json_path, output_dir, llm_name, q_type):
    dataset_dict = get_dataset(dataset_json_path, q_type)
    # load the tokenizer and the model
    tokenizer = AutoTokenizer.from_pretrained(llm_name)
    model = AutoModelForCausalLM.from_pretrained(
        llm_name,
        torch_dtype="auto",
        device_map="auto"
    )

    results = defaultdict(lambda: defaultdict(dict))
    for p_id, p_dict in dataset_dict.items():
        for i_id, i_dict in p_dict.items():
            for q_id, q_dict in i_dict.items():
                if q_type == 'oe':
                    curr_prompt = oe_initial_prompt.format(
                        question=q_dict['question'],
                    )
                else:
                    curr_prompt = mcq_initial_prompt.format(
                        question=q_dict['question'],
                        answer_choices='\n'.join([f"{k}) {v}" for k, v in q_dict['options'].items()])
                    )

                print(f"Processing {p_id} - {i_id} - {q_id}")
                messages = [
                    {"role": "user", "content": curr_prompt}
                ]
                text = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                    enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
                )
                model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

                # conduct text completion
                generated_ids = model.generate(
                    **model_inputs,
                    max_new_tokens=32768
                )
                output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

                # parsing thinking content
                try:
                    # rindex finding 151668 (</think>)
                    index = len(output_ids) - output_ids[::-1].index(151668)
                except ValueError:
                    index = 0

                content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
                if "<solution>" in content and "</solution>" in content:
                    content = re.search(r"<solution>(.*?)</solution>", content, re.DOTALL).group(1).strip()
                else:
                    content = content.replace("<solution>", "").replace("</solution>", "").strip()

                results[p_id][i_id][q_id] = content

        # Save interim results
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "results.json"), "w") as f:
            json.dump(results, f, indent=2)

    # Save final results
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("Results saved to", output_dir)
    if q_type == 'mcq':
        clean_answers_in_json(file_path=os.path.join(output_dir, "results.json"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_json_path", type=str, required=True, help="Path to the dataset JSON file.")
    parser.add_argument("--output_dir", type=str, required=False, help="Directory to save the results.", default="./output")
    parser.add_argument("--llm_name", type=str, required=True, help="Name of the LLM model (e.g., 'qwen-7b-chat').")
    parser.add_argument("--q_type", type=str, choices=['mcq', 'oe'], required=True, help="Type of questions: 'mcq' or 'oe'.")
    args = parser.parse_args()
   
    main(args.dataset_json_path, os.path.join(args.output_dir, args.llm_name, args.q_type), args.llm_name, args.q_type)
