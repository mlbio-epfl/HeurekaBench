import os
from pathlib import Path

def generate_file_tree(root_dir: str, prefix: str = "") -> str:
    relevant_exts = {'.csv', '.json', '.txt'}
    entries = sorted(Path(root_dir).iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    tree_str = ""

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "

        if entry.is_file():
            if entry.suffix.lower() in relevant_exts:
                tree_str += f"{prefix}{connector}{entry.name}\n"
        elif entry.is_dir():
            tree_str += f"{prefix}{connector}{entry.name}/\n"
            extension = "    " if is_last else "│   "
            tree_str += generate_file_tree(entry, prefix + extension)

    return tree_str


def inject_tree_into_prompt(prompt_file: str, root_dir: str, output_file: str):
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_text = f.read()

    file_tree_text = generate_file_tree(Path(root_dir))
    file_tree_block = f"""
**Directory Tree of Supporting Data**:
If a code snippet references a file path (e.g., data/sample.csv), you must resolve it based on the **actual structure of the project directory**. This ensures that the generated code correctly accesses the intended files when executed.

For instance, if a script references data/sample.csv, but the file is actually located at data/samples/sample.csv, you should update the path accordingly. **Always reference file paths relative to the root directory of the codebase.**

To assist you, the directory structure (starting from the root) for relevant data files is provided below. Use it to verify and correctly resolve all file references in the code:
```text
{file_tree_text.strip()}
```
    """.strip()

    if "{tree_files}" not in prompt_text:
        raise ValueError("The prompt file must contain the '{tree_files}' placeholder.")

    new_prompt = prompt_text.replace("{tree_files}", file_tree_block)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_prompt)

    print(f"File tree injected into prompt and saved to {output_file}")

def inject_tree_into_prompt_text(prompt_text: str, root_dir: str):
    file_tree_text = generate_file_tree(Path(root_dir))
    file_tree_block = f"""
**Directory Tree of Supporting Data**:
If a code snippet references a file path (e.g., data/sample.csv), you must resolve it based on the **actual structure of the project directory**. This ensures that the generated code correctly accesses the intended files when executed.

For instance, if a script references data/sample.csv, but the file is actually located at data/samples/sample.csv, you should update the path accordingly. **Always reference file paths relative to the root directory of the codebase.**

To assist you, the directory structure (starting from the root) for relevant data files is provided below. Use it to verify and correctly resolve all file references in the code:
```text
{file_tree_text.strip()}
```
    """.strip()

    if "{tree_files}" not in prompt_text:
        raise ValueError("The prompt file must contain the '{tree_files}' placeholder.")

    new_prompt = prompt_text.replace("{tree_files}", file_tree_block)
    return new_prompt.strip()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inject file tree into matcher_insights_prompt.")
    parser.add_argument("--prompt", required=True, help="Path to the original prompt file")
    parser.add_argument("--dir", required=True, help="Root directory of the codebase/data")
    parser.add_argument("--output", default="matcher_insights_prompt_filled.py", help="Output file with file tree injected")

    args = parser.parse_args()
    inject_tree_into_prompt(args.prompt, args.dir, args.output)
