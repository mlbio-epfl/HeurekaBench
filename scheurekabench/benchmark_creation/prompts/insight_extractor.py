insight_extractor_prompt = """
**You are a scientific research assistant with expertise in interpreting and analyzing high-impact scientific publications.**

You will be provided with a research article in the field of single-cell RNA sequencing biology that presents novel findings.

Your task is to extract **10 distinct, non-overlapping key insights** grounded specifically in the **authors' analysis and interpretation of their data**, rather than general background or established biological facts. Each insight must be **analytically derived**—emphasizing conclusions, patterns, or implications the authors draw from their results, demonstrating a deep understanding of the study's significance.

---

### What is a “High-Level Insight”?

A high-level insight is a concise, meaningful takeaway capturing a core contribution or finding of the study. Such insights typically appear in:

* The abstract
* Discussion or conclusion sections
* Summaries within results or figure legends
* Syntheses of experimental findings

These insights should avoid vague or broad restatements. Instead, they should clarify **what** was found, **why** it matters, and **how** the authors arrived at the conclusion.

---

### Task Instructions:

Extract and rank **10 insights** by importance, using this structured format for each:

**Insight #X**

*Summary:*
A clear, concise (1–3 sentences) paraphrased summary of the insight, capturing a key finding, interpretation, or contribution.

*How it was derived:*
A brief paragraph (3–5 sentences) detailing how the insight was obtained, focusing on information sufficient to reproduce the analysis. Include:

* Experimental and computational methods used
* Key data trends, statistical analyses, or comparisons
* Supporting figures, tables, or quantitative evidence, if applicable
* Authors’ interpretations relevant to the insight
* Reference the relevant paper sections (e.g., Results, Figures, Abstract)

*Relevant text paragraphs:*
Up to 10–15 sentences from the paper that underpin the insight, for context. Replicate the original text as closely as possible, ensuring it is clear and informative. This should reflect the authors' own words and interpretations, not your paraphrasing.

---

### Content Prioritization

When reading the article, prioritize these sections in order:

1. Abstract — overarching goals and headline findings
2. Main Results — detailed data, trends, and discoveries
3. Figures and Figure Legends — visual summaries and experimental design
4. Discussion — interpretations, implications, future directions
5. Methods — how insights were generated

---

### Additional Guidelines

* Use paraphrasing to avoid direct quotes in summaries and derivations.
* Ensure each insight stands alone and is understandable without the full paper.
* Favor insights that:

  * Reveal cause-effect relationships
  * Highlight unexpected or counterintuitive results
  * Synthesize multiple lines of evidence
  * Introduce novel techniques or conceptual advances
* Exclude formatting artifacts (page numbers, citation codes, etc.).
* If the study has multiple sub-experiments or datasets, derive at least one insight from each.
* Do **not** fabricate or simulate insights not explicitly present in the paper.
* Your audience is a biomedical researcher, so maintain rigor and accuracy.

---

### Example Output (illustrative only):

**Insight #3**

*Summary:*
The study reveals that COVID-19 lungs exhibit a significant increase in aberrantly activated monocyte-derived macrophages and alveolar macrophages, contributing to a hyperinflammatory state.

*How it was derived:*
Using single-nucleus RNA sequencing (snRNA-seq), the authors identified an increased prevalence of monocyte-derived macrophages (MDMs) and alveolar macrophages (AMs) in COVID-19 lungs compared to controls. Diffusion component analysis highlighted distinct trajectories for these myeloid cells, which were more frequent in COVID-19 cases. The study found differential expression of activation markers and long non-coding RNAs associated with aberrant macrophage activation, suggesting these cells are a major source of dysregulated inflammation. This data is supported by Figure 2 and Extended Data Figures 4 and 5.

*Relevant text paragraphs:*
Aberrant activation of myeloid cells: Myeloid cells represented a major cellular constituent in COVID-19 lungs and were more prevalent there than in control lungs (Fig. 1d, 
Extended Data Figs. 2a, c, 4a). We identified monocytes (n = 3,176), monocyte-derived macrophages (MDMs; n = 9,534), transitioning MDMs (n = 4,203), and resident alveolar macrophages (AMs; n = 12,511), 
which were recovered as distinct trajectories in diffusion component (DC) analysis and were more frequent in COVID-19 lungs (Fig. 2a–c, Extended Data Fig. 4b–i, Supplementary Tables 2, 4, 5). 
Myeloid cells from individuals with COVID-19 were highly and aberrantly activated. 
For example, MDMs in COVID-19 lungs differentially expressed genes of activation (for example, CTSB, CTSD, CTSZ, PSAP) and two long 
non-coding RNAs, NEAT1 and MALAT1, that are associated with aberrant macrophage activation and impaired T cell immunity18 (Extended 
Data Fig. 5a, Supplementary Table 5). AMs, which arise from fetal monocytes and can self-renew19, were enriched and highly activated 
in COVID-19 lungs (Fig. 2c, Extended Data Fig. 5a). Notably, COVID 19 AMs showed strongly decreased mRNA and protein expression of 
the tumour-associated macrophage receptor AXL (Fig. 2d, Extended Data Fig. 5b, c), a receptor tyrosine kinase that is important for coor
dinated clearance of apoptotic cells (efferocytosis) and subsequentanti-inflammatory regulation during tissue regeneration20. These data 
suggest that myeloid cells are a major source of dysregulated inflammation in COVID-19.

---

Now, carefully review the article and **generate 10 insights** using this structure and guidelines.
"""