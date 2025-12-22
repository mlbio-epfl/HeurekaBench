import re
import os
import json
import time
import argparse
from collections import defaultdict
import time
import numpy as np
import dotenv
from openai import OpenAI
import pandas as pd
from statistics import mean

import insightextractor_eval_prompts as eval_prompts  

def parse_insights(text):
    # Regex to extract the summary
    # It captures everything between "*Summary:*" and the next "*How it was derived:*"
    summary_pattern = r"\*Summary:\*\n(.*?)(?=\n\*How it was derived:\*)"

    summaries = re.findall(summary_pattern, text, re.DOTALL)

    # Optional: strip leading/trailing whitespace for each summary
    summaries = [f"Insight {s_idx}:" + s.strip() for s_idx, s in enumerate(summaries)]
    summaries = "\n\n".join(summaries)
    return summaries    

def main(dataset_path, gt_insights_path, oe_specs={"model_name": "gpt-4o", "top_logprobs": None}):
    papers_dirs = os.listdir(dataset_path)
    papers_dirs = [os.path.join(dataset_path, d) for d in papers_dirs if os.path.isdir(os.path.join(dataset_path, d)) and os.path.exists(os.path.join(dataset_path, d, "insights_paragraphs_gpt.txt"))]

    gt_insights = pd.read_csv(gt_insights_path, sep=";")

    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    strongly_related = 0
    realted = 0
    not_related = 0
    total = 0

    for paper_path in papers_dirs:   
        model_name = oe_specs["model_name"]
        top_logprobs = oe_specs["top_logprobs"]
        template, system_message = eval_prompts.get_insightextractor_eval_prompt(method="basic")

        summaries = parse_insights(open(os.path.join(paper_path, "insights_paragraphs_gpt.txt")).read())
        gt_insight = gt_insights[gt_insights["id"] == int(os.path.basename(paper_path).replace("paper", ""))]["findings"].values[0]
        prompt = template.format(llm_insights=summaries, scientist_insight=gt_insight)
        with open(f"./temp_123.txt", "w") as f:
            f.write(prompt)

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=1000,
            top_p=1,
            logprobs=bool(top_logprobs),
            top_logprobs=top_logprobs,
        )                

        # print(f"Response: {response.choices[0].message.content}")
        if not top_logprobs:
            score = re.findall(
            r"<rating>(\d+)</rating>", response.choices[0].message.content
            )[0]
        else:
            # get the index in response where we have the rating
            rating_str = re.findall(
                r"<rating>(\d+)</rating>", response.choices[0].message.content
            )[0]
            tokens = [o.token for o in response.choices[0].logprobs.content]
            rating_idx_in_response = tokens.index(rating_str)
            response = (
                response.choices[0]
                .logprobs.content[rating_idx_in_response]
                .top_logprobs
            )
            # convert logprobs to probs
            probs = [np.exp(obj.logprob) for obj in response]
            # renormalize probs to sum to 1
            probs = [obj / sum(probs) for obj in probs]
            ratings = [
                float(obj.token) if obj.token.isdigit() else 0 for obj in response
            ]
            # final score
            score = sum([a * b for a, b in zip(ratings, probs)])
        score = float(score)
        if score == 3:
            strongly_related += 1
        elif score == 2:
            realted += 1
        else:
            not_related += 1
        print(f"Paper path: {paper_path} Score: {score}")
        total += 1
    print(f"Strongly related: {strongly_related}, Related: {realted}, Not related: {not_related}, Total: {total}")

if __name__ == "__main__":
    
    # store all output into a output_file named output.txt
    parser = argparse.ArgumentParser(description='Run Biomni agent on datasets.')
    parser.add_argument('--dataset_path', type=str, required=True, help='Path to the dataset (with papers dirs).')
    parser.add_argument('--gt_insights_path', type=str, required=True, help='Path to the GT insights.')
    args = parser.parse_args()

    main(args.dataset_path, args.gt_insights_path)