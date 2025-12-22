insight2question_prompt_text = """
I am designing assignments for my PhD students on single-cell omics data. The assignment is based on a published scientific article presenting new research findings.
I want the PhDs to analyze the data and derive insights similar to those presented in the article, but without access to the article itself. That way, they will have to rely on their analytical skills and understanding of the data rather than simply recalling the article's conclusions or general biological knowledge.

**Assignment structure:**

* My PhD students will receive a dataset from the article, containing single-cell omics data.
* They will *not* have access to the article itself.
* They will be required to analyze the data and answer a series of questions that test their ability to interpret patterns and derive biological insights from the dataset.

**Your task:**

* I will provide a list of key insights extracted from the article. Each insight contains a summary, the description of how the insight was derived by the authors, and the associated paragraphs from the paper that support this insight.
* For each insight, create two (2) open-ended questions that assess students’ ability to reason through the data to reach similar conclusions. **The questions should together cover different aspects of the insights and its derivation. The questions must remain strictly grounded in the provided insight** without introducing hallucinations.
* **Questions should be mostly designed based on the derivation of the insight** and not be simply factual recall of the insight's summary.
* Use the associated paragraphs to identify any additional details that could help you design more challenging questions. 
* Question should not rely on your external knowledge. The desired correct answer(s) must reflect conclusions that can be drawn directly from the omics dataset, not just recall of factual statements.

**Guidelines for creating questions:**
* Avoid phrasing that suggests PhD students need to recall the article or authors’ conclusions. Use neutral language focused on data interpretation, such as “the data indicate,” “analysis of the dataset suggests,” or “based on gene expression patterns.”
* The question should not specify the exact methods to use to derive the answer from the data. The PhD students should be able to determine the appropriate analysis methods based on the question and their understanding of single-cell omics.
* The questions should be as open-ended as possible, allowing PhD students to explore the data and derive their own conclusions. Do not specify the exact analysis methods or outcomes in the questions.
* To reduce bias, formulate questions more generally (e.g., instead of “Type 1 and Type 7 show xyz behaviour”, ask “Which types show xyz behaviour, and justify with evidence?”).
* **Each question should ask only one clear thing**. Do not merge multiple sub-questions into a single question. 
* Do not use double-barreled formulations such as “How does X differ, and what might this suggest…?” or “How do X influence Y, and what is the impact on Z?”. 
* **Do not combine two sub-questions into one (e.g., “How…, and …?”)**. Instead, split them into separate, single-focus questions.
* Do not create questions that can be answered without analyzing the data.
* Please provide many questions that cannot be answered without the data. This kind of data can be sometimes found in the description of the insight's derivation or relevant text paragraphs.
* Questions should go beyond simple answers like “increase/decrease” or “yes/no.” They should be open-ended, requiring PhDs to explore different possibilities and justify their reasoning.
* Questions should not specify the method by which the answer must be obtained, leaving room for students to choose their own approach.

**Guidelines for creating answers:**
* **In addition to the questions, provide the correct answer(s) for each question**, based strictly on the dataset-derived insight.
* **Please provide the answer(s) immediately after each question.**
* Answers should focus on the findings themselves and not mention the specific methods or tools used to obtain them (e.g., SCENIC, differential gene expression analysis, CellDB).

The goal is to translate each research insight into a data-grounded question that tests PhD students’ analytical reasoning and interpretation skills in the context of single-cell omics data.

---
**Output format:**
For each insight, provide the question and the answer in the following format. Do not include any additional text or explanations before or after the output.


**Insight:** [Your insight here]


**Question1:** [Your question here]

**Answer1:** [Answer based on the dataset/insight]


**Question2:** [Your question here]

**Answer2:** [Answer based on the dataset/insight]

---

## Few-shot examples:


### Example 1: Paper on rheumatoid arthritis

#### Insight #1

*Summary:*
The study revealed a significant increase in CD4+ T effector memory cells in RA patients, suggesting their role in disease progression.

*How it was derived:*
The researchers performed a stratified analysis based on disease activity using the Disease Activity Score in 28 joints with CRP (DAS28-CRP) to categorize patients into remission-low and moderate-high disease activity groups. They observed a significant increase in the proportion of CD4+ T effector memory cells in patients with moderate-high disease activity (P = 0.034), as shown in Figure 5C. This was supported by the compositional analysis of cell densities and proportions, indicating the involvement of these cells in RA disease activity.


**Question:** Are any cell types increased in RA patients?

**Answer:** CD4⁺ T effector memory cells are increased in RA patients, particularly in those with moderate-to-high disease activity.


**Question:** What can suggest disease progression in RA patients?

**Answer:**: An increased proportion of CD4⁺ T effector memory cells can suggest disease progression in RA patients, as their levels were significantly higher in individuals with moderate-to-high disease activity.
 
#### Insight #3

*Summary:*
The study identified an IFN-induced transmembrane 3 (IFITM3)-overexpressing IFN-activated monocyte subset that is significantly associated with rheumatoid arthritis (RA) disease activity, highlighting its potential role in the pathogenesis of RA.

*How it was derived:*
This insight was derived from single-cell RNA sequencing (scRNA-Seq) analysis of peripheral blood mononuclear cells (PBMCs) from RA patients and matched controls. The researchers used UMAP embeddings and subset annotations to identify 18 distinct PBMC subsets, including the IFITM3-overexpressing monocyte subset. The differential expression of IFITM3 and other IFN-related genes was confirmed through Wilcoxon rank sum analysis, as shown in Figure 1 and Supplemental Figure 4. The study found that IFITM3 expression was specific to this monocyte subset, suggesting its involvement in RA pathogenesis.

**Question:** Which cell subset can be significantly associated with RA disease activity?

**Answer:** The IFITM3-overexpressing IFN-activated monocyte subset can be significantly associated with rheumatoid arthritis (RA) disease activity.

**Question:** Is any gene overexpressed in the monocyte subset of RA patients? 

**Answer:** Yes, the IFITM3 gene is overexpressed in the monocyte subset of RA patients.


### Example 2: paper on COVID-19

#### Insight #1

*Summary:*
The study identified a significant increase in aberrantly activated monocyte-derived macrophages and alveolar macrophages in the lungs of COVID-19 patients, contributing to a hyperinflammatory environment.

*How it was derived:*
Using single-nucleus RNA sequencing (snRNA-seq) on lung samples from COVID-19 patients and controls, the researchers identified an increased prevalence of myeloid cells, particularly monocyte-derived macrophages and alveolar macrophages, in COVID-19 lungs. Differential gene expression analysis revealed these cells expressed activation markers and long non-coding RNAs associated with impaired T cell immunity. This was supported by diffusion component analysis and UMAP projections, as detailed in the Results and Figures 1 and 2.

**Question:** Are there any differences in cell subset distributions between COVID-19 patients and the control group?

**Answer:** Yes, there is a significant increase in aberrantly activated monocyte-derived macrophages and alveolar macrophages in the lungs of COVID-19 patients compared to controls.

#### Insight #2

*Summary:*
The study identified the expansion of pathological fibroblasts in COVID-19 lungs, which are associated with rapidly progressing pulmonary fibrosis.

*How it was derived:*
Using snRNA-seq, the researchers identified an increased fraction of fibroblasts, particularly pathological fibroblasts expressing CTHRC1 and ECM genes, in COVID-19 lungs compared to controls. The degree of fibrosis correlated with disease duration, as shown by Sirius red fibrosis scoring. Ligand-receptor interaction analysis suggested that TGFβ signaling might contribute to fibroblast-mediated fibrosis, as detailed in Figure 4 and Extended Data Figure 12.

**Question:** What contributes to the fibroblast-mediated fibrosis?

**Answer:** TGFβ signaling contributes to fibroblast-mediated fibrosis in COVID-19 lungs.

**Question:** What is correlated with disease duration?

**Answer:** The degree of fibrosis is correlated with disease duration in COVID-19 patients.


### Example 3: paper on single-cell multiomic atlas of neuroblastoma

#### Insight #1

*Summary:*
The study reveals that macrophages in the neuroblastoma microenvironment significantly expand post-therapy, adopting pro-tumorigenic phenotypes that may contribute to therapy resistance.

*How it was derived:*
The authors used single-nucleus RNA sequencing to analyze macrophage populations in neuroblastoma samples before and after chemotherapy. They identified eight macrophage subsets and noted significant shifts in these populations post-therapy, with most subsets expanding except for the pro-inflammatory IL18+ population, which decreased. This expansion towards pro-tumorigenic phenotypes, such as immunosuppressive and angiogenic states, was linked to poorer treatment outcomes. These observations are detailed in the Results section and supported by Figure 4.

**Question:** Are there any changes in the cell distribution in the neuroblastoma microenvironment post-chemotherapy?

**Answer:** There are changes in macrophage populations, which significantly expand post-chemotherapy.

#### Insight #2

*Summary:*
The study reveals that neuroblastoma neoplastic cells exhibit multiple distinct transcriptomic states that recapitulate developmental processes and can predict clinical outcomes.

*How it was derived:*
Through single-nucleus RNA sequencing, the authors identified six distinct neoplastic cell states, characterized by ADRN and MES signature scores and differential gene expression. These states were associated with different developmental stages, with MES states enriched in non-neuroblastic phenotypes and ADRN states resembling neuroblast lineages. The study linked these states to clinical outcomes, with more differentiated states predicting better prognosis. These insights are detailed in the Results section and supported by Figure 2.

**Question:** What characterizes distinct transcriptomic states in neuroblastoma neoplastic cells? 

**Answer:** Neuroblastoma neoplastic cells exhibit six distinct transcriptomic states, characterized by ADRN and MES signature scores and differential gene expression. These states were associated with different developmental stages, with MES states enriched in non-neuroblastic phenotypes and ADRN states resembling neuroblast lineages. 

---

## Examples of what not to do:
* Do not use double-barreled formulations such as “How does X differ, and what might this suggest…?” or “How do X influence Y, and what is the impact on Z?”. 
* **Do not combine two sub-questions into one (e.g., “How…, and …?”)**. Instead, split them into separate, single-focus questions.
* Do not create questions that are rephrasing the summary of the insight. These can usually be answered without the data analysis.
* **Do not create questions that ask which techniques** would a PhD student use to obtain certain result.
* Questions should **go beyond simple answers like “increase/decrease” or “yes/no.”** They should be open-ended, requiring PhDs to explore different possibilities and justify their reasoning.
* Questions **should not specify the method by which the answer must be obtained**, leaving room for students to choose their own approach.

### Example 1: paper on single-cell multiomic atlas of neuroblastoma

#### Insight #1

*Summary:*
The study identifies a significant shift in the tumor microenvironment of high-risk neuroblastoma post-chemotherapy, with an increase in mesenchymal neoplastic cells correlating with poorer chemotherapy response.

*How it was derived:*
Using single-nucleus RNA and ATAC sequencing, the authors profiled 22 patients with high-risk neuroblastoma before and after induction chemotherapy. They observed that the proportion of mesenchymal neoplastic cells increased after therapy, and a higher proportion of these cells correlated with a poorer response to chemotherapy. This was supported by statistical analyses showing significant post-therapy changes in cell state proportions, particularly in patients with mutated ALK genes, where the decrease in mesenchymal state was less pronounced. These findings are detailed in the Results section and supported by Figures 1 and 2.

##### First example of undesired question -- too narrow question

**Undesired question:** How do the proportions of mesenchymal neoplastic cells change after chemotherapy in high-risk neuroblastoma patients?

**Why it’s undesired:** This question is too narrow, as it directs the PhD student to focus only on mesenchymal neoplastic cells. The answer is only the proportions increase or decrease, which is again too narrow. Instead, the task should encourage exploring a wider range of cell types and discovering on their own that mesenchymal neoplastic cells show the most characteristic change.

**Better question:** What changes can be observed in cell type distributions before and after chemotherapy in high-risk neuroblastoma patients?


##### Second example of undesired question -- too narrow question

**Undesired question:** What correlation can be observed between mesenchymal neoplastic cells and chemotherapy response in high-risk neuroblastoma patients?

**Why it’s undesired:** This question is too narrow, as it restricts the PhD student to examining only the relationship between mesenchymal neoplastic cells and chemotherapy response. The possible answers are limited to “positive correlation,” “negative correlation,” or “no correlation,” which makes the task overly simplistic. Instead, the question should invite students to explore a broader range of cell types and investigate how their distributions correlate with chemotherapy response. This approach better develops both their biological insight and analytical skills.

**Better question:** Which cell types show a strong correlation with chemotherapy response in high-risk neuroblastoma patients?

#### Insight 2:

##### First example of undesired question -- double-barreled formulations
**Undesired question:** Based on the dataset, what distinct transcriptomic states can be identified in neuroblastoma neoplastic cells, and how do these states relate to developmental stages?

**Why it’s undesired:** This is a double-barreled question, combining two distinct tasks into one. Such formulations can confuse students and make it unclear how detailed each part of the answer should be. Instead, **each question must focus on a single aspect.**

**Split the question:**

1) What distinct transcriptomic states can be identified in neuroblastoma neoplastic cells?

2) How do these transcriptomic states relate to developmental stages?


---

## Extracted insights (their summaries and how they were derived):

**Below is the source material for generating the questions.** 
Focus more on the derivation of the insights, not just their summaries. 
The insights are:

{insights}

**Please generate two (2) open-ended questions with their answers for each insight following the above instructions.**

"""