import nbformat as nbf
import os
import re
import argparse

def run_convert2nb(base_code_dir, model_call="claude"):
    codes_dir = os.path.join(base_code_dir, f"insight_codes_py_{model_call}")
    ipynb_dir = os.path.join(base_code_dir, f"insight_codes_ipynb_{model_call}")
    os.makedirs(ipynb_dir, exist_ok=True)
    
    code_files = [f for f in os.listdir(codes_dir) if f.endswith('.py')]

    for code_file_ in code_files:
        with open(os.path.join(codes_dir, code_file_), "r") as f:
            code = f.read()

        # Split the script into blocks
        blocks = re.split(r"#\s*--- Code Block \d+ ---\s*", code)

        # Remove any empty leading block (before the first comment)
        if not blocks[0].strip():
            blocks = blocks[1:]

        # Create the Jupyter notebook object
        nb = nbf.v4.new_notebook()
        nb.cells = []

        # Add each code block as a new cell
        for i, block in enumerate(blocks, start=1):
            # Optional: add a Markdown cell with block title
            nb.cells.append(nbf.v4.new_markdown_cell(f"### Code Block {i}"))
            # Add the code block
            nb.cells.append(nbf.v4.new_code_cell(block.strip()))

        # Save the notebook
        with open(os.path.join(ipynb_dir, f"{code_file_.replace('.py', '.ipynb')}"), 'w') as f:
            nbf.write(nb, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", required=True)
    parser.add_argument("--model_call", type=str, default="claude", choices=["gpt", "claude"])
    args = parser.parse_args()
    
    
    paper_dirs = os.listdir(args.base_dir)
    for paper_dir in paper_dirs:
        run_convert2nb(os.path.join(args.base_dir, paper_dir), model_call=args.model_call)
        print(f"Converted {paper_dir} code to Jupyter notebooks with model call {args.model_call}")

