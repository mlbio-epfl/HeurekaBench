from biomni.agent import A1
import dotenv
from biomni_prompts.mcq_initial_prompt import mcq_initial_prompt
from biomni_prompts.oe_initial_prompt import oe_initial_prompt
import re
import json
import argparse
import sys
import os

dotenv.load_dotenv()

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

def run_agent(insight_dict, output_dir, q_type, biomni_args):

    data_part_prompt = ""
    data_path2desc = insight_dict['data']
    for path, desc in data_path2desc.items():
        data_part_prompt += f"Path: {path}\nDescription: {desc}\n\n"
    
    data_part_prompt = data_part_prompt.strip()
        
    if q_type == 'oe':
        qs_dict = parse_oe_questions(insight_dict[f'{q_type}_question'])
    else:
        qs_dict = parse_mcq_question(insight_dict[f'{q_type}_question'])

    if len(qs_dict) == 0:
        print(f"No {q_type} questions found, skipping.")
        return
    for q_id, q_dict in qs_dict.items():
        output_path = os.path.join(output_dir, f"{q_id}_output.txt")
        if os.path.exists(output_path):
            print(f"Output {output_path} already exists, skipping.")
            continue

        # stdout and stderr to output file
        sys.stdout = open(output_path, 'w')
        sys.stderr = sys.stdout

        assert biomni_args["llm"] is not None, "LLM is not set"
        
        agent_kwargs = {
            "llm": biomni_args["llm"],
            "timeout_seconds": 1800,
            "temperature": biomni_args["temperature"],
            "self_critic": biomni_args["self_critic"],
            "plan_critic": biomni_args["plan_critic"],
            "use_tool_retriever": biomni_args["use_tool_retriever"]
        }
        
        if biomni_args["source"] is not None and biomni_args["base_url"] is not None:
            agent_kwargs["source"] = biomni_args["source"]
            agent_kwargs["base_url"] = biomni_args["base_url"]
        
        agent = A1(**agent_kwargs)

        if q_type == 'oe':
            curr_prompt = oe_initial_prompt.format(
                data_path=data_part_prompt,
                question=q_dict['question'],
            )
        else:
            curr_prompt = mcq_initial_prompt.format(
                data_path=data_part_prompt,
                question=q_dict['question'],
                answer_choices='\n'.join([f"{k}) {v}" for k, v in q_dict['options'].items()])
            )

        # save current prompt to file
        with open(os.path.join(output_dir, f'{q_id}_{q_type}_prompt.txt'), 'w') as f:
            f.write(curr_prompt)
        output = agent.go(curr_prompt)

        # flush and close the file
        sys.stdout.flush()
        sys.stdout.close()
        # reset stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        

def main(dataset_json_path, output_dir, q_type, biomni_args):
    with open(dataset_json_path, 'r') as f:
        dataset_dict = json.load(f)


    for p_id, p_dict in dataset_dict.items(): 
        print(f"Processing paper: {p_id}")
        p_dir = os.path.join(output_dir, p_id)

        for i_id, i_dict in p_dict.items():
            try:
                i_dir = os.path.join(p_dir, i_id)
                os.makedirs(i_dir, exist_ok=True)
                if f"{q_type}_question" in i_dict:
                    run_agent(i_dict, i_dir, q_type, biomni_args)
                else:
                    print(f"No {q_type} questions found for {p_id} - {i_id}, skipping.")
            except Exception as e:
                # flush and close the file
                sys.stdout.flush()
                sys.stdout.close()
                # reset stdout and stderr
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                print(f"Error processing {p_id} - {i_id}: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    
    # store all output into a output_file named output.txt
    parser = argparse.ArgumentParser(description='Run Biomni agent on datasets.')
    parser.add_argument('--dataset_json', type=str, required=True, help='Path to the dataset JSON file.')
    parser.add_argument('--output_dir', type=str, required=False, help='Path to save the output.', default='./output')
    parser.add_argument('--biomni_llm', type=str, required=False, help='Biomni LLM to use.', default=None)
    parser.add_argument('--biomni_source', type=str, required=False, help='Biomni source.', default=None)
    parser.add_argument('--biomni_base_url', type=str, required=False, help='Biomni base URL.', default=None)
    parser.add_argument('--temperature', type=float, required=False, help='Biomni temperature.', default=0.7)
    parser.add_argument('--q_type', type=str, required=True, help='Question type: mcq or oe.')
    parser.add_argument('--self_critic', action='store_true', help='Enable self-critic mode.')
    parser.add_argument('--plan_critic', action='store_true', help='Enable plan-critic mode.')
    parser.add_argument('--without_retriever', action='store_true', help='Disable tool retriever.')
    args = parser.parse_args()


    main(args.dataset_json, os.path.join(args.output_dir, args.biomni_llm, args.q_type), args.q_type, biomni_args={
        "llm": args.biomni_llm,
        "source": args.biomni_source,
        "base_url": args.biomni_base_url,
        "temperature": args.temperature,
        "self_critic": args.self_critic,
        "plan_critic": args.plan_critic,
        "use_tool_retriever": not args.without_retriever
    })
