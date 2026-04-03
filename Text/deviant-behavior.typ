// ============================================================
// deviant-behavior.typ
// Taylor & Francis – Deviant Behavior journal template
// Reference style: ASA (American Sociological Association)
//
// Sources:
//   • TF_Template_Word_Windows_2016.dotx  (style measurements)
//   • Taylor & Francis Manuscript Layout Guide
//   • Deviant Behavior Instructions for Authors
//
// ── Quick start ──────────────────────────────────────────────
//
//   #import "deviant-behavior.typ": *
//
//   #show: article.with(
//     title: "Your Title",
//     authors: (
//       (name: "Author One", affil: "a", corresponding: true),
//       (name: "Author Two", affil: "b"),
//     ),
//     affiliations: (
//       (symbol: "a", text: "Dept, University, City, Country"),
//       (symbol: "b", text: "Dept, University, City, Country"),
//     ),
//     correspondence: [CONTACT: Author One, Dept, University, City, ZIP, Country.
//       Email: author\@university.edu],
//     abstract: [Abstract text...],
//     keywords: ("keyword one", "keyword two"),
//   )
//
//   = Introduction
//   Body text @citekey. New paragraph text.
//
//   #bibliography("references.bib",
//     style: "american-sociological-association.csl")
//
// ── Notes ────────────────────────────────────────────────────
//
//   • Headings use SENTENCE CASE (only first word and proper nouns
//     capitalised), per T&F layout guide.
//   • Use American spelling throughout.
//   • Double quotation marks ("..."); single only inside a quotation.
//   • Supply american-sociological-association.csl in the same folder.
//     Download from: github.com/citation-style-language/styles
// ============================================================


// ─── Helpers ───────────────────────────────────────────────────────────────

/// Run-in heading level 4 — bold italic, inline at start of paragraph.
/// Usage:  #h4[Heading text] paragraph text continues here.
#let h4(body) = [*_#body._*#h(0.4em)]

/// Run-in heading level 5 — italic, inline at start of paragraph.
/// Usage:  #h5[Heading text] paragraph text continues here.
#let h5(body) = [_#body._#h(0.4em)]

/// Block quotation for passages of 40 or more words (no quotation marks).
/// 11 pt · indented 12.7 mm left / 10 mm right · 1.5× line spacing.
#let bquote(body) = block(
  above: 12pt,
  below: 12pt,
  inset: (left: 12.7mm, right: 10mm),
)[
  #set text(size: 11pt)
  #set par(leading: 0.65em, first-line-indent: 0pt, spacing: 0pt)
  #body
]

/// Figure caption.  Usage:  #fig-cap(1)[Caption text.]
#let fig-cap(number, body) = block(above: 6pt)[
  #set text(size: 10pt)
  #set par(leading: 0.5em, first-line-indent: 0pt, spacing: 0pt)
  *Figure #number.* #body
]

/// Note below a table.  Usage:  #table-note[Note text.]
#let table-note(body) = block(above: 4pt)[
  #set text(size: 10pt)
  #set par(leading: 0.5em, first-line-indent: 0pt, spacing: 0pt)
  _Note._ #body
]


// ─── Article template ──────────────────────────────────────────────────────

#let article(

  /// Full article title (sentence case).
  title: "",

  /// Array of author dicts.
  ///   Required:  name   — full name (string)
  ///   Optional:  affil  — affiliation letter, e.g. "a"
  ///              corresponding — bool, marks with *
  authors: (),

  /// Array of affiliation dicts.
  ///   symbol — matches the affil letter above
  ///   text   — "Dept, University, City, Country"
  affiliations: (),

  /// Full correspondence block for the * author.
  correspondence: [],

  /// Biographical notes for all contributors (≤ 200 words each).
  /// Pass `none` to omit from the title page.
  notes-on-contributors: none,

  /// Abstract text. Plain or structured — check journal instructions.
  /// Word limit: check current Instructions for Authors.
  abstract: [],

  /// Keywords (lowercase except proper nouns). Recommended: 5–6.
  keywords: (),

  /// Subject classification codes (pass `none` to omit).
  subject-codes: none,

  /// Document body — injected automatically via `#show: article.with(…)`.
  body,

) = {

  // ── Page layout ────────────────────────────────────────────────────────
  // Source: Word template pgSz / pgMar
  //   A4: 11 901 × 16 840 twips
  //   Margins: top/bottom 1 418 twips ≈ 25 mm · left/right 1 701 twips ≈ 30 mm
  set page(
    paper: "a4",
    margin: (top: 25mm, bottom: 25mm, left: 30mm, right: 30mm),
  )

  // ── Base typography ────────────────────────────────────────────────────
  // Word docDefaults: Times New Roman 12 pt (sz = 24 half-points)
  set text(font: "Times New Roman", size: 12pt, lang: "en")

  // Double line spacing — Word "Normal": line=480 twips, lineRule="auto"
  //   480 twips / 240 = 2.0 × single.  For 12 pt text → ~24 pt line height.
  //   Typst leading ≈ 1 em ≈ 12 pt gives baseline-to-baseline ≈ 24 pt. ✓
  //
  // spacing: 0pt — body paragraphs are separated ONLY by the first-line
  //   indent (Word "New paragraph" style), matching a standard double-spaced
  //   manuscript.  No extra blank space between paragraphs.
  //
  // first-line-indent: 12.7 mm — Word "New paragraph": ind firstLine=720 twips.
  //   Typst automatically suppresses this on the first paragraph after any
  //   block element (heading, quote, etc.) — matching Word's "Paragraph" style
  //   (no indent on the first paragraph of a section).
  set par(
    leading:           1em,
    spacing:           0pt,
    justify:           false,
    first-line-indent: 12.7mm,
  )

  // ── Heading styles ─────────────────────────────────────────────────────
  // Word template: all headings are 12 pt Times New Roman, no numbering.
  //
  // Spacing (Word twips → pt):
  //   before: 360 twips = 15 pt (space above the heading line)
  //   after:  60 twips  =  2.5 pt (heading's own after-space)
  //   + first paragraph after heading has before: 240 twips = 10 pt
  //   → visual gap between heading and following text ≈ 12.5 pt
  //
  // The `below` here combines both the heading-after and the para-before
  // so that the visual gap is correct without needing per-paragraph spacing.
  //
  // H1 — bold
  // H2 — bold italic
  // H3 — italic
  // H4 — run-in bold italic  →  use #h4[…] helper above
  // H5 — run-in italic       →  use #h5[…] helper above

  set heading(numbering: none)

  show heading.where(level: 1): it => block(
    above: 15pt, below: 12pt, width: 100%,
  )[#text(weight: "bold")[#it.body]]

  show heading.where(level: 2): it => block(
    above: 15pt, below: 12pt, width: 100%,
  )[#text(weight: "bold", style: "italic")[#it.body]]

  show heading.where(level: 3): it => block(
    above: 15pt, below: 12pt, width: 100%,
  )[#text(style: "italic")[#it.body]]

  // ── Bibliography ───────────────────────────────────────────────────────
  // Word "References" style:
  //   line = 360 twips → 1.5× spacing  (leading ≈ 0.65 em for 12 pt)
  //   ind left = hanging = 720 twips = 12.7 mm (hanging indent)
  //   spacing before = 120 twips ≈ 5 pt between consecutive entries
  //
  // The ASA CSL style (american-sociological-association.csl) handles the
  // hanging indent internally.  We only set line spacing and entry spacing.
  show bibliography: it => {
    set par(
      leading:           0.65em,
      spacing:           5pt,
      first-line-indent: 0pt,
    )
    it
  }


  // ══════════════════════════════════════════════════════════════════════
  // Build author and affiliation lines (computed once, reused on both pages)
  // ══════════════════════════════════════════════════════════════════════

  let author-parts = ()
  for a in authors {
    let part = [#a.name]
    if "affil" in a                          { part = part + super[#a.affil] }
    if a.at("corresponding", default: false) { part = part + super[\*] }
    author-parts.push(part)
  }

  let author-line = if author-parts.len() == 0 {
    []
  } else if author-parts.len() == 1 {
    author-parts.at(0)
  } else if author-parts.len() == 2 {
    author-parts.at(0) + [ and ] + author-parts.at(1)
  } else {
    let n = author-parts.len()
    author-parts.slice(0, n - 1).join([, ]) + [, and ] + author-parts.at(n - 1)
  }

  let affil-line = affiliations
    .map(a => [#super[#a.symbol]#a.text])
    .join([; ])


  // ══════════════════════════════════════════════════════════════════════
  // PAGE 1 — Title page
  // Contains author-identifying information.
  // For blind peer review, submit this page separately or omit author info.
  // ══════════════════════════════════════════════════════════════════════
  {
    set par(first-line-indent: 0pt, spacing: 10pt)

    // Title — 14 pt bold  (Word "Article title": sz=28, bold)
    text(size: 14pt, weight: "bold")[#title]

    // Authors — 14 pt  (Word "Author names": sz=28)
    // Superscript letters link to affiliations; * marks corresponding author.
    block(above: 10pt)[
      #text(size: 14pt)[#author-line]
    ]

    // Affiliations — 12 pt italic  (Word "Affiliation": italic)
    if affiliations.len() > 0 {
      block(above: 10pt)[
        #text(style: "italic")[#affil-line]
      ]
    }

    // Correspondence  (Word "Correspondence details": 12 pt)
    if correspondence != [] {
      block(above: 10pt)[#correspondence]
    }

    // Notes on contributors — 11 pt  (Word "Notes on contributors": sz=22)
    // Include short bio (≤ 200 words) for each author.
    if notes-on-contributors != none {
      block(above: 10pt)[
        #text(size: 11pt)[#notes-on-contributors]
      ]
    }
  }


  // ══════════════════════════════════════════════════════════════════════
  // PAGE 2 — Repeat title · Abstract · Keywords · Body · References
  // ══════════════════════════════════════════════════════════════════════
  pagebreak()

  {
    set par(first-line-indent: 0pt, spacing: 0pt)

    // Repeat title on page 2 (T&F standard requirement)
    text(size: 14pt, weight: "bold")[#title]

    // Abstract — 11 pt, indented block, 1.5× line spacing
    // Word "Abstract": sz=22 · ind left=720 twips (12.7 mm) / right=567 twips (10 mm)
    //                 spacing before=360 (15 pt) · after=300 (12.5 pt) · line=360 (1.5×)
    // T&F guide: indicate by reduced font size or heading — we use both.
    block(
      above: 15pt,
      below: 12.5pt,
      inset: (left: 12.7mm, right: 10mm),
    )[
      #set text(size: 11pt)
      #set par(leading: 0.65em, first-line-indent: 0pt, spacing: 0pt)
      #abstract
    ]

    // Keywords — 11 pt, same indented block
    // Word "Keywords": sz=22 · ind left=720 twips · spacing before/after=240 (10 pt)
    // T&F guide: 5–6 keywords; lowercase except proper nouns; separate with semicolons.
    if keywords.len() > 0 {
      block(
        above: 10pt,
        below: 10pt,
        inset: (left: 12.7mm, right: 10mm),
      )[
        #set text(size: 11pt)
        #set par(leading: 0.65em, first-line-indent: 0pt, spacing: 0pt)
        *Keywords:* #keywords.join("; ")
      ]
    }

    // Subject classification codes (optional — omit if not required)
    if subject-codes != none {
      block(
        above: 0pt,
        below: 10pt,
        inset: (left: 12.7mm, right: 10mm),
      )[
        #set text(size: 11pt)
        #set par(leading: 0.65em, first-line-indent: 0pt, spacing: 0pt)
        *Subject classification codes:* #subject-codes
      ]
    }
  }

  // Body — headings, sections, tables, figures, bibliography
  body
}
