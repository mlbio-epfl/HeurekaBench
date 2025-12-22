def get_g_eval_prompt(method="basic"):
    if method == "basic":
        geval_template, system_template = (
            G_EVAL_BASIC_TEMPLATE,
            G_EVAL_BASIC_SYSTEM_MESSAGE,
        )
        
    return geval_template, system_template

G_EVAL_BASIC_TEMPLATE = """
You are grading a PhD student's answer to an open-ended research question about a single-cell biology dataset. 
The task requires analysis of the dataset to derive the answer to the question. 
You will be given the student's answer and the ground-truth (GT) answer.

**Evaluation Steps:**
1) Extract atomic facts from the GT and label them F1..Fn.
   An atomic fact is a claim that can be objectively verified (including but not limited to: cell type/condition, direction/magnitude of change, gene/pathway names, statistical evidence, method/application, conclusion).
2) For each Fi, classify the student's coverage as:
   - PRESENT: fact included with the same meaning AND explicitly tied to dataset-derived quantitative/statistical outputs or cluster/subtype identifiers. PRESENT requires evidence that the student directly engaged with the dataset-defined labels.
   - PARTIAL: This group includes:
         - Facts with the correct meaning but supported only by descriptive biology or lists of plausible options (e.g., cell type names, marker/pathway lists), without dataset-level numbers or identifiers.
         - Facts whose support is vague or hedged, using terms such as "e.g.," "seems," "maybe," "likely," "generally," "typically," "usually," "for example," or similar language. 
         - Facts that appear to rely solely on general biological knowledge or recall, without direct reference to the dataset.
         - Answers that list multiple plausible options (e.g., marker genes, pathways, or cell types) without presenting dataset-based evidence.
   - MISSING: fact is not mentioned.
   - INCORRECT: wrong fact or fact that is contradictory to some GT fact.
3) Identify contradictions: any statement that is in direct conflict with the GT (including but not limited to: opposite direction, wrong cell type/condition).
   - Contradictions should only be judged relative to GT, not relative to biological knowledge outside GT.
   - Facts marked as MISSING do not count into contradictions.
   - Omitting details, partial coverage, or failing to mention context is not a contradiction. It may affect coverage (PARTIAL/MISSING) but does not count as contradictory.
4) Count number of GT facts that are PRESENT, PARTIAL, MISSING, or INCORRECT. Evaluate only against parts of the answer that address the GT facts. 
5) Review the coverage labels for all GT facts and determine the overall correctness score (1-5) based on the scoring rubric below.
6) Presence of additional information that is not part of GT facts, but does not contradict GT, DOES NOT AFFECT THE SCORE. Calculate the score solely based on the GT facts and their coverage labels.

   
**Scoring (Correctness 1-5, integers only):**
- 5: ALL GT facts are marked as PRESENT. No facts are marked as MISSING or INCORRECT.
      No contradictions of GT facts.
- 4: MOST or ALL GT facts are marked as PRESENT. 
      Detailed, dataset-grounded analysis is valid even if it does not repeat the GT fact's broader/general terms, as long as it conveys the same underlying fact.
      Facts labeled as MISSING are allowed. Facts labeled as INCORRECT are not allowed.
- 3: SOME GT facts (but NOT ALL) are marked as PRESENT. AT LEAST ONE GT fact is marked as PARTIAL or MISSING.
      Minor contradictions of GT facts are allowed.
      Facts labeled as MISSING are allowed.
- 2: NO GT facts are marked as PRESENT; SOME are PARTIAL.
      Student includes broad or generic options (e.g., list of plausable genes with no explanations), which seems like recall of biological knowledge and not dataset evidence.
      Minor contradictions of GT facts are allowed.
- 1: ALL GT facts are marked as MISSING; MOST GT facts are marked INCORRECT; there are major contradictions of GT; the student explicitly states inability to answer / no data available.

**General Rules:**
- Grade only against the GT answer; ignore outside knowledge.
- Focus only on parts addressing GT facts; ignore unrelated detail unless contradictory. 
- It does not matter if GT facts are not emphasized or the main focus - only matters whether they are present in the student's answer and not vague.
- Style, length, or phrasing differences (including paraphrases/synonyms) do not matter as long as GT facts are covered with dataset grounding.
- Dataset grounding (required for PRESENT): explicit quantitative/statistical evidence or dataset identifiers (e.g., percentages, fold changes, p-values, cluster IDs, enrichment scores).
- Assess additional information, not related to GT fact: PENALIZE ONLY IF the additional information is contradictory to the GT.
- Extra details related to the GT fact (e.g., subtypes, fold changes, statistics) are valid if they are dataset-based and consistent with the GT. Such details should not “obscure” correctness score as long as they are neither contradictory nor vague. However, vague or unsupported details—especially those resembling general biological recall (e.g., lists of plausible genes, cell types, or pathways)—should downgrade the related GT fact from PRESENT to PARTIAL.
- If details tied to the GT fact rely on vague or hedging language (e.g., “e.g.,” “likely,” “for example,”), or involve listing many plausible options (e.g., genes, pathways, cell types), the related GT fact should likewise be downgraded from PRESENT to PARTIAL.
- If the GT fact appears only as part of an extensive lists (including but not limited to: lists of plausible genes, pathways, or cell types), without dataset-specific grounding, the answer should be downgraded from PRESENT to PARTIAL. This applies even if the GT fact is technically included, since its support is obscured by recall-like listing rather than dataset evidence.
- All GT facts are treated equally. No fact is inherently more important than others.

Provided Answer:
{answer}

Ground Truth Answer (GT):
{gt_answer}

Output Format:
- Output the numerical rating wrapped in <rating></rating> tags.
- Do not include extra text outside these tags.
- Example:
<rating>3</rating>
Your Response:
"""

G_EVAL_BASIC_SYSTEM_MESSAGE = """You are a full professor in single-cell biology evaluating your PhD student's responses to questions."""
