import os
import re
import json
import argparse

def process_agent_outputs(root_dir):
    results = []

    # regex pattern to match agent answer
    block_pattern = re.compile(
        r"=+ Ai Message =+.*?<solution>.*?</solution>",
        re.DOTALL
    )

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith("_output.txt"):
                filepath = os.path.join(dirpath, fname)

                with open(filepath, "r") as f:
                    text = f.read()

                # find all AI message blocks
                blocks = re.findall(block_pattern, text)
                if blocks:
                    # take only the last block
                    last_block = blocks[-1]

                    # extract solution
                    solution_pattern = re.compile(r"<solution>(?:(?!<solution>).)*?</solution>", re.DOTALL)
                    solution_blocks = re.findall(solution_pattern, last_block)
                    if solution_blocks:
                        last_solution_block = solution_blocks[-1]
                        answer = last_solution_block.lstrip("<solution>").rstrip("</solution>").strip()

                    # metadata from path
                    parts = filepath.split(os.sep)
                    paper = next((p for p in parts if "paper" in p.lower()), None)
                    insight = next((p for p in parts if "insight" in p.lower()), None)
                    question = fname.replace("_output.txt", "")

                    results.append({
                        "paper": paper,
                        "insight": insight,
                        "question": question,
                        "answer": answer
                    })

    output_path = os.path.join(root_dir, "processed_results.json")
    nested = {}
    for item in results:
        paper = item['paper']
        insight = item['insight']
        question = item['question']
        answer = item['answer']
        
        nested.setdefault(paper, {})
        nested[paper].setdefault(insight, {})
        nested[paper][insight][question] = answer

    # order papers alphabetically
    nested = dict(sorted(nested.items()))

    # save to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nested, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process AI agent outputs.")
    parser.add_argument("--root_dir", type=str, help="Root directory to scan for output files.")
    args = parser.parse_args()
    process_agent_outputs(args.root_dir)