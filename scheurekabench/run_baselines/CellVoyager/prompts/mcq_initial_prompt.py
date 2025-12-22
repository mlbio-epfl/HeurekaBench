mcq_initial_prompt = """Task: Analyze the provided single-cell dataset and answer the biology question by selecting all correct options.

Input Data:
{data_path}

Question:
{question}

Answer Choices:
{answer_choices}

Output Format:
Return the selected options as a comma-separated list of letters wrapped inside XML-style tags <solution> and </solution>.
For example: <solution>A,C</solution>
"""