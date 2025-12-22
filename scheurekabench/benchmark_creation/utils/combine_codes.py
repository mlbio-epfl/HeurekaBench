import os
import json
import re
import argparse

def run_combining_codes(input_root, output_root, model_call: str = "gpt"):
    paper_name = os.path.basename(input_root)

    input_file = os.path.join(input_root, f"final_insight_code_mapping_{model_call}.json")
    
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist. Skipping {paper_name}.")
        return

    with open(input_file, 'r') as f:
        insights = json.load(f)

    def clean_code(code_block: str) -> str:
        """Remove <execute> tags and surrounding whitespace"""
        cleaned = re.sub(r'^<execute>\s*', '', code_block)
        cleaned = re.sub(r'\s*</execute>\s*$', '', cleaned)
        return cleaned.strip()

    for i, (insight_title, insight_data) in enumerate(insights.items(), start=1):
        insight_dir_name = f"insight_codes_py_{model_call}"
        insight_code = f"insight_{i:02d}"
        insight_dir = os.path.join(output_root, insight_dir_name)
        os.makedirs(insight_dir, exist_ok=True)

        file_path = os.path.join(insight_dir, f"{insight_code}.py")

        with open(file_path, 'w') as f:
            f.write(f"# Insight {i}: {insight_title}\n")
            f.write(f"# Summary: {insight_data['summary']}\n\n")

            for j, block in enumerate(insight_data.get('code_blocks', []), start=1):
                cleaned_code = clean_code(block['code'])
                indented_code = "\n".join("    " + line for line in cleaned_code.splitlines())
                f.write(f"# --- Code Block {j} ---\n")
                f.write("try:\n")
                f.write(indented_code + "\n")
                f.write(f"except Exception as e:\n")
                f.write(f"    print(f\" Failed in Code Block {j} of Insight {i}: {{e}}\")\n\n")

        print(f" Wrote {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", type=str, required=True)
    parser.add_argument("--output_root", type=str, required=True)

    parser.add_argument("--model_call", type=str, default="claude", choices=["gpt", "claude"])
    args = parser.parse_args()

    paper_dirs = [os.path.join(args.base_dir, d) for d in os.listdir(args.base_dir) if os.path.isdir(os.path.join(args.base_dir, d))]
    for paper_dir in paper_dirs:
        output_root_ = os.path.join(args.output_root, os.path.basename(paper_dir))
        run_combining_codes(paper_dir, output_root_, model_call=args.model_call)