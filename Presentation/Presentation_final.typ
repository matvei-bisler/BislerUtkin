// ============================================================
// Presentation_final.typ
//
// Conference talk accompanying "Agent-Based Modelling of 'Moral
// Entrepreneurship' and the Dynamics of Moral Panics in Social Networks".
//
// Four parts, twenty slides, following the paper's own structure:
//   1 Introduction  2 Model and methods  3 Results  4 Discussion and limitations
//
// Every figure is a separate file built by
//     cd ../Results && python3 make_presentation_figures.py
// from Results/data/*.json, the aggregates behind the paper's own figures.
// The deck uses the headline-free copies under figures/untitled/, because the
// slide heading already carries the claim.
//
// Compile from this folder:
//     typst compile Presentation_final.typ
//
// Roughly 18 minutes at one slide per 50 s. Thirteen further figures sit unused
// in figures/ (the mechanism chain, the exposure pictogram, the simplex, the
// Sobol bars, the network snapshots, the remaining defence panels): they are
// there for questions, or for a longer version of the talk.
//
// Figure widths are not free. diatypst silently CLIPS anything taller than about
// 0.45 of the text width, so a figure-only slide takes 45 x its aspect ratio in
// per cent, and every line of text on the slide costs a few points more.
// ============================================================

#import "@preview/diatypst:0.9.1": *

#set text(lang: "en", region: "gb")

#show heading.where(level: 3): set heading(numbering: none)

#show: slides.with(
  title: "Agent-Based Modelling of Moral Entrepreneurship",
  subtitle: "The Dynamics of Moral Panics in Social Networks",
  authors: ("Matvei A. Bisler", "Sergei R. Utkin"),
  footer-title: "Agent-Based Modelling of Moral Entrepreneurship",

  ratio: 16/9,
  layout: "medium",
  title-color: blue.darken(50%),
  toc: false,
  theme: "normal",
  count: "dot-section",
)

// ---- helpers -------------------------------------------------------------

#let concept(name, width: 92%) = align(center)[
  #figure(image("figures/untitled/concepts/" + name + ".pdf", width: width))
]

#let panel(name, width: 78%) = align(center)[
  #figure(image("figures/untitled/panels/" + name + ".pdf", width: width))
]

#let claim(body) = align(center)[
  #block(inset: 10pt, radius: 4pt, fill: blue.lighten(88%), width: 94%)[#body]
]

#let aside(body) = align(center)[
  #block(inset: 9pt, radius: 4pt, fill: luma(242), width: 94%)[#body]
]

// A hypothesis as it was registered, set off from the surrounding text.
#let registered(body) = block(inset: (left: 0.8em), width: 100%)[
  #set text(size: 0.82em, style: "italic")
  #body
]


= Introduction

== The Disproportionality Criterion

Moral panic is defined in part by *disproportion*: concern in excess of what the
situation warrants (Goode and Ben-Yehuda 1994). Disproportion requires a
comparison that empirical work can rarely make:

#aside[
  How alarmed would this population have been *without* the claims-making that
  alarmed it?
]

The counterfactual is unobservable, so the criterion is asserted and left
undemonstrated. Panic is invoked as self-evident while the criteria for
recognising it go unstated (Falkof 2020; Garland 2008), and Hier (2024) treats
disproportion as the field's central unresolved problem.

*A second gap.* Moral entrepreneurs, folk devils and panic are treated as three
objects with three literatures, whose interaction few formalise. Entrepreneur and
folk devil are often kept as fixed statuses, when stigmatised groups routinely act
as entrepreneurs of their own defence (Mikhaylova 2022; Hier 2011); and the
dominant instruments are not built to show how *micro-level interaction* generates
*macro-level escalation over time*.

== Research Question

A simulation can do what a case study cannot: execute the counterfactual. The
same population, the same network and the same initial draws are run twice, once
with and once without the claims-making, and the difference is computed
disproportion.

#claim[
  *Which claims-making strategies ignite a moral panic, under which network
  structures; and once ignited, what sustains it?*
]

Three hypotheses --- ignition, handover, defence --- were fixed in writing before
the runs. Several clauses were refuted, and are reported unrevised.


= Model and Methods

== Entities, States, and Structure

$N = 1000$ agents on a fixed undirected graph, each carrying two coupled states
and one fixed trait:

- *Moral position* $b_i (t) in [-1, 1]$ --- from the stigmatised pole to the
  dominant moral claim
- *Alarm* $a_i (t) in [0, 1]$ --- perceived danger, and *undirected*: how alarmed,
  not what is feared
- *Panic threshold* $theta_i$ --- past it an agent amplifies, heard $gamma$ times
  as loudly

*Two claims-makers act from outside the network.* $D$ pushes toward $+1$, $C$
toward $-1$. Neither is an agent and neither can be alarmed; standing outside is
what makes the two sources of alarm separable. The *folk devil is not an actor*:
it is the stigmatised pole around which alarm and clustering emerge.

Three generators supply the network --- Watts--Strogatz, Holme--Kim
(hub-dominated) and Erdős--Rényi --- matched on mean degree $⟨k⟩ = 10$.

== The Asymmetry the Model Rests On

#concept("c3_tolerance", width: 92%)

== Targeting Repertoires and the Control

Each active claims-maker reaches $rho_X N$ agents per step. *Which* agents is
decided by its targeting repertoire:

#table(
  columns: (auto, 1fr),
  inset: 6pt,
  stroke: none,
  table.hline(),
  [`random`], [a fresh uniform subset every step; at $rho = 1$, mass broadcast],
  [`hub`], [the highest-degree agents --- recruiting the well connected],
  [`base`], [the agents nearest the actor's own pole --- rallying the committed],
  [`fixed_random`], [*a control*: a uniform subset drawn once, addressed every step],
  table.hline(),
)

`hub` and `base` depart from `random` along two dimensions at once, in *whom*
they select and in returning to *the same* people. Separating the two requires a
control that departs along one dimension only:

- `random` against `fixed_random` isolates the *exposure schedule*
- `fixed_random` against `hub` isolates *degree*

== Measuring Disproportion

#concept("c1_four_worlds", width: 77%)

== The Panic Index and the Design

$ Pi(t) = (overline(a)(t) - overline(a)^"null" (t)) / (1 - overline(a)^"null" (t)) in [0, 1] $

An *episode* is at least $W$ steps with $Pi >= Pi^*$ and $q >= q^*$, where $q$ is
the share of the population past threshold. The three cuts are conventional, so
incidence is reported across a grid of all three.

#grid(
  columns: (1.1fr, 1fr),
  gutter: 12pt,
  [
    *Operating point*
    - small world, $N = 1000$, $⟨k⟩ = 10$
    - $epsilon = 0.5$; $mu = 0.30$, $delta = 0.25$, $omega = 0.35$
    - `base`, $alpha_D = 0.7$, $rho_D = 0.25$
    - withdrawal $t_"off" = 150$, horizon $T = 400$
    - 250 seeds; 291,960 runs
  ],
  [
    *Conditions checked at every point*
    - contagion sub-critical, so alarm cannot sustain itself
    - campaign-free world calm ($overline(a)^"null" <= 0.052$)
    - population starts agreed (mean gap $0.067$)
    - implementation docked against five known models: *14 / 14 checks pass*
  ],
)


= Results

== H1 --- Ignition Requires a Stable Audience

#registered[
  H1, as registered. Which repertoire ignites depends on topology; ignition is
  amplifying but not discontinuous. `hub` ignites fastest in hub-dominated
  networks and degenerates to `random` where degrees are even.
]

#panel("h1a_reach", width: 63%)

== What the Control Establishes

`fixed_random` tracks `base` across the sweep, and the two share nothing except a
settled audience. Since `fixed_random` knows nothing about who anyone is, what
amplifies cannot be a property of the people chosen.

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  [
    *Schedule* --- `random` to `fixed_random` --- multiplies $Pi$ by up to $7.0$,
    and accounts for the whole of `hub`'s advantage at $rho_D >= 0.30$.
  ],
  [
    *Degree* --- `fixed_random` to `hub` --- is worth a further $2.2$ to $2.5$
    times at $rho_D <= 0.10$, and nothing above $0.25$.
  ],
)

The registered degeneration clause is *refuted*: on Watts--Strogatz, where degree
varies by a standard deviation of $1.00$, `hub` still produces up to $14.8$ times
the disproportion `random` does. Topology moves `hub` and almost nothing else;
the other three repertoires vary by less than $0.02$.

#claim[
  A campaign becomes dangerous by addressing *some* people and not others,
  *repeatedly*. Which people they are matters less, and above $rho_D = 0.25$ not
  at all.
]

== Depth Is a Gate, Reach Is the Dial

#panel("h1d_gate", width: 75%)

== Universal Reach Manufactures No Division

#panel("h1c_interaction", width: 60%)

*Below the gate* a campaign converts: reached agents stay within their
neighbours' tolerance, $overline(b) arrow 0.99$, and the interaction never leaves
zero. *At universal reach* all four repertoires become one rule, exposure
concentration is exactly zero, and panic incidence is *$0.00$ under every cut of
the criterion*.

== H2 --- Where the Alarm Comes From

#registered[
  H2, as registered. Claims-alone rises first and plateaus, while the interaction
  rises later and overtakes it. After withdrawal, $Pi$ remains elevated for a
  duration governed by othering rather than by passive decay.
]

#panel("h2a_decomposition", width: 63%)

== The Apportionment

Of all alarm that would not have existed had nobody campaigned:

#align(center)[
  #table(
    columns: (2.4fr, 1fr),
    inset: 5pt,
    stroke: none,
    table.hline(),
    [*Source*], [*Share*],
    table.hline(stroke: 0.4pt),
    [Claims-making alone], [14%],
    [Othering alone (division present beforehand)], [2%],
    [Interaction (campaign-created division, othered)], [*84%*],
    table.hline(),
  )
]

- Mean othering exposure is $0.189$ in the full run against $0.006$ where nobody
  campaigns: the entrepreneur made *97%* of what the population reacts to
- *The registered ordering fails.* The interaction overtakes claims-alone at
  $t = 2$, the earliest step permitted, in 250 of 250 seeds and at every depth
- The result is an *apportionment*, and carries no chronology in which the
  entrepreneur holds the episode up alone before the public takes over

== What Survives the Withdrawal

#panel("h2b_othering", width: 59%)

Claims-alone falls to zero within five steps of withdrawal; 250 steps later $Pi$
retains *62%*. Three instruments agree on why: the $omega$ sweep at fixed
$mu + delta$, the simplex scan, and the Sobol decomposition, in which the *split*
scores $S_T = 0.993$ while total intensity scores $0.03$ and memory exactly $0$.

== H3 --- Counter-Claims-Making

#registered[
  H3, as registered, with both outcomes fixed in advance. _Branch 1:_
  broad-and-shallow lowers $Pi$ while narrow-and-deep raises it. _Branch 2:_ no
  configuration lowers $Pi$. #h(0.4em) *Neither occurred.*
]

#panel("h3a_overshoot", width: 62%)

== Defence Is a Sequence, Not a Sign

#align(center)[
  #table(
    columns: 6,
    inset: 5pt,
    align: center,
    stroke: none,
    table.hline(),
    table.header([configuration], [$(alpha_C, rho_C)$], [peak $Pi$], [excess],
                 [steps above], [$Pi(399)$]),
    table.hline(stroke: 0.4pt),
    [undefended], [(---, 0)], [0.289], [---], [---], [0.179],
    [broad and shallow], [(0.15, 0.60)], [0.329], [+0.077], [9], [0.106],
    [narrow and deep], [(0.90, 0.10)], [*0.467*], [*+0.239*], [24], [*0.020*],
    [matched], [(0.70, 0.25)], [0.380], [+0.135], [11], [0.045],
    table.hline(),
  )
]

- The largest overshoot belongs to the *lowest-reach* configuration, which rules
  out the cost channel: pulling a tenth of the population to $-1$ maximises
  distance to a bulk sitting at $overline(b) = +0.29$
- The reduction is *conversion, not reassurance*: $overline(b) arrow -0.99$ and
  mean othering exposure collapses to $0.005$
- A residual floor $approx 0.18 rho_C$: linear in reach, flat in depth


= Discussion and Limitations

== What the Apportionment Settles

The elite-driven and interactionist accounts have disputed the same episodes
without any means of apportioning them. The four-run design apportions them:
*14 : 2 : 84*.

Neither camp is right as usually stated. The entrepreneur is *necessary* --- where
nobody campaigns, or campaigns too mildly to be disowned, nothing happens --- and
nearly irrelevant to the *magnitude*.

#claim[
  The claims-maker cannot undo what it started, because the excess alarm no
  longer rests on the campaign. The object of intervention is not "stop the
  campaign" but the moral distance between people and those they actually talk to.
]

== Predictions for Empirical Research

*Ignition depends on repeated exposure to the same audience.* The mass
broadcaster is structurally the worst available entrepreneur. The measurable
quantity is the *concentration* of exposure, not its volume, which makes audience
fragmentation part of the mechanism rather than its setting.

*Local density decides whether a panic outlives its campaign.* Across two
empirical networks and matched generators $Pi(149)$ varies little; what survives
tracks clustering, $0.135 slash 0.100 slash 0.072 slash 0.006$ as it falls. No
synthetic generator reproduced this.

*Answering back intensifies the episode before it ends it.* And most when most
committed --- with no tone, provocation or backlash psychology in the model. It is
arithmetic on moral distance.

*A methodological warning.* Incidence jumps from $0.08$ to $0.96$ between
$rho_D = 0.15$ and $0.20$ while $Pi$ drifts from $0.177$ to $0.234$; empirical
episode counts may inherit their sharpness from the coding rule.

== Limitations

*The hard ceiling.* $Pi$ measures excess over the *model's own* counterfactual,
not over any real danger, because the model contains no danger to be in excess
of. Disproportionality is made *computable*, not *decidable*.

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  [
    *Five exclusions*
    - networks do not rewire, so nobody is actively repelled
    - no algorithm, no recommender
    - no actor can reassure
    - panics leave attitudes, not institutions
    - claims-makers do not learn
  ],
  [
    *Three scope conditions*
    - no pull back toward pre-campaign convictions ($sigma = 0$)
    - moral positions reasonably stable ($zeta lt.tilde 0.02$)
    - a population that starts agreed
  ],
)

Six parameters, but roughly *three live dimensions*: the depth--tolerance gate,
reach, and othering. Every simplification pushes the same way, toward
*under*-stating how far a population comes apart.

== Conclusion

The three results that generalise beyond this parameterisation are *negative in
form*:

+ Claims-making that reaches *everyone* cannot produce a panic --- manufactured
  division requires *unequal* exposure
+ Claims-making too shallow to be *disowned* cannot produce one either --- it
  persuades instead of dividing
+ Answering back cannot lower alarm without first raising it --- the only channel
  open to it is the elimination of disagreement

#claim[
  If moral panics are becoming easier to start, the reason is not that reach has
  increased.
]

#v(0.4em)

#align(center)[*Thank you.* Questions welcome.]
