oe_initial_prompt = """You are a biology expert answering questions related to transcriptomics.

Task: Answer the biology question.

Question:
{question}

Output Format:
Return the summary of an answer wrapped inside XML-style tags <solution> and </solution>.

Guidelines for the output format:
- Provide a fact-based summary (not a narrative or manuscript-style report).  
- Do not use extra formatting such as bullet points or section headers.  
- Include all key findings that directly address the question, emphasizing those most relevant to the answer.  
"""