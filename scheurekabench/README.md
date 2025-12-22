# Using the Framework to create a benchmark (`scheurekabench`)

We first recommend to setup the collection of research papers and their corresponding code repositories. Each paper should be in a separate folder with the following structure:
```
paperX/ (X is the paper number)
  |-  paper.pdf
  |-  code/ (can be obtained with `git clone <repository_url>` or manually downloaded)
  |-  data/ (contains single-cell datasets and additional files, e.g., .txt, .csv, etc.)
```

Next, create a conda environment with the required packages. If you identify some packages missing, please create a pull request to add them and we will update the following instructions accordingly.

```bash
conda create -n heurekabench python=3.12
conda activate heurekabench
pip install python-dotenv PyMuPDF openai anthropic nbformat
```

## Insight Extraction (InsightExtractor)
The first stage of the framework extracts insights from the research papers. To run insight extraction, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/sample_papers`). The insights will be saved in the `paperX/insights_paragraphs_<model_call>.txt` file. Default model is `gpt` but you can specify `claude` by adding `--model_call claude` to the command.

```bash 
python benchmark_creation/code_insights.py --base_dir <path_to_base_dir>
```

## Code Description Generation (CodeDescriber)
Next, we describe the code files in the `paperX/code` folder. To run code description generation, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/sample_papers`). The code descriptions will be saved in the `paperX/code_insights_<model_call>.json` file. Default model is `claude` but you can specify `gpt` by adding `--model_call gpt` to the command.

```bash
python benchmark_creation/code_insights.py --base_dir <path_to_base_dir>
```

## Code Insight Matching (CodeMatcher) and Multi-step Code Generation (CodeGenerator)
The next step is to match the insights with the code files and generate the multi-step code to support the insights. To run code insight matching and multi-step code generation, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/sample_papers`). The multi-step code will be saved in the `paperX/final_insight_code_mapping_<model_call>.json` file. Default model is `claude` but you can specify `gpt` by adding `--model_call gpt` to the command.

```bash
python benchmark_creation/match_insights.py --base_dir <path_to_base_dir>
```

If the code is not generated for some insights correctly (e.g., relevant code files not matched), you can re-run the above script or ignore those insights and continue with the next step.

The above command will generate the multi-step code to support the insights in `.json` format. To convert the `.json` file to a `.ipynb` file (and easier manual verification), use the following commands sequentially. `--output_root` can be same as `--base_dir` but you can specify a different path to save the multi-step code in `.ipynb` format.

```bash
python benchmark_creation/utils/combine_codes.py --base_dir <path_to_base_dir> --output_root <path_to_output_root>
python benchmark_creation/utils/convert_to_nb.py --base_dir <path_to_base_dir>
```

## Question Generation
After the manual verification of the multi-step code, the verified insights are used to generate the questions. During the manual validation process, create an `insights.json` file which contains the verified insights along with all the data (single-cell and additional files required during verification) paths.  

Next, to run question generation, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/sample_papers`). The questions will be saved in the `paperX/questions_<model_call>.json` file. Default model is `claude` but you can specify `gpt` by adding `--model_call gpt` to the command. After the question generation steps, one can remove (i) easy questions that are answered correctly by baseline closed-source LLMs (ii) the hallucinated, duplicated, or questions from non-validated parts of the insights.

```bash
python benchmark_creation/insights_to_questions.py --insight_json_path <path_to_insight_json_file>
```

> **Note:** All the relevant prompts are available in the [`benchmark_creation/prompts`](benchmark_creation/prompts) folder.

# `scheurekabench` details

The questions along with the single-cell datasets are stored in the [benchmark](benchmark) folder. The content and their descriptions are as follows:
```
benchmark/
  |- scdata (data folder with all the single-cell datasets and additional files, e.g., .txt, .csv, etc.)
  |- mcq_lite.json (multiple-choice questions, lite-version for computationally expensive agents)
  |- mcq.json (multiple-choice questions, full-version)
  |- mcq_tu.json (multiple-choice questions that likely require specific tool usage)
  |- oeq_lite.json (open-ended questions, lite-version)
  |- oeq.json (open-ended questions, full-version)
  |- oeq_tu.json (open-ended questions that likely require specific tool usage)
```

# Running AI Co-scientists on the `scheurekabench`
> **Note:** The paths in the datasets should contain the absolute paths otherwise the agent sometimes fails to find the data files if it is relative paths. We recommend to append absolute path to the `data` keys in `scheurekabench/benchmark/oeq.json` and `scheurekabench/benchmark/mcq.json` files.

### Running LLMs without access to agent environment
To run open-sourceLLMs without access to an agent environment, you can use the following command. To run closed-source LLMs, you can use the same command but replace `run_open_llms.py` with `run_closed_llms.py`.

```bash
python run_baselines/run_open_llms.py \
    --dataset_json_path <path_to_dataset_json_file> \
    --output_dir <path_to_output_dir> \
    --llm_name <LLM_name> \
    --q_type <question_type: mcq|oe>
```
### Running CellVoyager baseline
To run CellVoyager baseline, you can use the following command:
```bash
cd run_baselines/CellVoyager
python run_cellvoyager.py \
    --dataset_json_path <path_to_dataset_json_file> \
    --output_dir <path_to_output_dir> \
    --cellvoyager_llm claude-sonnet-4-20250514 \
    --q_type <question_type: mcq|oe>
```

## Running Biomni with Different Models
> **Note:** We provide the adaptation of Biomni version 0.0.6 for the following experiments. The original Biomni repository is available at [here](https://github.com/snap-stanford/Biomni) and newer versions can be merged appropriately.

### Running Closed-Source LLMs

To run Biomni with closed-source LLMs, you can use the following command:

```bash
python run_biomni/run_biomni.py \
    --dataset_json <path_to_dataset_json_file> \
    --biomni_llm <LLM_name: claude-sonnet-4-20250514|gpt-4o> \
    --q_type <question_type: mcq|oe> \
    --output_dir <path_to_output_dir>
```

### Running Open-Source LLMs

> **Note:** It is recommended to create a new conda environment with the required packages to serve with vLLM in the following manner (to avoid potential conflicts with other packages). If there are some packages that are missing when serving, please create a pull request to add them and we will update the following instructions accordingly.
```bash
conda create -n vllm-serve python=3.11.13
conda activate vllm-serve
pip install vllm=0.11.0
```

First, start a vLLM server with the desired LLM (e.g., to serve `openai/gpt-oss-120b` with 4 GPUs):

```bash
vllm serve openai/gpt-oss-120b \
  --port 8000 \
  --tensor-parallel-size 4
```
Before running Biomni, we have to set `biomni_e1` environment following the official instructions [here](https://github.com/snap-stanford/Biomni/tree/main/biomni_env). Then `conda activate biomni_e1` to activate the environment.

Followed by this, use the following command to run Biomni with the open-source LLM (with the correct `--biomni_llm` and `--biomni_base_url`):

```bash
python run_biomni/run_biomni.py \
    --dataset_json <path_to_dataset_json_file> \
    --output_dir <path_to_output_dir> \
    --biomni_llm <LLM_name: openai/gpt-oss-120b> \
    --biomni_source Custom \
    --biomni_base_url http://0.0.0.0:8000/v1 \
    --q_type <question_type: mcq|oe>
    --temperature <temperature>
```

# Evaluation Workflow

Once the agent has produced outputs, we first extract the solutions from the agent outputs with the following command:
```bash
python extract_agent_answer.py --root_dir <path_to_agent_outputs>
```
> **Note:** Some agent runs might have not produced appropriate outputs (e.g., <solution></solution> tags do not contain the solution because the agent stopped prematurely, or segmentation fault occurred, no response between <solution> and </solution> tags, etc.). In such cases, it is recommended to re-run the agent by deleting the output files for those questions, otherwise GPT-4o judge will not assign meaningful scores to such outputs.

After extracting the solutions (which will be located in the `<root_dir>/processed_results.json` file), we can run the evaluation with the following command:

```bash
python evaluate_agent_answer.py \
    --dataset_json <path_to_dataset_json_file> \
    --results_json <path_to_processed_results.json> \
    --q_type <question_type: mcq|oe>
```

There is an option to use batch processing for open-ended question evaluation (to batch the requests to the GPT API). To use batch processing, add the `--batch_oe_judge` flag to the command.

Finally, the evaluation results and associated files will be found within the `<root_dir>` directory.
