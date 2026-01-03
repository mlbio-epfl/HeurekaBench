# Using the HeurekaBench Framework to create a benchmark

First setup a collection of research papers and their corresponding code repositories. Each paper should be in a separate folder with the following structure:
```
base_dir/
  |-paperX/ (X is the paper number)
    |-  paper.pdf
    |-  code/ (can be obtained with `git clone <repository_url>` or manually downloaded)
    |-  data/ (contains single-cell datasets and additional files, e.g., .txt, .csv, etc.)
```

All prompts are already setup in [benchmark_creation/prompts](benchmark_creation/prompts) folder. 
> **Optionally:** but it is recommended to perform minor edits to the prompts and replace current single-cell domain few shot-examples with your own domain. This is optional because these examples primarily explain the LLM what the outputs should look like. 

Next, create a conda environment with the required packages and `.env` file (a sample file is provided in the [.env.example](https://github.com/mlbio-epfl/HeurekaBench/tree/main/.env.example) file).

```bash
conda create -n heurekabench python=3.12
conda activate heurekabench
pip install python-dotenv PyMuPDF openai anthropic nbformat
```


## Step 1a: Insight Extraction (InsightExtractor)
The first stage of the framework **extracts insights from the research papers**. Use the following command:

```bash 
python benchmark_creation/code_insights.py \
    --base_dir <path_to_base_dir> \
    --model_call <model_call: gpt|claude>
```
The insights will be saved at `paperX/insights_paragraphs_<model_call>.txt`.

## Step 1b: Code Description Generation (CodeDescriber)
Next, we **describe the code files** in the `paperX/code` folder with natural language. This is a crucial step to help the LLM understand the code and generate the multi-step code to support the insights later. Use the following command:

```bash
python benchmark_creation/code_insights.py \
    --base_dir <path_to_base_dir> \
    --model_call <model_call: gpt|claude>
```
The code descriptions will be saved at `paperX/code_insights_<model_call>.json`.

## Step 1c: Code-Insight Matching (CodeMatcher) and Multi-step Code Generation (CodeGenerator)
The next step is to **match the insights** with the code files and **generate the multi-step code** to support the insights. 

```bash
python benchmark_creation/match_insights.py \
    --base_dir <path_to_base_dir> \
    --model_call <model_call: gpt|claude>
```
The multi-step code will be saved at `paperX/final_insight_code_mapping_<model_call>.json`.  

> **Note:** If the code is not generated for some insights correctly (e.g., relevant code files not matched), you can re-run the above script or ignore those insights and continue with the next step.

The above command will generate the multi-step code to support the insights in `.json` format. To convert the `.json` file to a `.ipynb` file (and subsequently easier manual verification), use the following commands sequentially. `--output_root` can be same as `--base_dir` but you can specify a different path to save the multi-step code in `.ipynb` format.

```bash
python benchmark_creation/utils/combine_codes.py --base_dir <path_to_base_dir> --output_root <path_to_output_root>  
python benchmark_creation/utils/convert_to_nb.py --base_dir <path_to_base_dir>
```
> **Note:** During the manual validation process, create an `insights.json` file (similar to final benchmark, e.g., `scheurekabench/benchmark/oeq.json` without the questions) which contains the verified insights along with all the data paths (single-cell and additional files required during verification) paths.  

## Step 2: Question Generation
After the verification of the multi-step code, the verified insights are used to **generate the questions**. Use the following command:

```bash
python benchmark_creation/insights_to_questions.py \
    --insight_json_path <path_to_insight_json_file> \
    --model_call <model_call: gpt|claude> \
    --qtype <question_type: mcq|oe>
```
The questions will be saved in the `<qtype>_questions.json` alongside the `insights.json` file location.  

> **Note:** After the question generation steps, one can remove (i) automatically detected easy questions that are answered correctly by strong closed-source LLMs (refer to main README on how to run LLMs without access to agent environment [here](https://github.com/mlbio-epfl/HeurekaBench#running-llms-without-access-to-agent-environment)) (ii) manually, the hallucinated, duplicated, or questions from non-validated parts of the insights.


**That's it!** You have now created a benchmark for your scientific domain to evaluate your AI agent as an AI Co-scientist. :tada: