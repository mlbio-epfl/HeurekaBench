# HeurekaBench: A Benchmarking Framework for AI Co-scientist

`heurekabench` is a framework to create benchmarks with exploratory, open-ended research questions for experimental datasets for AI co-scientists. Each question in the benchmark is grounded in a scientific study and its corresponding code repository, and is created using a semi-automated pipeline that leverages multiple LLMs to extract insights and generate candidate workflows, which are then verified against reported findings. An instantiation of this framework `scheurekabench` for benchmarking AI co-scientists in the single-cell domain.

## Overview of the Framework
<p align="center">
  <img src="figs/framework.png" alt="Overview of the Framework" width="800"/>
</p>

The pipeline consists of two stages:   
- **(a) insight generation**: where candidate insights are extracted from scientific articles and semi-automatically validated  
- **(b) question generation**: where validated insights are reformulated as question-answer pairs   
- **(c) question solving**: where the agent autonomously designs and executes a multi-step analysis, producing a data-driven answer that is evaluated against published findings.   

## Using the Framework to create a benchmark
The first task is to create a `.env` file in the root directory of the project. An example file is provided in the [.env.example](.env.example) file. You can copy it and rename it to `.env`.  

Next, we demonstrate the use of `heurekabench` framework to create a benchmark for the single-cell domain, `scheurekabench`. The two stages of the pipeline are implemented in the `scheurekabench` folder and for more details, please refer to the [README](scheurekabench/README.md) file.

## Running AI Co-scientists on the benchmark
To evaluate, the agent is provided with the questions from the benchmark and has to autonomously design and execute a multi-step analysis to produce a data-driven answer that is evaluated against published findings. Currently, we adapt existing single-cell agents as AI Co-scientists to solve the tasks in the `scheurekabench` benchmark. More details on the agents and how to run them are provided in the [README](scheurekabench/README.md) file.

## Getting the single-cell datasets
All the single-cell datasets should be stored in the `scheurekabench/benchmark/scdata` folder. The single-cell datasets (`.h5ad`, `.txt`, `.csv`, etc.) are available [here](https://drive.google.com/drive/folders/1qRPW4P_Un0Pjm4Pbakvk1KhZdNiww22g?usp=sharing) in a compressed manner. Please follow the instructions below to download and extract the datasets:

You should have all of the following in the same directory (ideally at the root of the project):

- `scdata.part_[aa-af]`
- `scdata.tar.zst.sha256`

---

```bash
# Reassemble the archive
cat scdata.part_* > scdata.tar.zst 

# Verify the integrity of the archive
# Expected output: scdata.tar.zst: OK
sha256sum -c scdata.tar.zst.sha256

# Optional: Verify the integrity of the archive using zstd
zstd -t scdata.tar.zst

# Extract the datasets (will automatically extract to `scheurekabench/benchmark/scdata/`)
# You can check the size after extraction with `du -sh scheurekabench/benchmark/scdata/` which should be 44 GB
tar -I zstd -xf scdata.tar.zst

# Optional: Clean up the files
rm scdata.part_* scdata.tar.zst

# Mandatory: give read permissions to the `scheurekabench/benchmark/scdata/` folder to all users
chmod -R a+r scheurekabench/benchmark/scdata/
```