# oe_initial_prompt = """Task: Analyze the provided single-cell dataset and answer the biology question.

# Input Data:
# {data_path}

# Question:
# {question}

# Output Format:
# Return the summary of an answer wrapped inside XML-style tags <solution> and </solution>.
# """


oe_initial_prompt = """Task: Analyze the provided single-cell dataset and answer the biology question.

Input Data:
{data_path}

Question:
{question}

Output Format:
Return the summary of an answer wrapped inside XML-style tags <solution> and </solution>.

Guidelines for the output format:
- Base the answer strictly on the results derived from the dataset.  
- Provide a fact-based summary (not a narrative or manuscript-style report).  
- Do not use extra formatting such as bullet points or section headers.  
- Include all key findings that directly address the question, emphasizing those most relevant to the answer.  
"""