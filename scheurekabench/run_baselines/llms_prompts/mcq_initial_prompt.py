mcq_initial_prompt = """You are a biology expert answering multiple-choice questions related to transcriptomics.

Task: Answer the biology question by selecting all correct options.

Question:
{question}

Answer Choices:
{answer_choices}

Output Format:
Return the selected options as a comma-separated list of letters wrapped inside XML-style tags <solution> and </solution>.
For example: <solution>A,C</solution>
"""