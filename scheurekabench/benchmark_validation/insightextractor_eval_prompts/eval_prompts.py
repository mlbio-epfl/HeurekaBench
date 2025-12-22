def get_insightextractor_eval_prompt(method="basic"):
    if method == "basic":
        geval_template, system_template = (
            INSIGHT_EXTRACTOR_EVAL_BASIC_TEMPLATE,
            INSIGHT_EXTRACTOR_EVAL_BASIC_SYSTEM_MESSAGE,
        )
    return geval_template, system_template

INSIGHT_EXTRACTOR_EVAL_BASIC_TEMPLATE = """
You will be given a list of LLM-generated insights and a single scientist-derived insight. 
Your task is to assign a single score according to the following rules.

Scoring (Relatedness 1-3, integers only):
- 3 (strongly related): At least one LLM insight is strongly related to the scientist-derived insight.  
- 2 (related): No strongly related insights, but at least one is related.  
- 1 (unrelated): All LLM insights are unrelated.  

LLM-derived insights: 
{llm_insights}

Scientist-derived insight: 
{scientist_insight}


Output Format:
- Output the numerical rating wrapped in <rating></rating> tags.
- After the rating, output an explanation wrapped in <explanation></explanation> tags.
- Do not include extra text outside these tags.
- Example:
<rating>2</rating>
"""

INSIGHT_EXTRACTOR_EVAL_BASIC_SYSTEM_MESSAGE = """You are an expert evaluating conceptual alignment between AI-generated insights and a scientist-derived insight."""