import re
import os
import json
import time
import argparse
from geval_prompts import eval_prompts
from collections import defaultdict
import numpy as np
import dotenv
from openai import OpenAI
import pandas as pd
from statistics import mean

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
    
    return qs_dict

def compute_oe_score(content, top_logprobs, logprobs_data=None):
    """Extract and compute score from model response, with optional logprob weighting."""
    score = 0
    if not top_logprobs:
        try:
            score = float(re.findall(r"<rating>(\d+)</rating>", content)[0])
        except (IndexError, ValueError):
            score = 0
    else:
        try:
            rating_str = re.findall(r"<rating>(\d+)</rating>", content)[0]
            
            if logprobs_data:
                rating_token_entry = None
                for entry in logprobs_data:
                    if entry.get("token") == rating_str or entry.token == rating_str:
                        rating_token_entry = entry
                        break
                
                if rating_token_entry:
                    top_log = rating_token_entry.get("top_logprobs", getattr(rating_token_entry, "top_logprobs", None))
                    if top_log:
                        probs = [np.exp(obj["logprob"] if isinstance(obj, dict) else obj.logprob) for obj in top_log]
                        total = sum(probs)
                        probs = [p / total for p in probs]
                        ratings = [float(obj["token"] if isinstance(obj, dict) else obj.token) 
                                 if (obj["token"] if isinstance(obj, dict) else obj.token).isdigit() else 0 
                                 for obj in top_log]
                        score = sum([a * b for a, b in zip(ratings, probs)])
                    else:
                        score = float(rating_str)
                else:
                    score = float(rating_str)
            else:
                score = float(rating_str)
        except (IndexError, ValueError, AttributeError) as e:
            print(f"Scoring error: {e}")
            score = 0
    
    return float(score)

def load_evaluation_dataset(dataset_json_path, q_type):
    """Load and parse dataset into evaluation-ready format."""
    eval_dataset_dict = defaultdict(dict)
    
    with open(dataset_json_path, 'r') as f:
        dataset_dict = json.load(f)
   
    for p_id, p_dict in dataset_dict.items(): 
        eval_dataset_dict[p_id] = defaultdict(dict)
        for i_id, i_dict in p_dict.items():
            if f"{q_type}_question" in i_dict:
                curr_qs = create_dataset_element(i_dict, q_type)
                if curr_qs:
                    eval_dataset_dict[p_id][i_id] = curr_qs
            else:
                print(f"No {q_type} questions found for {p_id} - {i_id}, skipping.")
    
    return eval_dataset_dict

def main(dataset_json_path, results_json_path, q_type, batch_oe_judge=False, oe_specs={"model_name": "gpt-4o", "top_logprobs": 3}):
    if q_type == 'oe' and not batch_oe_judge:
        return main_non_batch(dataset_json_path, results_json_path, q_type, oe_specs)
    
    eval_dataset_dict = load_evaluation_dataset(dataset_json_path, q_type)
    
    with open(results_json_path, 'r') as f:
        results_dict = json.load(f)

    correct = 0
    total = 0
    total_answered = 0
    if q_type == "oe":
        requests = []
        custom_id_map = {}
        model_name = oe_specs["model_name"]
        top_logprobs = oe_specs["top_logprobs"]
        counter = 0 
    else:
        p2i2q_correct = defaultdict(lambda: defaultdict(list))
        recalls = []
        precisions = []
        f1s = []
        global_tps = 0
        global_fps = 0
        global_fns = 0
        global_num_pred = 0

    for p_id, p_dict in eval_dataset_dict.items():
        for i_id, i_dict in p_dict.items():
            for q_id, q_dict in i_dict.items():
                total += 1
                gt = q_dict["answer"].strip()
                if p_id in results_dict and i_id in results_dict[p_id] and q_id in results_dict[p_id][i_id]:
                    total_answered += 1
                    prediction = results_dict[p_id][i_id][q_id].strip()
                    if q_type == "mcq":
                        gt_letters = set(gt.split(","))
                        pred_letters = set(prediction.split(","))

                        if gt_letters == pred_letters:
                            p2i2q_correct[p_id][i_id].append(q_id)
                            correct += 1

                        tps = len(gt_letters.intersection(pred_letters))
                        fps = len(pred_letters - gt_letters)
                        fns = len(gt_letters - pred_letters)
                        num_pred = len(pred_letters)
                        if tps + fns > 0:
                            recall = tps / (tps + fns)
                            recalls.append(recall)
                        else:
                            recalls.append(0.0)
                        if tps + fps > 0:
                            precision = tps / num_pred
                            precisions.append(precision)    
                        else:
                            precisions.append(0.0)

                        f1s.append(2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0)

                        global_tps += tps
                        global_fps += fps
                        global_fns += fns
                        global_num_pred += num_pred
                    else:
                        template, system_message = eval_prompts.get_g_eval_prompt(method="basic")
                        prompt = template.format(answer=prediction, gt_answer=gt)

                        custom_id = f"req_{counter}"
                        counter += 1

                        requests.append({
                            "custom_id": custom_id,
                            "method": "POST",
                            "url": "/v1/chat/completions",
                            "body": {
                                "model": model_name,
                                "messages": [
                                    {"role": "system", "content": system_message},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": 0,
                                "max_tokens": 3000,
                                "top_p": 1,
                                "logprobs": bool(top_logprobs),
                                "top_logprobs": top_logprobs
                            }
                        })

                        custom_id_map[custom_id] = {
                            "p_id": p_id,
                            "i_id": i_id,
                            "q_id": q_id,
                            "question": q_dict["question"],
                            "prediction": prediction,
                            "ground_truth": gt
                        }
                else:
                    print(f"Missing prediction for {p_id} - {i_id} - {q_id}, skipping.")
    
    if q_type == "oe":
        results = []
        all_scores = []

        batch_file_path = f"batches/evaluation_batch/batch_input_{os.path.dirname(results_json_path)}.jsonl"
        os.makedirs(os.path.dirname(batch_file_path), exist_ok=True)
        with open(batch_file_path, "w") as f:
            for req in requests:
                f.write(json.dumps(req) + "\n")

        dotenv.load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        batch_file = client.files.create(
            file=open(batch_file_path, "rb"),
            purpose="batch"
        )

        batch = client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": f"evaluation batch {results_json_path}"}
        )

        print(f"Batch {batch.id} created. Waiting for completion...")

        status = batch.status
        while status not in ["completed", "failed", "expired"]:
            time.sleep(10)
            batch = client.batches.retrieve(batch.id)
            status = batch.status
            print(f"Batch status: {status}")

        if status != "completed":
            raise RuntimeError(f"Batch failed or expired with status {status}")

        output_file_id = batch.output_file_id
        output_file = client.files.content(output_file_id)
        results_jsonl = output_file.text.strip().split("\n")

        for line in results_jsonl:
            entry = json.loads(line)
            custom_id = entry["custom_id"]
            resp_body = entry["response"]["body"]
            choice = resp_body["choices"][0]
            content = choice["message"]["content"]

            score = compute_oe_score(content, top_logprobs, choice.get("logprobs", {}).get("content"))
            
            info = custom_id_map[custom_id]
            info["score"] = score
            all_scores.append(score)
            results.append(info)

        results_df = pd.DataFrame(results)
        results_df.to_csv(os.path.join(os.path.dirname(results_json_path), "oe_evaluation_results.csv"), index=False)
        final_score = mean(all_scores) if all_scores else 0.0
        print(f"Final mean score: {final_score:.4f}")
    else:
        macro_recall = mean(recalls) if recalls else 0.0
        macro_precision = mean(precisions) if precisions else 0.0
        
        micro_recall = global_tps / (global_tps + global_fns) if (global_tps + global_fns) > 0 else 0.0
        micro_precision = global_tps / global_num_pred if global_num_pred > 0 else 0.0
        micro_f1 = 2 * micro_precision * micro_recall / (micro_precision + micro_recall) if (micro_precision + micro_recall) > 0 else 0.0
        accuracy = correct / total if total > 0 else 0.0

        print(f"Accuracy: {correct}/{total} = {accuracy:.2%}\n")
        print(f"Macro Recall: {macro_recall:.2%}\n")
        print(f"Macro Precision: {macro_precision:.2%}\n")
        print(f"Macro F1: {mean(f1s):.2%}\n")
        print(f"Micro Recall: {micro_recall:.2%}\n")
        print(f"Micro F1: {micro_f1:.2%}\n")
        print(f"Micro Precision: {micro_precision:.2%}\n")
         
        output_dir = os.path.dirname(results_json_path)
        with open(os.path.join(output_dir, 'mcq_evaluation_results.txt'), 'w') as f:
            f.write(f"Accuracy: {correct}/{total} = {accuracy:.2%}\n")
            f.write(f"Macro Recall: {macro_recall:.2%}\n")
            f.write(f"Macro Precision: {macro_precision:.2%}\n")
            f.write(f"Macro F1: {mean(f1s):.2%}\n")
            f.write(f"Micro Recall: {micro_recall:.2%}\n")
            f.write(f"Micro Precision: {micro_precision:.2%}\n")
            f.write(f"Micro F1: {micro_f1:.2%}\n")
            
        with open(os.path.join(output_dir, 'mcq_detailed_results.json'), 'w') as f:
            json.dump(p2i2q_correct, f, indent=4)

        print(f"Detailed results saved to {os.path.join(output_dir, 'mcq_detailed_results.json')}")

def main_non_batch(dataset_json_path, results_json_path, q_type, oe_specs={"model_name": "gpt-4o", "top_logprobs": 3}):
    eval_dataset_dict = load_evaluation_dataset(dataset_json_path, q_type)
    
    with open(results_json_path, 'r') as f:
        results_dict = json.load(f)

    correct = 0
    total = 0

    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    if q_type == "oe":
        results = []
        all_scores = []
        model_name = oe_specs["model_name"]
        top_logprobs = oe_specs["top_logprobs"]

    for p_id, p_dict in eval_dataset_dict.items():
        for i_id, i_dict in p_dict.items():
            for q_id, q_dict in i_dict.items():
                print(f"Evaluating {p_id} - {i_id} - {q_id}...")
                total += 1
                gt = q_dict["answer"].strip()
                if p_id not in results_dict or i_id not in results_dict[p_id] or q_id not in results_dict[p_id][i_id]:
                    print(f"Missing prediction for {p_id} - {i_id} - {q_id}, skipping.")
                    continue

                prediction = results_dict[p_id][i_id][q_id].strip()

                if q_type == "mcq":
                    if gt == prediction:
                        correct += 1
                else:
                    template, system_message = eval_prompts.get_g_eval_prompt(method="basic")
                    prompt = template.format(answer=prediction, gt_answer=gt)

                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0,
                        max_tokens=1000,
                        top_p=1,
                        logprobs=bool(top_logprobs),
                        top_logprobs=top_logprobs,
                    )

                    print(f"Response: {response.choices[0].message.content}")
                    explanation = re.findall(
                        r"<explanation>(.*?)</explanation>",
                        response.choices[0].message.content,
                        re.DOTALL,
                    )
                   
                    if not top_logprobs:
                        score = re.findall(
                            r"<rating>(\d+)</rating>", response.choices[0].message.content
                        )[0]
                    else:
                        rating_str = re.findall(
                            r"<rating>(\d+)</rating>", response.choices[0].message.content
                        )[0]
                        tokens = [o.token for o in response.choices[0].logprobs.content]
                        rating_idx_in_response = tokens.index(rating_str)
                        top_log = response.choices[0].logprobs.content[rating_idx_in_response].top_logprobs
                        
                        probs = [np.exp(obj.logprob) for obj in top_log]
                        probs = [p / sum(probs) for p in probs]
                        ratings = [float(obj.token) if obj.token.isdigit() else 0 for obj in top_log]
                        score = sum([a * b for a, b in zip(ratings, probs)])
                    
                    score = float(score)
                    info = {
                        "p_id": p_id,
                        "i_id": i_id,
                        "q_id": q_id,
                        "question": q_dict["question"],
                        "prediction": prediction,
                        "ground_truth": gt,
                        "score": score,
                        "explanation": explanation[0].strip() if explanation else "",
                    }
                    all_scores.append(score)
                    results.append(info)
                    time.sleep(2)

    if q_type == "oe":
        results_df = pd.DataFrame(results)
        results_df.to_csv(os.path.join(os.path.dirname(results_json_path), "oe_evaluation_results.csv"), index=False)
        final_score = mean(all_scores) if all_scores else 0.0
        print(f"Final mean score: {final_score:.4f}")
    else:
        print(f"Accuracy: {correct}/{total} = {correct/total:.2%}")
        with open(os.path.join(os.path.dirname(results_json_path), 'mcq_evaluation_results.txt'), 'w') as f:
            f.write(f"Accuracy: {correct}/{total} = {correct/total:.2%}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate agent answers against ground truth.')
    parser.add_argument('--dataset_json', type=str, required=True, help='Path to the dataset JSON file.')
    parser.add_argument('--results_json', type=str, required=True, help='Path to the results JSON file.')
    parser.add_argument('--q_type', type=str, required=True, choices=['mcq', 'oe'], help='Question type: mcq or oe.')
    parser.add_argument('--batch_oe_judge', action='store_true', help='Use batch processing for open-ended question evaluation.')
    args = parser.parse_args()

    main(args.dataset_json, args.results_json, args.q_type, batch_oe_judge=args.batch_oe_judge)