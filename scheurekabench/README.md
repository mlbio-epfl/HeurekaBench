# Steps to create a benchmark with the HeurekaBench framework

Below, we provide an instantiation of the HeurekaBench framework for the single-cell biology domain, sc-HeurekaBench. These steps can be repeated for other scientific domains to create corresponding new benchmarks.

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
The first stage of the framework extracts insights from the research papers. To run insight extraction, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/papers`). The insights will be saved in the `paperX/insights_paragraphs_<model_call>.txt` file. Default model is `gpt` but you can specify `claude` by adding `--model_call claude` to the command.

```bash 
python benchmark_creation/code_insights.py --base_dir <path_to_base_dir>
```

## Code Description Generation (CodeDescriber)
Next, we describe the code files in the `paperX/code` folder. To run code description generation, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/papers`). The code descriptions will be saved in the `paperX/code_insights_<model_call>.json` file. Default model is `claude` but you can specify `gpt` by adding `--model_call gpt` to the command.

```bash
python benchmark_creation/code_insights.py --base_dir <path_to_base_dir>
```

## Code Insight Matching (CodeMatcher) and Multi-step Code Generation (CodeGenerator)
The next step is to match the insights with the code files and generate the multi-step code to support the insights. To run code insight matching and multi-step code generation, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/papers`). The multi-step code will be saved in the `paperX/final_insight_code_mapping_<model_call>.json` file. Default model is `claude` but you can specify `gpt` by adding `--model_call gpt` to the command.

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

Next, to run question generation, use the following command. In the following command, `base_dir` is the path to the base directory containing the paper folders (e.g., `benchmark_creation/papers`). The questions will be saved in the `paperX/questions_<model_call>.json` file. Default model is `claude` but you can specify `gpt` by adding `--model_call gpt` to the command. After the question generation steps, one can remove (i) easy questions that are answered correctly by baseline closed-source LLMs (ii) the hallucinated, duplicated, or questions from non-validated parts of the insights.

```bash
python benchmark_creation/insights_to_questions.py --insight_json_path <path_to_insight_json_file>
```

> **Note:** All the relevant prompts are available in the [`benchmark_creation/prompts`](benchmark_creation/prompts) folder.

## Some additional pointers to adapt the HeurekaBench framework

The above steps can have straightforward adaptation for other scientific domains by making minimal changes as follows:
 
- To adapt the prompts in the [`benchmark_creation/prompts`](benchmark_creation/prompts) folder, the required changes include the `domain names` and a `few-shot examples`. Such examples can be generated by running the modules without any examples first, while all other instructions are present. Then, some outputs can be selected to include in the prompt. Note that these modules can be run without examples; however, in practice, since LLMs are the core of these modules, it is recommended to provide a few-shot in-domain examples.  
- The framework needs human experts with enough experience working in the domain to understand and analyze the outputs of automated modules. As a potential future work, automating this step **reliably** would convert the semi-automated HeurekaBench into an automated framework.