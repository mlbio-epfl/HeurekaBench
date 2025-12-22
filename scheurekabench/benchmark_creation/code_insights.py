import os, json, sys, argparse, time
import openai
import anthropic
from dotenv import load_dotenv
import nbformat

from prompts.code_describer import code_describer_prompt

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = {
    "claude-3-5-haiku-latest": 8192,
    "claude-opus-4-20250514": 16384,
    "claude-sonnet-4-20250514": 16384,
}

try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    def n_tokens(txt: str) -> int: return len(enc.encode(txt))
except ImportError:
    def n_tokens(txt: str) -> int: return len(txt) // 4

DEFAULT_MODEL = "gpt-4o"
MAX_PROMPT_TOKENS = 100000

def batch_files(file_list, max_tokens):
    batch, token_sum = [], 0
    num_paths = 0
    for path, code in file_list:
        code_block = f"### BEGIN {path}\n{code}\n### END {path}\n"
        t = n_tokens(code_block)
        if t > max_tokens:
            print(f"Skipping {path} (too large at {t} tokens)")
            continue
        if (token_sum + t > max_tokens or num_paths > 9) and batch:
            yield batch
            batch, token_sum, num_paths = [], 0, 0
        batch.append((path, code))
        token_sum += t
        num_paths += 1
    if batch:
        yield batch

def describe_batch(batch, model_call="gpt"):
    merged_source = "".join(
        f"### BEGIN {path}\n{code}\n### END {path}\n" for path, code in batch
    )
    full_prompt = code_describer_prompt + "\n\n" + merged_source

    if model_call == "gpt":
        try:
            response = openai.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.3,
                max_tokens=8192,
                timeout=300,
                response_format={"type": "json_object"},
            )
            content = getattr(response.choices[0].message, "content", None)
        except Exception as e:
            print("OpenAI API call failed:", e)
            return {}

    elif model_call == "claude":
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        try:
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS[CLAUDE_MODEL],
                temperature=0.3,
                messages=[{"role": "user", "content": full_prompt}]
            )
            content = response.content[0].text
        except Exception as e:
            print("Claude API call failed:", e)
            return {}

    else:
        raise ValueError(f"Unsupported model_call: {model_call}")

    cleaned = content.strip().lstrip("```json").lstrip("```").strip('`\n ')
    try:
        return json.loads(cleaned or "{}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}\nPartial response:\n{cleaned[:500]}...")
        return {}

def process_single_paper_dir(paper_dir, model_call):
    code_path = os.path.join(paper_dir, "code")
    output_file = os.path.join(paper_dir, f"code_insights_{model_call}.json")

    if not os.path.exists(code_path):
        print(f"No code/ folder in {paper_dir}. Skipping.")
        return

    files = []
    for root, _, fs in os.walk(code_path):
        for f in fs:
            full = os.path.join(root, f)
            rel_path = os.path.relpath(full, code_path)
            try:
                if f.endswith((".py", ".R", ".pl", ".Rmd", ".rmd")):
                    with open(full, "r", encoding="utf-8") as fh:
                        files.append((rel_path, fh.read()))
                elif f.endswith(".ipynb"):
                    with open(full, "r", encoding="utf-8") as fh:
                        nb = nbformat.read(fh, as_version=4)
                        code_cells = [cell.source for cell in nb.cells if cell.cell_type == "code"]
                        if code_cells:
                            files.append((rel_path, "\n\n".join(code_cells)))
            except Exception as e:
                print(f"Could not read {full}: {e}")

    if not files:
        print(f"No code files found in {code_path}. Skipping.")
        return

    descriptions = {}
    for i, batch in enumerate(batch_files(files, MAX_PROMPT_TOKENS - 8192), 1):
        print(f"{os.path.basename(paper_dir)}: Batch {i} of {len(files)} files")
        desc = describe_batch(batch, model_call=model_call)
        descriptions.update(desc)
        time.sleep(1)

    with open(output_file, "w", encoding="utf-8") as fp:
        json.dump(descriptions, fp, indent=2)
    print(f"Saved to {output_file}\n")

def main(base_dir, model_call):
    if model_call == "gpt" and not OPENAI_API_KEY:
        sys.exit("ERROR: Set the OPENAI_API_KEY environment variable.")
    if model_call == "claude" and not CLAUDE_API_KEY:
        sys.exit("ERROR: Set the CLAUDE_API_KEY environment variable.")

    openai.api_key = OPENAI_API_KEY

    paper_dirs = sorted(
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("paper") and not os.path.exists(os.path.join(base_dir, d, f"code_insights_{model_call}.json"))
    )


    print(f"Found {len(paper_dirs)} paper directories in {base_dir}.")

    for paper_dir in paper_dirs:
        process_single_paper_dir(paper_dir, model_call)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", type=str, required=True, help="Directory with paper1/, paper2/, ...")
    parser.add_argument("--model_call", type=str, default="claude", choices=["gpt", "claude"])
    args = parser.parse_args()

    main(args.base_dir, args.model_call)
