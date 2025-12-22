"""
To use this script, you need to first clone the code InsightBench from the following repository:
git clone https://github.com/ServiceNow/insight-bench.git
"""
import json
import hashlib
from uuid import uuid4
from pathlib import Path

insights = {}
code_dir = Path("paper1/code")
code_dir.mkdir(exist_ok=True)

index_path = code_dir / "_content_index.json"
if index_path.exists():
    content_index = json.load(open(index_path))
else:
    content_index = {}

used_uuids = set()

def unique_uuid():
    while True:
        uid = uuid4().hex[:12]
        if uid not in used_uuids:
            used_uuids.add(uid)
            return uid

def normalize_code(text: str) -> str:
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]

    normalized = []
    prev_blank = False
    for ln in lines:
        is_blank = (ln.strip() == "")
        if is_blank and prev_blank:
            continue
        normalized.append(ln)
        prev_blank = is_blank
    return "\n".join(normalized).strip() + "\n"

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_or_create_code_file(code_text: str) -> str:
    norm = normalize_code(code_text)
    h = content_hash(norm)
    if h in content_index:
        return content_index[h]["filename"]

    uid = unique_uuid()
    fname = f"code_script_{uid}.py"
    fpath = code_dir / fname
    with open(fpath, "x") as f:
        f.write(norm)
    content_index[h] = {"uid": uid, "filename": fname}
    json.dump(content_index, open(index_path, "w"), indent=2)
    return fname


for flag in range(1, 51):
    insight_dict = json.load(open(f'insight-bench/data/notebooks/flag-{flag}.json'))

    our_insight = {
        "how": insight_dict['metadata']["role"] + " ; " + insight_dict['metadata']["category"],
        "relevant": insight_dict['metadata']["dataset_description"],
    }

    code_scripts = []
    summary = f"Goal: {insight_dict['metadata']['goal']}. Insights: "
    for isl in insight_dict["insight_list"]:
        summary += isl["insight"] + " ; "
        code_scripts.append(
            "import os\n"
            "import json\n"
            "import argparse\n"
            "import requests\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "from pandas import date_range\n" + isl["code"]
        )

    our_insight["summary"] = summary
    our_insight["num_steps"] = len(code_scripts)

    gt_files = []
    for cs in code_scripts:
        fname = get_or_create_code_file(cs)
        gt_files.append(fname)

    our_insight["gt_files"] = ";".join(gt_files)
    insights[f"Insight #{flag}"] = our_insight

    if len(used_uuids) > 200:
        print("Reached 200 code files, stopping.")
        print("Current insight number: ", flag)
        break

json.dump(insights, open("insights.json", "w"), indent=4)

