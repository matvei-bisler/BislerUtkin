// ============================================================
// article.typ — Manuscript for Deviant Behavior
// Imports deviant-behavior.typ template (same folder)
// ============================================================

#import "deviant-behavior.typ": *

#show: article.with(
  title: "Article title in sentence case goes here",

  authors: (
    (name: "Author Name 1", affil: "a", corresponding: true),
    (name: "Author Name 2", affil: "b"),
    (name: "Author Name 3", affil: "a"),
  ),

  affiliations: (
    (symbol: "a", text: "Department, University, City, Country"),
    (symbol: "b", text: "Department, University, City, Country"),
  ),

  correspondence: [CONTACT: Author Name 1, Department, University,
    Street Address, City ZIP, Country. Email: email\@university.edu],

  notes-on-contributors: [
    *Author Name 1* biographical note (≤ 200 words).

    *Author Name 2* biographical note (≤ 200 words).

    *Author Name 3* biographical note (≤ 200 words).
  ],

  abstract: [Abstract text goes here as prescribed by the journal's
    instructions for authors. State the research question, methods, key
    findings, and conclusions. Check current Instructions for Authors for
    word limit and whether a structured abstract is required.],

  keywords: (
    "keyword 1",
    "keyword 2",
    "keyword 3",
    "keyword 4",
    "keyword 5",
  ),

  // subject-codes: "Code1; Code2",  // uncomment only if required by journal
)


// ─────────────────────────────────────────────────────────────────────────────
= Introduction
// ─────────────────────────────────────────────────────────────────────────────

First paragraph — no first-line indent after a heading (T&F "Paragraph" style).
Cite sources with `@citekey` in ASA author-date style, e.g. @placeholder_book_a.

Second paragraph — first-line indent (T&F "New paragraph" style). Use
*bold* for terms introduced for the first time and _italic_ for emphasis
or foreign words. Use double quotation marks "like this" throughout.


// ─────────────────────────────────────────────────────────────────────────────
= Theoretical background
// ─────────────────────────────────────────────────────────────────────────────

== Level 2 heading

First paragraph of section. Cite @placeholder_article_b.

Second paragraph. Block quotation for passages of 40 or more words:

#bquote[
  Block quotation text goes here without quotation marks. Indent the passage
  and omit quotation marks. Citation follows the closing punctuation
  @placeholder_book_c.
]

Paragraph resuming after the block quotation (no indent).

New paragraph with first-line indent.

== Another level 2 heading

=== Level 3 heading

First paragraph under level 3 heading.

Run-in headings for levels 4 and 5 — use the `#h4` and `#h5` helpers:

#h4[Level 4 run-in heading.] Paragraph text begins immediately after the
bold-italic heading and period, with a thin space between them.

#h5[Level 5 run-in heading.] Paragraph text begins immediately after the
italic heading and period.


// ─────────────────────────────────────────────────────────────────────────────
= Data and methods
// ─────────────────────────────────────────────────────────────────────────────

== Sample

Describe the data source, sampling strategy, and final analytic sample
(_N_ = 000) @placeholder_book_d.

== Measures

=== Dependent variable

Description of the dependent variable and operationalization (α = .XX).

=== Independent variables

Description of key independent variables (α = .XX).

=== Controls

Description of control variables.

== Analytic strategy

Description of statistical methods and software @placeholder_article_e.


// ─────────────────────────────────────────────────────────────────────────────
= Results
// ─────────────────────────────────────────────────────────────────────────────

== Descriptive statistics

[Table 1 near here]

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: (left, right, right, right),
    stroke: none,
    table.hline(stroke: 1pt),
    table.header(
      [*Variable*], [*Mean*], [*SD*], [*Range*],
    ),
    table.hline(stroke: 0.5pt),
    [Variable 1], [0.00], [0.00], [0–0],
    [Variable 2], [0.00], [0.00], [0–0],
    [Variable 3], [0.00], [0.00], [0–0],
    table.hline(stroke: 1pt),
  ),
  caption: [Table 1 title (_N_ = 0,000)],
)

#table-note[Explain abbreviations, significance levels (* _p_ < .05;
** _p_ < .01; \*\*\* _p_ < .001), and data source here.]

== Main analyses

[Table 2 near here]

Results text @placeholder_article_f. Reference tables and figures in the
text as "(see Table 1)" or "[Figure 1 near here]".

== Sensitivity analyses

Description of robustness checks and alternative specifications.


// ─────────────────────────────────────────────────────────────────────────────
= Discussion
// ─────────────────────────────────────────────────────────────────────────────

#h4[Finding 1.] Discussion of the first main finding and its theoretical
implications @placeholder_article_g.

#h4[Finding 2.] Discussion of the second main finding.

#h4[Finding 3.] Discussion of the third main finding.

== Limitations

Limitations and directions for future research.


// ─────────────────────────────────────────────────────────────────────────────
= Conclusion
// ─────────────────────────────────────────────────────────────────────────────

Concluding paragraph summarising contributions and policy implications.


// ── End-matter ───────────────────────────────────────────────────────────────

*Acknowledgements*

[Acknowledgements, if any. Omit during blind peer review — add after acceptance.]

*Disclosure of interest*

The authors report there are no competing interests to declare.

*Funding*

[Grant details: funding agency, grant number. Or state: This research
received no specific grant from any funding agency in the public, commercial,
or not-for-profit sectors.]

*Data availability statement*

[Describe where data supporting this article can be found, or state that
the data are not publicly available and why.]


// ─────────────────────────────────────────────────────────────────────────────
// References — formatted automatically by Typst using the ASA CSL style
// ─────────────────────────────────────────────────────────────────────────────

#bibliography("references.bib",
  style: "american-sociological-association.csl",
  title: "References")
