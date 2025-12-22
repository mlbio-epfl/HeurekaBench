insight2question_prompt_text = """
I am designing assignments for my PhD students on single-cell omics data. The assignment is based on a published scientific article presenting new research findings.
I want the PhDs to analyze the data and derive insights similar to those presented in the article, but without access to the article itself. That way, they will have to rely on their analytical skills and understanding of the data rather than simply recalling the article's conclusions or general biological knowledge.

**Assignment structure:**

* My PhD students will receive a dataset from the article, containing single-cell omics data.
* They will *not* have access to the article itself.
* They will be required to analyze the data and answer a series of questions that test their ability to interpret patterns and derive biological insights from the dataset.

**Your task:**

* I will provide a list of key insights extracted from the article. Each insight contains a summary, the description of how the insight was derived by the authors, and the associated paragraphs from the paper that support this insight.
* For each insight, create two (2) multiple-choice questions that assess students’ ability to reason through the data to reach similar conclusions. **The questions should together cover different aspects of the insights and its derivation. The questions must remain strictly grounded in the provided insight** without introducing hallucinations.
* **Questions should be mostly designed based on the derivation of the insight** and not be simply factual recall of the insight's summary.
* Use the associated paragraphs to identify any additional details that could help you design more challenging questions, including plausible but tricky wrong answers (hard negatives). 
* Question and correct answer should not rely on your external knowledge. The correct answer(s) must reflect conclusions that can be drawn directly from the omics dataset, not just recall of factual statements.
* Tips for **designing hard questions with hard negatives**s:
  1) Wrong answers should simulate realistic misinterpretations of the data, premature conclusions, or confusions between similar cell types / genes / pathways. These are more cognitively demanding for PhD students to distinguish.
  2) Avoid irrelevant or obviously false options. Each incorrect option should reflect a misguided but well-intentioned line of reasoning from someone analyzing the dataset.
* Questions can be either:

  * *Single-answer*: one correct option (e.g., “D”)
  * *Multiple-answer*: more than one correct option (e.g., “A,C,D”)

**Guidelines:**

* Randomize the position of the correct answer(s) among the options.
* Avoid phrasing that suggests PhD students need to recall the article or authors’ conclusions. Use neutral language focused on data interpretation, such as “the data indicate,” “analysis of the dataset suggests,” or “based on gene expression patterns.”
* The question should not specify the exact methods to use to derive the answer from the data. The PhD students should be able to determine the appropriate analysis methods based on the question and their understanding of single-cell omics.
* The questions should be as open-ended as possible, allowing PhD students to explore the data and derive their own conclusions. Do not specify the exact analysis methods or outcomes in the questions.
* **If for the answer, there are multiple correct options (e.g., cells, genes, etc.), the answer should be splitted in multiple options**, e.g., A) cell type 1, B) cell type 2, C) cell type 3, D) cell type 4. **The correct answer should be a combination of these options**, e.g., "A,C" or "B,D". 
* **Please provide many questions that cannot be answered without the data.** This kind of data can be sometimes found in the description of the insight's derivation.

The goal is to translate each research insight into a data-grounded question that tests PhD students’ analytical reasoning and interpretation skills in the context of single-cell omics data.

---

**Output format:**
For each insight, provide the question and answer options in the following format. Do not include any additional text or explanations before or after the output.


**Insight:** [Your insight here]

**Question1:** [Your question here]

A) [Option A]

B) [Option B]

C) [Option C]

D) [Option D]

**Answer1:** [Correct option(s) here, e.g., "A,C"]

**Question2:** [Your question here]

A) [Option A]

B) [Option B]

C) [Option C]

D) [Option D]

**Answer2:** [Correct option(s) here, e.g., "A,C"]

**Question3:** [Your question here]

A) [Option A]

B) [Option B]

C) [Option C]

D) [Option D]

**Answer3:** [Correct option(s) here, e.g., "A,C"]

---

## Few-shot examples:


### Example 1: Paper on rheumatoid arthritis

#### Insight #1

* Summary:
The study revealed a significant increase in CD4+ T effector memory cells in RA patients, suggesting their role in disease progression.

* How it was derived:
The researchers performed a stratified analysis based on disease activity using the Disease Activity Score in 28 joints with CRP (DAS28-CRP) to categorize patients into remission-low and moderate-high disease activity groups. They observed a significant increase in the proportion of CD4+ T effector memory cells in patients with moderate-high disease activity (P = 0.034), as shown in Figure 5C. This was supported by the compositional analysis of cell densities and proportions, indicating the involvement of these cells in RA disease activity.

**Question:** Analysis of the dataset indicates which cell type is increased in RA patients?

A) CD8+ naive T cells

B) CD4+ T effector memory cells

C) Plasmablasts

D) Classical monocytes

**Correct Answer**: B

This question is intentionally open-ended to allow my PhD students to explore which cell type is increased in RA patients. We should avoid including any additional specifics—such as vague descriptors like "moderate-high disease activity of RA"—regarding the analysis or outcomes. The correct answer can be derived from the summary.

#### Insight #3

* Summary:
The study identified an IFN-induced transmembrane 3 (IFITM3)-overexpressing IFN-activated monocyte subset that is significantly associated with rheumatoid arthritis (RA) disease activity, highlighting its potential role in the pathogenesis of RA.

* How it was derived:
This insight was derived from single-cell RNA sequencing (scRNA-Seq) analysis of peripheral blood mononuclear cells (PBMCs) from RA patients and matched controls. The researchers used UMAP embeddings and subset annotations to identify 18 distinct PBMC subsets, including the IFITM3-overexpressing monocyte subset. The differential expression of IFITM3 and other IFN-related genes was confirmed through Wilcoxon rank sum analysis, as shown in Figure 1 and Supplemental Figure 4. The study found that IFITM3 expression was specific to this monocyte subset, suggesting its involvement in RA pathogenesis.

**Question:** Based on the dataset analysis, which cell subset is significantly associated with RA disease activity?

A) CD4+ naive T cells

B) IFN-activated monocytes

C) Nonclassical monocytes

D) Memory B cells

**Correct Answer:** B

**Explanation of the question and answer**: The question is open for my PhDs to explore what cell subset is associated with RA disease activity. We should not specify that it is due to the overexpression of IFITM3. The PhD student should be the one to discover the reason. Correct answer is extracted from the insight summary.


---

### Example 2: paper on COVID-19


#### Insight #1

* Summary:
The study identified a significant increase in aberrantly activated monocyte-derived macrophages and alveolar macrophages in the lungs of COVID-19 patients, contributing to a hyperinflammatory environment.

* How it was derived:
Using single-nucleus RNA sequencing (snRNA-seq) on lung samples from COVID-19 patients and controls, the researchers identified an increased prevalence of myeloid cells, particularly monocyte-derived macrophages and alveolar macrophages, in COVID-19 lungs. Differential gene expression analysis revealed these cells expressed activation markers and long non-coding RNAs associated with impaired T cell immunity. This was supported by diffusion component analysis and UMAP projections, as detailed in the Results and Figures 1 and 2.

**Question:** Based on the dataset, what types of cell contribute to hyperinflammatory environment in COVID-19 lungs?
A) Monocyte-derived macrophages
B) Alveolar epithelial cells
C) Alveolar macrophages
D) Neutrophils

**Correct Answer:** A,C

**Explanation of the question and answer**: This is an example of a good multiple-choice question, with very good negatives. Please provide questions with multiple correct answers and plausible negatives.


#### Insight #2

* Summary:
The study identified the expansion of pathological fibroblasts in COVID-19 lungs, which are associated with rapidly progressing pulmonary fibrosis.

* How it was derived:
Using snRNA-seq, the researchers identified an increased fraction of fibroblasts, particularly pathological fibroblasts expressing CTHRC1 and ECM genes, in COVID-19 lungs compared to controls. The degree of fibrosis correlated with disease duration, as shown by Sirius red fibrosis scoring. Ligand-receptor interaction analysis suggested that TGFβ signaling might contribute to fibroblast-mediated fibrosis, as detailed in Figure 4 and Extended Data Figure 12.

**Question:** Which genes are expressed by the pathological fibroblasts identified as increased in COVID-19 lungs?
A) CTHRC1 genes
B) ACTA2 genes
C) COL1A1 genes 
D) ECM genes

**Correct Answer:** A,D

**Explanation of the question and answer**: This is an example of a good multiple-choice question, with very good negatives. Please provide questions with multiple correct answers and plausible negatives. The question is based on the how it was derived part, and it requires the analysis of the dataset to be answered.

---

## Examples of what not to do:
* Do not create questions that are rephrasing the summary of the insight. These can usually be answered without the data analysis.
* Do not create questions that ask which techniques would a PhD student should use to obtain certain result. 


### Example 1 of what not to do:
#### Insight:

*Note: Paper is on COVID-19*

* Summary:
The study revealed that epithelial cell-derived interleukin-6 (IL-6) is more abundant in COVID-19 lungs, contributing to the inflammatory milieu.

* How it was derived:
Using imaging mass cytometry, the researchers quantified IL-6 expression in lung tissues from COVID-19 patients and controls. They found that IL-6 was more abundant in epithelial cells from COVID-19 patients, although not differentially expressed in macrophages. This cytokine's role in inflammation was further discussed in the context of the lung's hyperinflammatory environment, as shown in Figure 3 and Extended Data Figure 9.

**Question:** Which cytokine is found to be more abundant in epithelial cells of COVID-19 lungs, *contributing to the inflammatory environment*?

A) Interleukin-10 (IL-10)

B) Interleukin-6 (IL-6)

C) Tumor necrosis factor-alpha (TNF-α)

D) Interferon-beta (IFN-β)

**Correct Answer:** B

**Description why I do not want this:** You should not specify that it contributes to the inflammatory environment, as this is derived from the data analysis. The PhD students should derive this from the data on their own.

**Instead, you could ask:** What is more abundant in epithelial cells from COVID-19 patients compared to controls?

### Example 2 of what not to do:

#### Insight:

*Note: Paper is on intestine-on-chip*

* Summary:
The intestine-on-chip model demonstrated the ability to capture the cellular diversity of the human small intestine, including major epithelial subtypes, myofibroblasts, and neurons.

* How it was derived:
Single-cell RNA sequencing (scRNA-seq) was performed on cells from the intestine-on-chip, revealing two transcriptionally distinct compartments: epithelial and mesenchymal/neural. The epithelial compartment included transit-amplifying/stem cells, enterocytes, Paneth-like cells, goblet cells, and enteroendocrine cells. The mesenchymal/neural compartment contained myofibroblasts and neurons, among others (Results, Figures 3A-C).


**Question:** What analysis was performed to reveal the transcriptionally distinct compartments in the intestine-on-chip model?

A) Pseudotime analysis

B) Single-cell RNA sequencing (scRNA-seq)

C) Correlation analysis

D) FITC-dextran permeability test

**Correct Answer:** B

**Description why I do not want this:**  This question is not good because it does not require the analysis of the data. The answer is simple as it tests the basic knowledge of the techniques used in biology.

**Instead, you could ask:** What was revealed about the cells from the intestine-on-chip?


### Example 3 of what not to do:

#### Insight:

*Note: Paper is on COVID-19*

* Summary:
The study found that COVID-19 lungs exhibit an ectopic presence of tuft-like cells, which may play a role in the disease's pathophysiology.

* How it was derived:
The researchers identified a trajectory of tuft-like cells in COVID-19 lungs using snRNA-seq, which were not present in control lungs. These cells expressed markers like CHAT and POU2F3 and were found in increased numbers in the upper airways and lung parenchyma of COVID-19 patients. The potential role of these cells in viral pneumonia was further explored using mouse models, as described in the Results and Extended Data Figure 10.

**Question:** What does the dataset indicate about the presence of tuft-like cells in COVID-19 lungs?

A) They are absent in COVID-19 lungs

B) They express markers like CHAT and POU2F3

C) They are found in control lungs

D) They are increased in the upper airways and lung parenchyma

**Correct answers**: B, D

**Description why I do not want this:**  The question uses absolute terms like “absent” and “found,” which can be too harsh. It is better to use softer language such as “rare” or “not rare” to reflect biological variability more accurately. Also, since the question focuses on tuft-like cells in COVID-19 lungs, including control lungs in the answer options creates confusion and distracts from the main focus. The negatives in the answers are poorly phrased and are easy to distinugish. Create hard negatives to distinguish from.


---

## Extracted insights (their summaries and how they were derived):

**Below is the source material for generating the questions.** 
Focus more on the derivation of the insights and the associated paragraphs from the paper, not just the insight summaries. 
The insights are:

{insights}

---

**Please generate two (2) multiple-choice questions for each insight following the above instructions.**

"""
