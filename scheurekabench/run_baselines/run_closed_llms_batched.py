import re
import os
import json
from openai import OpenAI
import dotenv
import time
import anthropic
import argparse
from collections import defaultdict
from llms_prompts.mcq_initial_prompt import mcq_initial_prompt
from llms_prompts.oe_initial_prompt import oe_initial_prompt
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request


# Load environment variables from .env file
dotenv.load_dotenv()
# === CONFIGURATION ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

OPENAI_MODEL_DEFAULT = "gpt-4o"
CLAUDE_MODEL_DEFAULT = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = {
    "claude-sonnet-4-20250514": 16384,
    "claude-3-7-sonnet-20250219": 8192,
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
    pattern = r"\*\*Question(\d+):\*\*\s*(.*?)\s*((?:[A-D]\).*?(?:\s+))+)\*\*Answer\1:\*\*\s*([A-D](?:,[A-D])*)"

    matches = re.findall(pattern, text, re.DOTALL)

    questions_dict = {}
    for num, q_text, options_block, ans in matches:
        options = dict(re.findall(r"([A-D])\)\s*(.*)", options_block))
        questions_dict[f"Question{num}"] = {
            "question": q_text.strip(),
            "options": options,
            # "answer": ans
        }

    return questions_dict

def parse_oe_questions(text):
    # Pattern to match QuestionN blocks (ignore answers)
    pattern = r"\*\*Question(\d+):\*\*\s*(.*?)(?=\s*\*\*Answer\d+:|\Z)"
    
    matches = re.findall(pattern, text, re.DOTALL)

    questions_dict = {}
    for num, q_text in matches:
        questions_dict[f"Question{num}"] = {
           "question": q_text.strip()
        }
    return questions_dict

def create_batch_element(insight_dict, output_dir, q_type):
        
    if q_type == 'oe':
        qs_dict = parse_oe_questions(insight_dict[f'{q_type}_question'])
    else:
        qs_dict = parse_mcq_question(insight_dict[f'{q_type}_question'])

    if len(qs_dict) == 0:
        print(f"No {q_type} questions found, skipping.")
        return
    
    curr_prompts = defaultdict(str)
    for q_id, q_dict in qs_dict.items():

        if q_type == 'oe':
            curr_prompt = oe_initial_prompt.format(
                question=q_dict['question'],
            )
        else:
            curr_prompt = mcq_initial_prompt.format(
                question=q_dict['question'],
                answer_choices='\n'.join([f"{k}) {v}" for k, v in q_dict['options'].items()])
            )

        curr_prompts[q_id] = curr_prompt

    return curr_prompts

def main(dataset_json_path, output_dir, llm_name, q_type):
    
    if llm_name == "GPT":
        MODEL_DEFAULT = OPENAI_MODEL_DEFAULT
    elif llm_name == "CLAUDE":
        MODEL_DEFAULT = CLAUDE_MODEL_DEFAULT
    elif llm_name == "CLAUDE-3.7":
        MODEL_DEFAULT = "claude-3-7-sonnet-20250219"

    # start clients
    if llm_name == "GPT":
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    
    with open(dataset_json_path, 'r') as f:
        dataset_dict = json.load(f)

    # create batch requests
    batch_requests = []
    custom_id_map = {}  # Map custom_id to (dir_name, q_idx)
    request_counter = 0
    
    for p_id, p_dict in dataset_dict.items(): 
        print(f"Processing paper: {p_id}")
        p_dir = os.path.join(output_dir, p_id)

        for i_id, i_dict in p_dict.items():
            i_dir = os.path.join(p_dir, i_id)
            if f"{q_type}_question" in i_dict:
                question_prompts = create_batch_element(i_dict, i_dir, q_type)
                for q_idx, prompt in question_prompts.items():
                    custom_id = f"req_{request_counter}"
                    request_counter += 1
                    if llm_name == "GPT":
                        batch_element = {
                        "custom_id": custom_id,
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": MODEL_DEFAULT,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 1.0,
                            }
                        }
                    else:
                        batch_element = Request(
                            custom_id=custom_id,
                            params = MessageCreateParamsNonStreaming(
                                model=MODEL_DEFAULT,
                                max_tokens=CLAUDE_MAX_TOKENS[MODEL_DEFAULT],
                                messages=[{"role": "user", "content": prompt}],
                                temperature=1.0,
                            ),
                        )
                    batch_requests.append(batch_element)    
                    custom_id_map[custom_id] = (p_id, i_id, q_idx)
            else:
                print(f"No {q_type} questions found for {p_id} - {i_id}, skipping.")

    # run batch
    if llm_name == "GPT":
        # Save batch input to JSONL
        batch_file_path = f"./batches/run_openai_batch/batch_input_{q_type}.jsonl"
        os.makedirs(os.path.dirname(batch_file_path), exist_ok=True)
        batch_input_path = batch_file_path
        with open(batch_input_path, "w") as f:
            for req in batch_requests:
                f.write(json.dumps(req) + "\n")

        # Upload batch input file
        batch_input_file = client.files.create(
            file=open(batch_input_path, "rb"),
            purpose="batch"
        )

        # Create batch
        batch = client.batches.create(
            input_file_id=batch_input_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": "Dataset evaluation batch"}
        )

        print("Batch created:", batch.id)
        # Poll batch status
        status = batch.status
        while status not in ["completed", "failed", "expired"]:
            time.sleep(20)
            batch = client.batches.retrieve(batch.id)
            status = batch.status
            print(f"Batch status: {status}")

        if status != "completed":
            raise RuntimeError(f"Batch failed or expired with status {status}")
    else:
        batch = client.messages.batches.create(
            requests=batch_requests,
        )
        b_id = batch.id

        message_batch = None
        while True:
            time.sleep(20)
            message_batch = client.messages.batches.retrieve(
                b_id
            )
            if message_batch.processing_status == "ended":
                break
                    
            print(f"Batch {b_id} is still processing...")

    results = defaultdict(dict)
    if llm_name == "GPT":
        # Once the batch is complete, retrieve results:
        output_file_id = batch.output_file_id
        file_response = client.files.content(output_file_id)
        batch_lines = file_response.text.strip().split("\n")

        for line in batch_lines:
            record = json.loads(line)
            custom_id = record["custom_id"]
            dir_name, i_idx, q_idx = custom_id_map[custom_id]
            
            if record["error"] is None:
                content = record["response"]["body"]["choices"][0]["message"]["content"]
                # select content between <solution> and </solution> if there are <solution> tags
                # with re
                if "<solution>" in content and "</solution>" in content:
                    content = re.search(r"<solution>(.*?)</solution>", content, re.DOTALL).group(1).strip()
                else:
                    content = content.replace("<solution>", "").replace("</solution>", "").strip()
            else:
                content = ""
                print(f"Error for {custom_id}: {record['error']}")
            
            if i_idx not in results[dir_name]:
                results[dir_name][i_idx] = {}
            results[dir_name][i_idx][q_idx] = content
    else:
        for result in client.messages.batches.results(b_id):
            custom_id = result.custom_id
            dir_name, i_idx, q_idx = custom_id_map[custom_id]
            res_block = result.result
            message_block = res_block.message
            if res_block.type == "succeeded":
                content_list = message_block.content
                content = "\n".join([msg.text for msg in content_list])
                if "<solution>" in content and "</solution>" in content:
                    content = re.search(r"<solution>(.*?)</solution>", content, re.DOTALL).group(1).strip()
                else:
                    content = content.replace("<solution>", "").replace("</solution>", "").strip()
            else:
                content = ""
                print(f"Error for {custom_id}: {result.error}")
            
            if i_idx not in results[dir_name]:
                results[dir_name][i_idx] = {}
            results[dir_name][i_idx][q_idx] = content

    # Save final results
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("Results saved to", output_dir)
    if q_type == 'mcq': 
        clean_answers_in_json(file_path=os.path.join(output_dir, "results.json"))

if __name__ == "__main__":
    
    # store all output into a output_file named output.txt
    parser = argparse.ArgumentParser(description='Run Biomni agent on datasets.')
    parser.add_argument('--dataset_json', type=str, required=True, help='Path to the dataset JSON file.')
    parser.add_argument('--output_dir', type=str, required=False, help='Path to save the output.', default='./output')
    parser.add_argument('--llm_name', type=str, required=False, help='Biomni LLM to use.', default=None)
    parser.add_argument('--q_type', type=str, required=True, help='Question type: mcq or oe.')
    args = parser.parse_args()


    main(args.dataset_json, os.path.join(args.output_dir,  os.path.basename(os.path.dirname(args.dataset_json)), args.llm_name, args.q_type), args.llm_name, args.q_type)