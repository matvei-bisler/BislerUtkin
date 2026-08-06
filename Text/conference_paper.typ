// ============================================================
// conference_paper.typ
// Agent-Based Modelling of "Moral Entrepreneurship" and the
// Dynamics of Moral Panics in Social Networks
//
// Bibliographies:  ../Moral Panic.bib           (Zotero export, substantive)
//                  ../Computational Methods.bib (Zotero export, methods)
// Citation style:  american-sociological-association.csl (this folder)
//
// Spelling: British ("modelling", "defence", "recognise"), following the title.
// Self-contained: no deposit, no pointers outside this text. One appendix (notation).
//
// Compile from the repository root (the figures live outside this folder):
//   typst compile --root . Text/conference_paper.typ
// ============================================================

#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1",
)

#set text(
  size: 11pt,
  lang: "en",
  region: "gb",
)

#set par(justify: true, leading: 0.72em, first-line-indent: 1.5em)

#set heading(numbering: "1.1")
#show heading: set block(above: 1.4em, below: 0.8em)
#show heading.where(level: 1): set text(size: 12pt, weight: "bold")
#show heading.where(level: 2): set text(size: 11pt, weight: "bold", style: "italic")

#set math.equation(numbering: "(1)")
#show figure.caption: set text(size: 9.5pt)
#set table(stroke: none)

// Run-in heading: bold lead-in, paragraph continues on the same line.
#let h4(body) = [*#body.*#h(0.4em)]

// Pre-registered hypothesis, set off from the surrounding prose.
#let registered(body) = block(inset: (left: 1.2em), width: 100%)[
  #set text(size: 10pt, style: "italic")
  #set par(first-line-indent: 0pt)
  #body
]


// ── Title block ──────────────────────────────────────────────────────────────

#align(center)[
  #block(width: 92%)[
    #text(size: 15pt, weight: "bold")[
      Agent-Based Modelling of "Moral Entrepreneurship" and the Dynamics of Moral Panics in Social Networks
    ]
  ]

  #v(1.1em)

  #text(size: 11.5pt)[Matvei A. Bisler#super[\*] #h(1.2em) Sergei R. Utkin#super[\*\*]]

  #v(0.4em)

  #block(width: 88%)[
    #set text(size: 9pt)
    #set par(justify: false, first-line-indent: 0pt, leading: 0.6em)
    \* Doctoral School of Political Science, HSE University; Universal University \
    \*\* International Center for the Study of Institutions and Development; Doctoral School of Political Science, HSE University
    // TODO: corresponding author's email, if the venue requires one.
  ]
]

#v(1.4em)


// ── Abstract ─────────────────────────────────────────────────────────────────

#block(width: 100%, inset: (x: 1.2em))[
  #set text(size: 10pt)
  #set par(justify: true, first-line-indent: 0pt, leading: 0.68em)

  *Abstract.* Disproportion belongs to the definition of moral panic and is almost never measured: no one can observe how alarmed a population would have been without the claims-making that alarmed it. This paper makes that comparison computable. We specify an agent-based model in which 1,000 networked agents carry two coupled states, a moral position and a level of alarm, updated through bounded confidence, in which people are moved only by those they still find close enough to listen to; threshold contagion, in which alarm is caught from others and the alarmed are heard more loudly; and othering, the conversion of local moral disagreement into perceived threat. Two claims-makers act on the population from outside. Every setting is run four times on one seed in a $2 times 2$ design (claims-making on/off $times$ othering on/off), which decomposes aggregate alarm exactly and yields disproportion directly. Three pre-registered hypotheses were tested across some 292,000 runs. Amplification requires a stable audience; targeting the well connected adds to it only while reach is small. A repertoire that resamples its audience each step never exceeds its own forcing, and at full reach no repertoire produces a panic at all. At the operating point, 84% of manufactured alarm is the interaction between campaign-created division and othering, and 62% of disproportion survives 250 steps after the entrepreneur withdraws. Counter-claims-making raises disproportion for 9 to 24 steps before lowering it, and lowers it only by converting the population. Disproportion is measured here against the model's own counterfactual; the model contains no real danger to measure it against.

  #v(0.7em)

  *Keywords:* moral panic; moral entrepreneurship; agent-based modelling; social networks; opinion polarization.
]

#v(1.4em)


// ─────────────────────────────────────────────────────────────────────────────
= Introduction
// ─────────────────────────────────────────────────────────────────────────────

Since Cohen's study of the mods and rockers, moral panic has named a recognisable sequence: a condition, episode, or group is defined as a threat to societal values; the definition is promoted and amplified by claims-makers; and the reaction that follows exceeds what the threat itself warrants @cohenFolkDevilsMoral1994 @goodeMoralPanicsCulture1994. Two roles drive the sequence. Moral entrepreneurs define the boundary and campaign for it @beckerOutsidersStudiesSociology1997; folk devils are the simplified figures onto which deviance is projected. The framework travels widely, and recent applications include cyber-organised crime @lavorgnaCyberorganisedCrimeCase2019, misinformation and platform activism @moranMisinformationActivismAnalyzing2023, immigration politics @zhangMoralPanicInsecurity2025, school curricula @leeds1619ProjectMoral2024, and gender quotas @shiranBacklashQuotasMoral2024.

That reach has not been matched by measurement. #cite(<goodeMoralPanicsCulture1994>, form: "prose") define panic partly by disproportion, concern in excess of what the situation warrants, and disproportion requires a comparison that empirical work can rarely make: one cannot observe how alarmed a society would have been without the claims-making that alarmed it. Since the counterfactual is unobservable, the criterion is asserted and left undemonstrated. Reviews of the field record what follows from that. Panic is invoked as self-evident while the criteria for recognising it go unstated @falkofMoralPanicDirections2020 @garlandConceptMoralPanic2008, and #cite(<hierRethinkingProblemDisproportion2024>, form: "prose") treats disproportion as the field's central unresolved problem. The same gap underlies the discipline's long-running disputes over agency, temporality, normative commitment, and how far the concept can be stretched before it stops discriminating, disagreements catalogued by #cite(<davidIdeaMoralPanic2011>, form: "prose") and, on the normative question, by #cite(<cohenWhoseSideWere2011>, form: "prose").

A second limitation concerns how the framework's elements are studied. Moral entrepreneurs, folk devils, and panic itself are usually treated as three objects with three literatures whose interaction nobody formalises. Work on networked panics has moved well beyond the mass-mediated model: #cite(<mcrobbieRethinkingMoralPanic1995>, form: "prose") rewrote it for multi-mediated societies, and #cite(<walshSocialMediaMoral2020>, form: "prose") assessed what platform communication does to societal reaction. Yet entrepreneur and folk devil are often kept as fixed statuses, when in practice stigmatised groups routinely act as entrepreneurs of their own defence @mikhaylovaFolkDevilsMoral2022 @hierFolkDevilResistance2011. The dominant instruments (discourse and framing analysis, case studies, ego-network description @mihaylovaVozmozhnostiPrimeneniyaEgosetevogo2021 @mihaylovaIzmerenieMoralnoyPaniki2022) are interpretively strong, but they are not built to show how micro-level interaction generates macro-level escalation over time.

A simulation can do what a case study cannot: run the counterfactual. It executes the same population, the same network and the same initial draws twice over, once with and once without the claims-making that is supposed to have caused the alarm, and the difference between the two is computed _disproportion_. The counterfactual also makes a second and older question answerable. Alarm in the model has two manufactured sources, one injected by claims-makers from outside and one generated by the population itself through exposure to moral disagreement, and each can be switched off independently. Four runs on one seed therefore isolate what either contributes alone, together with the alarm that exists only because both are present. Our claim concerns that third quantity: a moral panic is ignited by claims-makers and then sustained by the population they divide. The claim apportions the alarm between two sources, and the transfer between them, as Section 3.2 shows, is immediate rather than gradual. It also gives a numerical answer to a dispute that has so far been conducted rhetorically. Whether panics are held up by elite claims-makers or by the reaction of the public itself is what separates elite-driven from interactionist accounts, and neither side has been in a position to apportion the two. The research question follows: which claims-making strategies ignite moral panic, under which network structures, and once ignited, what sustains it?

The instrument is an agent-based model, and it works from the bottom up. It specifies how each individual responds to the people around them and to whoever is campaigning at them, then lets the population-level pattern follow from those responses. A run is a network of a thousand people, each holding a moral position on a contested issue and a level of alarm. Positions move as people are pulled by whichever claims-maker reaches them and by the neighbours they still find worth listening to; alarm moves as it lingers, as it is caught from others, and as it is generated by _othering_, the conversion of local moral disagreement into perceived threat. Nobody in the population decides anything. Agents respond through fixed rules, and all strategic agency sits with the two claims-makers outside the network. That division of labour is how the model addresses the micro-macro gap, since macro-level escalation is then produced by non-strategic micro-level response to strategic macro-level input. Three hypotheses, one for each phase of an episode, were fixed in writing before the runs: what ignites it, what keeps it alive, and what answering back does to it. Several of their clauses turned out to be wrong, among them both outcomes specified in advance for the third, and Section 3 prints each hypothesis as registered beside what happened.

The paper contributes three things. First, it makes the disproportionality criterion computable, so that the elite-versus-interactionist dispute becomes an apportionment between two terms. Second, it identifies the condition under which claims-making ignites anything at all, and that condition is a stable audience. Volume and structural position matter much less, which leaves universal reach as the one strategy that cannot produce a panic. Third, it supplies a mechanism for an observation the constructivist literature has long made qualitatively, that organised defence of a stigmatised position tends to intensify an episode before it ends it. Methodologically it follows the generative rationale that a social pattern is explained when a micro-specification grows it @epsteinGenerativeSocialScience2006; the nearest prior model of panic itself simulates its diffusion in an epidemic setting @guoModelingSimulatingOnline2021.


// ─────────────────────────────────────────────────────────────────────────────
= Model and methods
// ─────────────────────────────────────────────────────────────────────────────

The model has six parameters and four rules. Four parameters are global and two, depth and reach, are set per claims-maker, so a run with both actors active fixes eight numbers.#footnote[The description follows the ODD protocol (Overview, Design concepts, Details), the standard reporting checklist for agent-based models @grimmStandardProtocolDescribing2006 @grimmODDProtocolDescribing2020, in substance if not in its section order.] What the model leaves out is stated in Section 4.3.

== Entities, states, and structure

The model contains $N$ agents, a fixed undirected graph recording who can hear whom, and two external claims-makers. Each agent carries two states that change from step to step. The first is a _moral position_, written $b_i (t)$ ($b$ for belief, with the subscript naming the person and $t$ the step), which runs from $-1$, full alignment with the stigmatised position, to $+1$, full alignment with the dominant moral claim; the middle of the range stands for indifference or ambivalence. The second is _alarm_, written $a_i (t)$ and running from $0$ to $1$: how much danger this person feels is in the air. Alarm is deliberately undirected. It records how alarmed someone is and says nothing about what they fear; the object of the fear is read off jointly with their position, so that an alarmed agent near $+1$ fears the stigmatised group while one near $-1$ fears persecution. Each agent also carries a fixed _panic threshold_ $theta_i$ ($theta$ for threshold), the level of alarm past which they begin to amplify: once across it, a person is heard more loudly by everyone around them, in the way an agitated participant in a rumour is. Dispersion in those thresholds (people differ in how much alarm it takes to set them off) is the only difference between agents that the model keeps, because it fixes what share of the population is amplifying at a given level of alarm, and that share is the gain of the reinforcement loop described below @granovetterThresholdModelsCollective1978. Every symbol used in this section is collected, with its plain reading, in @tab:notation.

Structure is the primary explanatory variable of the first experiment. Three generators are used, each producing a population with the same average number of contacts per person (the _mean degree_) but a different social shape: the Watts--Strogatz small world, in which anyone can be reached in few steps and one's contacts tend to know each other @wattsCollectiveDynamicsSmallworld1998; the Holme--Kim graph, or preferential attachment with clustering @holmeGrowingScalefreeNetworks2002, which adds a few very well-connected people (hubs) while keeping those closed triangles of mutual acquaintance that plain preferential attachment lacks @barabasiEmergenceScalingRandom1999; and the Erdős--Rényi random graph @gilbertRandomGraphs1959, which has neither hubs nor triangles and therefore serves as the comparison case in which structure does nothing. Following #cite(<broidoScalefreeNetworksAre2019>, form: "prose"), the second is called hub-dominated, not scale-free. Runs keep the whole graph, isolates included, since isolation is substantively meaningful: an agent reachable only by a claims-maker occupies a real sociological position.

Two strategic actors push at this system from outside it. The _moral entrepreneur_ $D$ promotes the dominant moral claim and pulls the agents it reaches toward its own pole, $p_D = +1$; the _counter-entrepreneur_ $C$ pulls toward the opposite pole, $p_C = -1$, standing in for the niche media through which folk devils answer back @mcrobbieRethinkingMoralPanic1995. A pole is simply the position an actor argues for, and it never changes during a run. Neither actor is an agent: they have no internal state, no position in the network, and cannot themselves be alarmed. Because they stand outside it, the two sources of alarm remain separable; an actor inside the network would both cause alarm and absorb it. The symmetric design follows #cite(<mikhaylovaFolkDevilsMoral2022>, form: "prose"), for whom entrepreneur and folk devil name positions taken up within a contest and not fixed statuses of those who occupy them. The folk devil accordingly has no actor of its own. It enters as the stigmatised pole around which alarm and clustering emerge, which preserves the constructivist insight that folk devils are constituted through attribution.

Initial positions in the consensual default are drawn evenly from the narrow band $[-0.2, 0.2]$ around indifference, written $"Uniform"[-0.2, 0.2]$; the already-divided contrast draws instead from two bell curves of equal size centred on $-0.7$ and $+0.7$ with a spread of $0.15$, written $"Normal"(plus.minus 0.7, 0.15)$. Thresholds are $"Uniform"[0, 1]$, so that every level of susceptibility is equally represented, against a contrast in which everyone shares a single threshold $theta = 0.5$. Initial alarm is $"Uniform"[0, 0.1]$, low but non-zero. That baseline carries the model's sense of _warranted_ concern, so it cannot be set to zero. @tab:params lists the parameters and their operating-point values.

#figure(
  table(
    columns: (auto, 1fr, auto, auto, auto),
    align: (left + horizon, left + horizon, center + horizon, center + horizon, center + horizon),
    inset: (x: 5pt, y: 4pt),
    table.hline(stroke: 0.8pt),
    table.header(
      [*Symbol*], [*Reads as*], [*Domain*], [*Operating\ point*], [*Tested\ by*],
    ),
    table.hline(stroke: 0.4pt),
    [$epsilon$], [tolerance: how much disagreement a person still listens to], [$[0,2]$], [$0.5$], [H2],
    [$mu$], [memory: how long alarm lingers after the alarming stops], [$[0,1)$], [$0.30$], [H2],
    [$delta$], [contagion: how much alarm is caught from others], [$[0,1]$], [$0.25$], [H2],
    [$omega$], [othering: how much disagreement is itself danger], [$[0,1]$], [$0.35$], [H2],
    [$alpha_X$], [depth: how hard a claims-maker pushes those it reaches], [$[0,1]$], [$alpha_D = 0.7$], [H1, H3],
    [$rho_X$], [reach: what share it reaches per step], [$[0,1]$], [$rho_D = 0.25$], [H1, H3],
    table.hline(stroke: 0.4pt),
    [$sigma$], [anchor to initial conviction; a restoring force, hence zero], [$[0,1]$], [$0$], [---],
    [$gamma$], [how much louder an amplifying agent is heard], [$>= 1$], [$3.0$], [---],
    [$zeta$], [size of the random jitter on positions (its standard deviation)], [$>= 0$], [$0.01$], [---],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Parameters and fixed constants. The upper block is varied across runs; the lower block is held fixed and re-run at alternative values as a check. $X$ stands for either claims-maker, the entrepreneur $D$ or the counter-entrepreneur $C$. The full notation is in @tab:notation.],
) <tab:params>

== The four rules

#h4[Targeting] Each active actor $X$ reaches $n_X = min(N, ceil(rho_X N))$ agents per step, its reach $rho_X$ being read as a share of the population, so that $rho_X = 0.25$ means a quarter of it; we write $g^X_i (t) = 1$ for a person it reaches at that step and $0$ for everyone else. `random` draws a uniform subset, redrawn every step, and at $rho_X = 1$ it is mass broadcast; `hub` takes the $n_X$ highest-degree nodes; `base` takes the $n_X$ agents closest to the actor's own pole, rallying the already committed; `fixed_random` draws a uniform subset once and addresses it every step. The fourth is a measuring instrument and not a strategy. `hub` and `base` depart from `random` along two dimensions at once, in _whom_ they select and in returning to the same people every step, so separating the two requires a control that departs along one dimension only: `random` against `fixed_random` isolates the exposure schedule, and `fixed_random` against `hub` isolates degree.

#h4[Peer influence] An agent is moved only by neighbours close enough to still be worth listening to. Four pieces of notation carry this. _Moral distance_ $Delta_(i j)(t) = |b_i (t) - b_j (t)|$ is how far apart two people's positions are, so a distance of $0$ is agreement and of $2$ is the full width of the issue. $cal(N)_i$ is the set of $i$'s contacts and $d_i$ is how many of them there are. Finally, $kappa_j (t)$ is how loudly $j$ is heard: $gamma$ (three times the normal volume at the operating point) once $j$'s alarm is past its threshold, and $1$ otherwise. The net pull that $i$'s contacts exert on its position is then

$ S_i (t) = cases(
  (sum_(j in cal(N)_i) kappa_j (t) bb(1) [Delta_(i j)(t) <= epsilon] (b_j (t) - b_i (t))) / (sum_(j in cal(N)_i) kappa_j (t)) & "if" d_i > 0,
  0 & "if" d_i = 0.
) $ <eq:peer>

Read in words: average the disagreement of everyone whose position is within tolerance $epsilon$, weighting each of them by how loudly they are heard, and move that far. The bracketed indicator is a switch that counts a contact only while the gap to them stays inside tolerance; beyond it, the contact is tuned out and contributes nothing. This is bounded confidence without repulsion, following Hegselmann and Krause (2002) and #cite(<deffuantMixingBeliefsInteracting2000>, form: "prose"); #cite(<flacheModelsSocialInfluence2017>, form: "prose") survey the wider family. Agents disengage from the morally distant but are never driven away by them, which keeps divergence attributable to a single mechanism. Note that the denominator counts every contact, tuned out or not: being surrounded by people one has stopped listening to leaves less to move toward, and so shortens the distance anyone travels in a step.

#h4[Position update] Agents a claims-maker reaches are pulled toward its pole with a strength set by its _depth_ $alpha_X$ (how hard it pushes those it reaches) and by how far the person still has to travel: $I^D_i (t) = alpha_D g^D_i (t)(1 - b_i (t))$ for the entrepreneur and $I^C_i (t) = alpha_C g^C_i (t)(1 + b_i (t))$ for its opponent. The second factor shrinks as an agent approaches the pole, so an actor acting alone moves each person a fixed _fraction_ of the remaining way and can never push anyone past the end of the scale. Positions then update as

$ b_i (t+1) = "clip"_([-1,1])[ underbrace(sigma b_i (0), "anchor") + (1 - sigma)(underbrace(b_i (t), "persistence") + underbrace(S_i (t), "peers") + underbrace(I^D_i (t) - I^C_i (t), "claims-makers")) + underbrace(xi_i (t), "noise") ], $ <eq:position>

where $xi_i (t)$ is a small random jitter of size $zeta$, standing for the idiosyncratic reasons people shift a little without any social prompting, and the outer clip simply keeps positions inside the scale. Here $sigma$ is the Friedkin--Johnsen anchor weight @friedkinSocialInfluenceOpinions1990, the degree to which people are held to the conviction they started with. We set it to zero for a substantive reason. The term $sigma b_i (0)$ is a restoring force toward each agent's _pre-campaign_ position, which under a consensual start sits near zero, so any positive $sigma$ returns the population to consensus on its own timescale of $-1 slash ln(1 - sigma)$ steps, whatever $omega$ is, and dissolves the manufactured division this paper is about. The only other work the anchor would do is to prevent the trivial consensus of plain neighbour averaging @degrootReachingConsensus1974, and bounded confidence already does that. Depth appears here and nowhere else: it scales persuasion and leaves alarm untouched, so an actor is silenced by $rho_X = 0$ and never by $alpha_X = 0$.

#h4[Alarm update] Agents catch alarm; they never reason their way into it. A claims-maker enters the neighbourhood of each agent it reaches as though it were one more contact, maximally alarmed and permanently loud, which is what receiving an alarming message amounts to. Writing $m_i (t)$ for how many claims-makers reach $i$ this step (zero, one or both), the two things an agent is exposed to are _alarm exposure_ $E_i$, how alarmed its social world looks, and _othering exposure_ $Phi_i$, how much moral disagreement it is surrounded by:

$ E_i (t) = min(1, (sum_(j in cal(N)_i) kappa_j (t) a_j (t) + gamma m_i (t)) / (d_i + m_i (t))), quad
  Phi_i (t) = (sum_(j in cal(N)_i) kappa_j (t) Delta_(i j)(t) slash 2) / (sum_(j in cal(N)_i) kappa_j (t)), $ <eq:exposure>

both of which are zero for someone with no contacts whom no claims-maker reaches. Alarm then updates as a weighted sum of three things: what the agent already felt, what its world feels, and how much it disagrees with the people around it.

$ a_i (t+1) = "clip"_([0,1])[ underbrace(mu a_i (t), "memory") + underbrace(delta E_i (t), "contagion") + underbrace(omega Phi_i (t), "othering") ]. $ <eq:alarm>

Alarm exposure carries two features the results depend on. Both claims-makers raise alarm, because alarm is undirected: a message that a threat exists is alarming whoever sends it, so the defence of a stigmatised group frightens people exactly as the campaign against it does. And the denominator counts contacts, without summing their volume. Had we divided by total volume, exposure would be an average, and an average can never exceed its largest ingredient: no one could end up more alarmed than the most alarmed person they know. Dividing by the count instead lets alarmed contacts _accumulate_, so that someone with many agitated acquaintances ends up more alarmed than any one of them. That is the reinforcement described by complex contagion @granovetterThresholdModelsCollective1978 @centolaComplexContagionsWeakness2007, and it is why the expression is capped at $1$. Othering exposure, by contrast, excludes claims-makers altogether: it is the experience of being surrounded by morally distant peers, and not of receiving a message.

Together, @eq:peer and @eq:exposure produce the model's central asymmetry. A neighbour beyond an agent's tolerance contributes nothing to its position and the most to its alarm: such neighbours cannot change its mind, and they frighten it more than anyone else can. A population sorted into opposed camps therefore manufactures its own alarm, and all three hypotheses rest on that.

== Measuring panic

Alarm has two manufactured sources and each can be switched off independently: claims-making by silencing both actors, othering by setting its coefficient $omega$ to zero, which stops disagreement being frightening in itself. Every setting is therefore executed four times, in a $2 times 2$ design: with neither source, with claims-making only, with othering only, and with both. Write $overline(a)$ for the population's average alarm and mark each version with a superscript, $overline(a)^"null"$ for the world with neither source, $overline(a)^"cm"$ for claims-making only, $overline(a)^"oth"$ for othering only, and plain $overline(a)$ for the full run. The four are strictly comparable, because a single random seed fixes the network, the initial positions, the initial alarm and the thresholds. They are the same thousand people living through four different worlds. Their averages then split the total exactly, at every step:

$ overline(a) = underbrace(overline(a)^"null", "warranted")
  + underbrace(overline(a)^"cm" - overline(a)^"null", "claims-making alone")
  + underbrace(overline(a)^"oth" - overline(a)^"null", "othering alone") \
  + underbrace(overline(a) - overline(a)^"cm" - overline(a)^"oth" + overline(a)^"null", "interaction"). $ <eq:decomp>

The first term is the alarm the situation warranted anyway; the next two are what each source produces on its own; the fourth, the _interaction_, is the term the design exists to isolate. It is the alarm that arises only because both sources are present: the division an entrepreneur creates, amplified by a population that then finds its own divisions frightening. In a world where the two sources simply added up, this term would be zero, and every point below turns on the fact that it is not. One further property of the design matters for how the term should be read. Since all four worlds start identical, the interaction is exactly zero at the first step and can become non-zero only at the second, and then by a single route: the campaign has moved positions, which changes the moral distances that othering reads. Whatever the interaction later measures was therefore manufactured inside the run, and none of it is inherited from how divided the population happened to be at the start.

Disproportion is the total excess over what the situation warrants, normalised by the room available for it:

$ Pi(t) = (overline(a)(t) - overline(a)^"null" (t)) / (1 - overline(a)^"null" (t)) in [0, 1]. $ <eq:pi>

We call this the _panic index_ $Pi$ ($Pi$ for panic): at zero the population is exactly as alarmed as the same population would have been with nobody campaigning, and at one mean alarm has reached the top of its scale. A _moral panic episode_ is then a stretch of at least $W$ consecutive steps in which the index stays above a cut $Pi^*$ and the share of the population past its own alarm threshold, written $q$, stays above a second cut $q^*$. Requiring both distinguishes panic from two things it is often confused with: concern that is widespread but proportionate, where many are alarmed and little of it is excess, and the successful manipulation of a small minority, which is the reverse. In the terms of #cite(<goodeMoralPanicsCulture1994>, form: "prose"), the pair makes disproportionality operational and approximates consensus. The placement of the three cuts is conventional, so incidence is reported across a grid of all three, and we show below that the conclusions do not depend on the choice. Alongside $Pi$ we record persistence after withdrawal, mean position, mean othering exposure, and two summaries of shape. Sarle's bimodality coefficient @pfisterGoodThingsPeak2013 asks whether the population's positions form one hump or two, which is how a split into opposed camps registers as a single number. The exposure concentration $"Var"_i (sum_t g^D_i (t))$ is the variance, across people, of the number of times each was addressed over the whole run: it sits near zero when a campaign spreads its attention evenly and grows large when the campaign keeps returning to the same few, which is what tells the four repertoires apart.

The instrument stays meaningful only under two conditions. The first is bookkeeping: the three weights on alarm must not sum past one, or alarm would run off the top of its scale, and we impose this on every parameter setting we sample. The second is substantive. Contagion must stay _sub-critical_, meaning that a spark of alarm dropped into an otherwise calm population dies out instead of feeding on itself; an epidemiologist would write the condition as a reproduction number below one. Above that boundary alarm sustains itself from any spark at all, whatever anyone campaigns about, so the comparison the paper rests on stops meaning anything, since the excess no longer depends on the claims-making. The boundary is not a single number, because an alarmed contact is heard several times as loudly as a calm one and therefore counts for more than its share. We measure it at every point we report: silence both actors, switch off othering, set a few per cent of the population at full alarm, and check that the alarm dies out.

== Experimental design and verification

The operating point throughout is a Watts--Strogatz small world with $N = 1000$ and mean degree $10$; $epsilon = 0.5$, $mu = 0.30$, $delta = 0.25$, $omega = 0.35$; $sigma = 0$, $gamma = 3$, $zeta = 0.01$; the entrepreneur on `base` with $alpha_D = 0.7$ and $rho_D = 0.25$, withdrawing at $t_"off" = 150$; horizon $T = 400$. Experiment A crosses the four repertoires with the three topologies and the two initial position regimes, with $C$ silent, raising reach in fine increments and varying depth against reach on a full grid, since the two interact. Experiment B re-runs the settings that reliably ignite with $rho_D arrow 0$ at $t_"off"$, tracking @eq:decomp across the withdrawal and sweeping the alarm parameters. Experiment C is the only one in which both actors appear, $D$ withdrawing at $t_"off"$ and $C$ entering there at three configurations chosen to span the trade-off between its reach and its depth without mapping that trade-off exhaustively.

Every quantity we report is a distribution over seeds, with panic incidence as a frequency; nothing rests on a single run. At 250 seeds per setting the Monte Carlo standard error on incidence is at most $plus.minus 0.032$, which is how far a reported frequency could move if the same setting were re-run on a fresh batch of seeds; and since each seed produces all four runs the headline program is 72,990 counterfactual sets, or 291,960 simulation runs, taking 54 minutes on 15 cores.

The second hypothesis is a claim about _which_ of three ways alarm can be kept alive actually keeps it alive, so testing one input at a time will not answer it; the analysis has to apportion a single outcome among competing inputs. A variance-based sensitivity analysis does exactly that. It asks what share of the variation in an outcome, across the whole space of settings, each input is responsible for, counting the effects it has jointly with the others @sobolGlobalSensitivityIndices2001. Such a share is called a Sobol index. The one we use throughout, written $S_T$, is the _total-order_ index, which credits an input both with what it does on its own and with what it does only in combination with the rest, so that a mechanism working entirely through another is still visible. An input whose index is near one drives the outcome; one whose index is near zero contributes nothing of its own.

Our version of it departs from the standard design in two places. First, the three alarm weights cannot be drawn independently, because they must not sum past one; drawing them freely and discarding the illegal combinations would leave the survivors correlated and the apportionment invalid. We therefore split each setting into two questions that _can_ be asked independently: the _total intensity_ $s$, how strong alarm dynamics are overall, and the _split_ between memory, contagion and othering, that is, what shares of that total each of the three receives. The split is a three-way mix whose parts add to one, a budget allocated across three headings, and the geometric name for the set of such mixes is a simplex. For three parts it is a triangle: each corner is one mechanism doing all the work, and every interior point is a blend, which is how @fig:h2 plots it. Asking about the split at fixed intensity poses the sociological question directly: granted that a population is inflammable, what keeps it inflamed? Second, the noise constant $zeta$ enters as a fourth input, run over two ranges, because how far positions drift for idiosyncratic reasons competes with othering to explain what survives. Estimation uses a standard sampling design and estimator @saltelliVarianceBasedSensitivity2010 @jansenAnalysisVarianceDesigns1999, written from scratch and checked against a test function whose answers are known analytically @ishigamiImportanceQuantificationTechnique1991, which it reproduces to within $0.0025$.

That the code implements the specification is established separately from any substantive result. The technique is to strip the model down until it becomes a simpler model whose behaviour is already known, and to check that it reproduces that behaviour: switch off tolerance and the two actors and it must reduce to plain neighbour averaging, which converges to consensus; restore the anchor and it must land on the equilibrium Friedkin and Johnsen derived; keep tolerance and it must leave the number of surviving opinion clusters that the Hegselmann--Krause model leaves; hold everything homogeneous and mean alarm must settle where the analytic fixed point predicts; and on a graph with no ties at all the campaign world and the campaign-free world must coincide exactly, so that the panic index is zero by construction. All fourteen verification and property checks pass. The implementation is Python with `networkx` @hagbergExploringNetworkStructure2008 and `numpy` @harrisArrayProgrammingNumPy2020, and all randomness derives from one recorded seed through three substreams, for setup, targeting and noise: sharing a stream between targeting and noise would desynchronise the four arms, and the counterfactual would no longer hold the same population fixed.

The three hypotheses, and both possible outcomes of the third, were fixed in writing before the program was run, and where the runs contradicted a registered clause the wording has not been revised. Section 3 states each hypothesis as registered and then reports what happened.


// ─────────────────────────────────────────────────────────────────────────────
= Results
// ─────────────────────────────────────────────────────────────────────────────

The conditions of Section 2.3 hold throughout, and each buys something specific. Alarm is sub-critical at the operating point: a spark dropped into the calm population dies away to nothing, so no episode reported below is alarm feeding on itself irrespective of any campaign. The campaign-free world stays near-calm (its highest mean alarm across all runs is $0.052$), so the denominator of @eq:pi never approaches zero and the index remains well conditioned. The population also starts genuinely agreed: mean othering exposure at the outset, $overline(Phi)(0)$, which reads the average moral distance between contacts on the halved scale of @eq:exposure, is $0.067$, against $0.386$ in the divided contrast. Whatever division the runs later show, the campaign made it. The three generators are matched on mean degree ($10.00$, $9.94$, $9.88$) and differ where they are meant to. Clustering, the chance that two of a person's contacts also know each other, is $0.487$, $0.212$ and $0.010$; degree dispersion, how unequally contacts are shared out across people, is $1.00$, $12.81$ and $3.22$, for Watts--Strogatz, Holme--Kim and Erdős--Rényi respectively.

== Ignition

#registered[
  H1, as registered. Which repertoire ignites a panic depends on network topology, and ignition is amplifying but not discontinuous: $Pi > rho_D$ across the usable range, while the response stays smooth and saturating rather than jumping at a critical value. `hub` ignites fastest in hub-dominated networks and degenerates to `random` where degrees are even.
]

Amplification is the model's formal counterpart of a reaction out of proportion to its cause: a point above the diagonal $Pi = rho_D$ in panel (a) of @fig:h1 is a response larger than the forcing that produced it. It appears, though not for claims-making in general. `hub` clears the diagonal from the smallest reach tested, `base` and `fixed_random` clear it to $rho_D approx 0.4$, and `random` never clears it at any reach, running at a flat $Pi slash rho_D approx 0.18$, which is what pure injection without amplification looks like. Which curves coincide tells us why: `fixed_random` traces `base` almost exactly across the whole sweep, and the two have nothing in common except a stable audience, since the control selects uniformly at random and carries no degree signal. What amplifies is reaching _the same_ people repeatedly; whether they are also the right people is a separate question, taken up in the next paragraph. Read sociologically, a campaign turns into a panic by working on a fixed constituency, and how many people it persuades matters far less. Repetition on the same audience opens a gap between that audience and everyone else, and the gap does the alarming.

#figure(
  image("../Results/figures/fig1_h1_ignition.pdf", width: 100%),
  caption: [Ignition. (a) how much panic each of the four repertoires produces as its reach grows, on the small world, with the diagonal $Pi = rho_D$ drawn in: a curve above that line is a reaction larger than the campaign that caused it. (b) the same for `hub` alone across the three network types, with `random` repeated as a light reference, which isolates what topology does. (c) manufactured division (the interaction term) against reach, circles marking each peak, showing that it rises, peaks and then disappears. (d) $Pi$ across every combination of depth $alpha_D$ and reach $rho_D$, darker being higher, with the heavy rule drawn where a reached agent's one-step move $alpha_D (1 - overline(b))$ crosses the tolerance $epsilon = 0.5$: below that rule the campaign persuades, above it the campaign divides. All four panels read $Pi$ at $t = 199$. Mean over 250 seeds; bands are $plus.minus 1$ standard deviation across seeds.],
) <fig:h1>

The registered clause that `hub` degenerates to `random` where degrees are even is refuted, and the control identifies the mechanism `hub` was actually exploiting. On Watts--Strogatz, whose degree s.d. is $1.00$, `hub` still exceeds `random` by up to $14.8 times$. Decomposing that advantage, `random` $arrow$ `fixed_random` isolates the exposure schedule and is worth up to $7.0 times$, accounting for the whole of `hub`'s advantage at $rho_D >= 0.30$, where the control exceeds `hub`; `fixed_random` $arrow$ `hub` isolates degree and is worth a further $2.2$ to $2.5 times$ at $rho_D <= 0.10$ and nothing above $0.25$. Exposure concentration closes the argument: at $rho_D = 0.10$, $"Var"_i (sum_t g^D_i)$ is $18$ for `random` and $3600$ for `fixed_random`, the attainable maximum, but only $2272$ for `hub`, whose audience churns where degrees tie. `hub` is thus less concentrated than the control and still beats it at low reach, which is the signature of a second and independent channel. A small budget benefits from well-connected targets; a moderate one benefits only from consistency. The practical reading is that influencer recruitment buys a claims-maker something real only while it cannot afford an audience of its own; past that point the gain comes from returning to the same people, and their connectedness ceases to matter.

Topology moves `hub` and almost nothing else, which is what panel (b) of @fig:h1 isolates: its peak runs $0.475$, $0.433$ and $0.386$ on Holme--Kim, Erdős--Rényi and Watts--Strogatz, while the other three repertoires vary by less than $0.02$. The registered topology clause holds, but for that one repertoire alone.

The sharpest structure lies in the axis the hypothesis treated as secondary. Panel (d) of @fig:h1 reads row-wise. Below $alpha_D (1 - overline(b)) approx epsilon$ the whole row stays pale, running from $Pi = 0.02$ at the narrowest reach to $0.13$ at $rho_D = 0.7$, because there the entrepreneur _converts_. Reached agents stay inside their neighbours' tolerance and drag the population to the pole together, $overline(b) arrow 0.99$, with the interaction term at zero. Above the gate the rows are nearly identical to one another, the three depths $0.7$, $0.8$ and $0.9$ differing by less than $0.02$, while moving along a row changes $Pi$ six-fold and carries it to $0.44$. No reach ignites anything below the gate; above it, reach decides how large the episode becomes. Depth is a gate and reach is the dial, so access to an audience converts into panic only where the claims-making is intense enough to be disowned. A fine sweep locates the gate between $alpha_D = 0.62$ and $0.68$, where the across-seed s.d. of $Pi$ inflates from $0.014$ to $0.064$: within one cell some seeds cleave and others converge. That is the model's only knife-edge behaviour, and it sits in depth, not in reach. Substantively, the gate is the point at which a campaign stops persuading and starts estranging. A moderate claim carries its audience along with their neighbours; a claim strong enough to be disowned takes the audience out of earshot of everyone else, and only then does reach begin to matter.

Manufactured division peaks at intermediate reach and vanishes at full reach, which is the arch traced by panel (c) of @fig:h1. The interaction term peaks at $0.346$ (`fixed_random`) and $0.340$ (`base`) at $rho_D = 0.50$ and at $0.289$ (`hub`) at $rho_D = 0.20$, then collapses to $0.002$ for every repertoire at $rho_D = 1$, where all four are the same rule and exposure variance is exactly zero; panic incidence there is $0.00$ under every cut of the criterion grid. The most powerful claims-maker imaginable, reaching everyone every step, is the one that cannot divide anybody. Universal address moves the whole population together, and a population that moves together has no internal distance left to be frightened by. Alarm is manufactured by unevenness in who receives the message, and the message itself does none of that work.

The experiment leaves two further observations. Incidence rises from $0.08$ to $0.96$ between $rho_D = 0.15$ and $0.20$ while $Pi$ moves smoothly from $0.177$ to $0.234$ with an across-seed s.d. of $0.015$, which places the apparent tipping point in the instrument and not in the model. Flattening the threshold distribution then lowers $Pi$ by 35 to 40 per cent at every reach while leaving the curve's shape and peak untouched: dispersion sets the gain of the reinforcement loop. Of the nine registered clauses of H1, six held, two held only in part (amplification and the role of dispersion), and one, the degeneration of `hub`, was refuted.

== Handover

#registered[
  H2, as registered. The claims-making-alone term rises first and then plateaus, while the interaction term rises later and overtakes it. After the entrepreneur withdraws, $Pi$ remains elevated for a duration governed by othering rather than by passive decay: persistence is maximised near the $omega$ vertex of the alarm simplex, the split carries a larger total Sobol index than the intensity does, and $Pi$ decays to zero when $omega = 0$ but to a positive floor when $omega > 0$.
]

The apportionment is not close. At the operating point the entrepreneur's own signal contributes $0.041$ to mean alarm and the division it manufactures contributes $0.246$, a ratio of $5.94$ to one reached within twenty steps and stable for the rest of the campaign (@tab:h2, @fig:h2 panel (a)): 14 per cent of the manufactured alarm is the claims-making signal, 2 per cent is pre-existing division, and 84 per cent is the interaction. The two ways the interaction could arise separate cleanly. Alarm might be running over disagreement that already existed and was merely made more audible, or over disagreement the campaign itself produced; comparing mean othering exposure in the full run with the othering-only run at the step before withdrawal ($0.189$ against $0.006$) puts 97 per cent of it in the second category. The entrepreneur's durable product is the division, and not the alarm it broadcasts.

#figure(
  table(
    columns: 7,
    align: (center + horizon, center, center, center, center, center, center),
    inset: (x: 5pt, y: 4pt),
    table.hline(stroke: 0.8pt),
    table.header([$t$], [warranted], [claims\ alone], [othering\ alone],
                 [_interaction_], [$Pi$], [$q$]),
    table.hline(stroke: 0.4pt),
    [2], [0.0165], [0.0272], [0.0198], [*0.0366*], [0.0850], [0.100],
    [10], [0.0001], [0.0413], [0.0050], [*0.2182*], [0.2646], [0.260],
    [20], [0.0000], [0.0414], [0.0046], [*0.2461*], [0.2921], [0.285],
    [149], [0.0000], [0.0415], [0.0046], [*0.2430*], [0.2890], [0.288],
    table.hline(stroke: 0.3pt),
    [155], [0.0000], [0.0024], [0.0046], [*0.2378*], [0.2448], [0.259],
    [399], [0.0000], [0.0000], [0.0046], [*0.1745*], [0.1791], [0.188],
    table.hline(stroke: 0.8pt),
  ),
  caption: [The decomposition of @eq:decomp across withdrawal, mean over 250 seeds. The entrepreneur withdraws at $t_"off" = 150$; the rule marks that step. $q$ is the share of the population past its threshold.],
) <tab:h2>

The registered _ordering_, however, fails. The interaction overtakes claims-alone at $t = 2$ (the earliest step at which Section 2.3 permits it to be non-zero) in 250 of 250 seeds, and at every one of eight depths spanning the gate. There is no regime in which the panic belongs to the entrepreneur for a while and to the population later, because at $alpha_D > epsilon$ ties are severed on contact: the division is complete on the first step and othering works on the second. The composition claim survives; the phase story does not. That matters for how the finding should be read. Ours is an accounting statement about where the alarm comes from, and it carries no chronology in which the entrepreneur holds the episode up alone before the public takes over.

The division outlives the entrepreneur that made it. Claims-alone falls to zero within five steps of withdrawal, and 250 steps later $Pi$ retains 62 per cent of its value at withdrawal; in 210 of the 250 seeds it was still elevated when the run ended, so those persistence figures are lower bounds on the true durations. The floor is made of othering and nothing else. Raising the othering weight while holding the other two fixed, so that the population's total capacity for alarm cannot change, moves what remains 250 steps after withdrawal from exactly zero to $0.286$; panel (b) of @fig:h2 puts the two moments side by side, $Pi$ at withdrawal and $Pi$ 250 steps later, against $omega$. Where disagreement is not itself experienced as danger, the episode ends with the campaign; where it is, the campaign is no longer needed.

#figure(
  image("../Results/figures/fig2_h2_handover.pdf", width: 100%),
  caption: [Handover. (a) the four terms of @eq:decomp through the run, the dotted vertical marking the entrepreneur's withdrawal and the arrow the 5.94-to-one ratio of interaction to claims-alone; the gap between those two curves is the finding. (b) how much panic there is at withdrawal, and how much is still there 250 steps later, plotted against the othering weight $omega$ with $mu + delta$ held fixed, so that only the mix changes and not the population's total capacity for alarm. (c) what survives to the end of the run, $Pi(399)$, at each of 45 points on the triangle of alarm splits described in Section 2.4, the circle marking the maximum and the crosses the four points discarded for failing the sub-criticality probe. (d) total-order Sobol indices for the three reparameterised inputs, the share of the variation each is responsible for, with a pair of bars per input for the two outcomes: how much panic persists, and when the transfer happens. Almost everything sits on one input, the othering-versus-contagion balance.],
) <fig:h2>

That dependence sits in the _mix_ between the three alarm mechanisms and not in their total strength, and two independent instruments say so. The first scans the mix directly, and panel (c) of @fig:h2 is the result: holding total intensity fixed, we walk over 45 combinations of memory, contagion and othering, one point of the triangle each, and read off how much alarm survives at every one of them. Four of them have to be thrown out first, and the reason nearly reversed the result. Those four sit close to pure contagion, where alarm sustains itself regardless of any campaign, and they show the highest surviving alarm in the whole scan ($0.585$, against $0.097$ at pure othering). Plotting the scan without removing them would read as a refutation of the hypothesis; removing them without saying so would confirm it for the wrong reason. Among the 41 combinations that pass, the maximum sits exactly at pure othering. The second instrument is the variance decomposition described in Section 2.4, drawn in panel (d) of @fig:h2 as one bar per input. It shares none of the first one's assumptions, gives the same answer, and locates it more sharply. The split turns out to be carried by one of its two coordinates alone, the balance between othering and contagion, which scores $S_T = 0.993$ for what survives and $1.004$ for the timing of the transfer. The other coordinate, the balance between memory and the remaining two, scores exactly zero on both, and the overall intensity of alarm scores three to four per cent. How long alarm lingers in an individual therefore makes no difference whatever to persistence; what decides it is whether the alarm circulating in the population is caught from others or generated by disagreement. An index slightly above one is estimation error and not a share exceeding the whole.

That result comes with one scope condition, and it is the sharpest limit in the study. With the drift of individual positions added as a fourth input, othering still explains essentially everything ($1.002$ against $0.022$) while drift stays below about twice its default; over a range five times the default the ordering _reverses_, to $0.389$ against $0.750$. The mechanism is intuitive once stated: if people's positions wander enough, someone who had drifted out of a neighbour's tolerance wanders back into it, the groups the campaign separated re-merge, and no permanent division is left for othering to feed on. Drift therefore governs what survives and leaves the timing of the transfer alone. The permanence of manufactured division depends on moral positions being fairly stable, and how stable they really are is not a question this model can answer. The anchor competes through the same channel: at $sigma = 0.05, 0.10, 0.20$ measured persistence is 13, 9 and 4 steps against the $-1 slash ln(1 - sigma)$ prediction of 19.5, 9.5 and 4.5, and the floor disappears.

The registered clauses on tolerance and on the polarised regime need qualification. Low tolerance was predicted to bring the handover forward; the direction holds but there is no gradient, since $Pi(149)$ runs $0.320$ to $0.289$ across $epsilon <= 0.5$ and collapses to $0.045$ with no handover at all for $epsilon >= 0.7$. Tolerance and depth are one gate seen from two sides, $epsilon approx alpha_D (1 - overline(b))$. The polarised regime, predicted to hand over earlier with a smaller interaction, instead produces the largest $Pi(149)$ in the study ($0.566$) with the smallest interaction ($0.024$) and an othering-alone term of $0.500$: almost all of its alarm is division that existed before anyone acted. An already-divided population needs less entrepreneurship, but the cell is an attenuated test, and avoiding that attenuation is why the consensual default exists.

== Defence

#registered[
  H3, as registered, with both outcomes fixed in advance. A counter-entrepreneur acts through an immediate cost scaling with $rho_C$ and a delayed benefit scaling with $alpha_C$ that is not guaranteed in sign. _Branch 1:_ broad-and-shallow lowers $Pi$ while narrow-and-deep raises it, so defence works but only through reach. _Branch 2:_ no configuration lowers $Pi$, so counter-claims-making is structurally self-defeating in this model.
]

Neither branch occurred. Every configuration raises $Pi$ above the undefended baseline for its first 9 to 24 steps and lowers it permanently thereafter; panel (a) of @fig:h3 shows the three defended runs and the undefended baseline together, and panel (b) subtracts the baseline from each, so that the moment a defence starts helping is the moment its curve crosses zero. Broad and shallow ($alpha_C = 0.15$, $rho_C = 0.60$) overshoots by $0.077$ for nine steps and ends at $Pi(399) = 0.106$; narrow and deep ($0.90$, $0.10$) overshoots by $0.239$ for 24 steps and ends at $0.020$; matched to $D$'s values ($0.70$, $0.25$) overshoots by $0.135$ for eleven steps and ends at $0.045$, against an undefended baseline of $0.179$. All three lower $Pi$ at the horizon, in 95 to 98 per cent of seeds. Whether defence works has no single answer, because the difference from the undefended baseline changes sign at a step that depends on the configuration: the endpoint says defence works, the transient says it backfires, and both are true of the same run. A directional question about a dynamic process needs a time attached to it, and H3, as we registered it, did not have one.

The ordering of the three configurations carries the substance. The largest overshoot belongs to narrow and deep, the configuration with the lowest reach and therefore the smallest immediate cost, which rules out the first channel. The second channel produces it: pulling agents toward $p_C$ narrows moral distance only if it moves them toward the population's bulk, and at withdrawal the bulk sits at $overline(b) = +0.29$. Taking a tenth of the population to $-1$ in a single step does the opposite, driving mean othering exposure from $0.190$ to $0.309$ and $Pi$ to $0.467$, 61 per cent above what the panic would have been had nobody answered back. The defence of the stigmatised position, mounted intensively on a small base, is briefly the most panic-generating act in the study. The gate at work is the one that governs ignition, operated from the other side: $alpha_C = 0.15$ never exceeds tolerance and $overline(Phi)$ falls immediately, while $alpha_C = 0.90$ severs ties on contact and cleaves the population again before healing it.

#figure(
  image("../Results/figures/fig3_h3_defense.pdf", width: 100%),
  caption: [Defence. (a) $Pi$ through $C$'s entry, for the three defended configurations and the undefended baseline. (b) each defended configuration with the baseline subtracted, so that zero is "the defence changed nothing" and the marked crossings are where it starts to help. (c) each run as a path across the $(overline(b), Pi)$ plane, from withdrawal (star) to the horizon (dot), which shows the fall in panic arriving together with the conversion of the population. (d) what is left at the horizon, $Pi(399)$, plotted against each of $C$'s two levers one at a time, with the guide $Pi = 0.18 rho_C$ drawn in. Mean over 250 seeds, 125 in panel (d).],
) <fig:h3>

The eventual reduction works by conversion. In all three configurations $Pi$ falls because $overline(b)$ goes to $-0.99$ and mean othering exposure collapses to $0.005$, the value of a population with nothing left to other. Panel (c) of @fig:h3 is where this is easiest to see: it plots each run as a path across the plane of mean position against panic, from the common start at withdrawal (star) to the end of the run (dot). The three defended paths all travel to the far left and end there, with the population converted; the undefended run holds its position and simply decays in place, which is the persistence of Section 3.2 seen from another angle. The counter-entrepreneur does not calm anyone; it wins totally, and a population that agrees about everything has no moral distance to be alarmed by. That is the only route the model leaves open, since no message in it can say _there is no threat_: alarm falls only when there is nothing left to disagree about. The finding is therefore conditional on that exclusion and is not a claim about what real counter-campaigns can achieve; Section 4.3 names the extension that would settle it.

The residue at the horizon is the price of speaking. Moving each of the counter-entrepreneur's two levers on its own, as panel (d) of @fig:h3 does, residual disproportion is $approx 0.18 rho_C$, running $0.020$ to $0.185$ as $rho_C$ goes from $0.10$ to $1.00$, and flat in depth at $0.087$ to $0.088$ across $alpha_C$. It depends on how many people the defence talks to, and not at all on how hard it argues. Every claims-maker enters the alarm neighbourhood of everyone it reaches as a maximally alarmed contact, and alarm is undirected, so once the population is converted that contact is all that is left. A defence cannot lower the panic index below what its own broadcasting costs, and the wide campaign of reassurance ends with five times the residual alarm of the narrow one, not because it reassures worse but because it keeps talking to more people.

== Robustness

The headline numbers are invariant to population size ($Pi(149) = 0.292$, $0.292$, $0.293$ at $N = 500, 1000, 2000$, with only the across-seed dispersion moving, roughly as $N^(-1 slash 2)$) and to the update scheme (updating agents one at a time in random order, instead of all together, moves it by $0.010$, inside that dispersion). Replication on two public networks @leskovecGraphEvolutionDensification2007 @mcauleyDiscoveringSocialCircles2014, each accompanied by the three generators re-run at its own realised size and mean degree, shows that the parameters, not the graph, decide the episode produced _while an entrepreneur is acting_: across eight rows spanning an eightfold range of mean degree, $Pi(149)$ lies between $0.227$ and $0.270$. Structure decides what survives. In the dense graph it decides nothing, all four versions landing between $0.191$ and $0.198$; in the sparse one it decides a factor of twenty, and it does so in strict order of how likely two of a person's contacts are to know each other: $0.135$, $0.100$, $0.072$ and $0.006$ as that likelihood falls from $0.53$ to almost nothing. The mechanism is visible in the rules. Bounded confidence cuts the population into groups, and a group holds together only while its members reinforce one another faster than drift pulls them apart; mutual acquaintance supplies that reinforcement. Sparse and unacquainted is the one combination in which manufactured division fails to outlive the campaign.

The instrument needed two checks of its own. The polarisation reported here is not boundary pile-up: the interior bimodality coefficient, taken after dropping every agent pinned at a pole, agrees with the raw one to three decimals, and a bound that can never pin anyone leaves $Pi$ within $0.008$. The counterfactual-validity horizon (where re-drawing the position noise moves one arm by more than a tenth of the effect being resolved) falls between $t = 191$ and $t = 289$ in three of five audited seeds, so $Pi(399)$ is reported as a distribution over seeds and never as a trajectory.


// ─────────────────────────────────────────────────────────────────────────────
= Discussion
// ─────────────────────────────────────────────────────────────────────────────

== What the apportionment settles

Whether panics are held up by elite claims-makers or by the reaction of the public itself is disputed @goodeMoralPanicsCulture1994 @mcrobbieRethinkingMoralPanic1995, and the dispute has stayed rhetorical for want of any way to apportion the two. The four-run design apportions them, 14 per cent to 2 per cent to 84 per cent.

Neither camp is right as usually stated. The entrepreneur is _necessary_: where nobody campaigns nothing happens, and where the campaign is too mild to be disowned nothing happens either. It is also nearly irrelevant to the size of what follows. Its achievement is to divide the population far enough that alarm becomes self-sustaining, after which it is no longer needed. That has a consequence for how panics end, or fail to. The claims-maker cannot undo what it started, because the excess alarm no longer rests on the campaign; only a population for whom disagreement is not in itself frightening will shed that alarm entirely. Any intervention therefore has an object other than "stop the campaign", and the model names what an empirical study would have to measure: how morally far apart people are from those they actually talk to, in place of how much campaigning there is. The mechanism has a cousin in the cascade literature, where public reaction outruns the information that started it @kuranAvailabilityCascadesRisk1999. The two differ in what does the reinforcing: information and reputation there, disagreement itself here.

== Three predictions for empirical research

#h4[Ignition depends on repeated exposure to the same audience] The mass broadcaster is, on this model, structurally the worst available moral entrepreneur. A campaign that reaches everyone equally leaves nobody more exposed than anyone else, and the population then moves as one: no division is manufactured and no episode occurs under any reading of the criterion. A claims-maker becomes dangerous by addressing some people and not others, repeatedly, so the fragmentation of audiences belongs to the mechanism itself and not merely to the setting in which the mechanism runs. The prediction is uncomfortable for a common intuition about mass media, since it implies that the mass-press episodes of the classic literature @cohenFolkDevilsMoral1994 and contemporary platform cases @carlsonFakeNewsInformational2020 @walshSocialMediaMigration2023 are doing different things under one label, and it makes the difference measurable, through the unevenness of exposure and not its volume. One caution comes from the same control. Since most of what targeting the well-connected achieves is achieved just as well by a fixed audience chosen at random, targeting by connectedness is a weak stand-in for algorithmic amplification, and nothing here licenses a claim about platform ranking.

#h4[Local density decides whether a panic outlives its campaign] Across two real networks and their matched synthetic counterparts, how large an episode grows while the campaign runs barely depends on the network at all; the network governs instead how much of the episode is left afterwards, and in the sparse case that is decided by how likely two of a person's contacts are to know one another. The mechanism is the one described in the results: division survives only inside groups whose members hold each other in place, and mutual acquaintance does the holding. The comparative prediction is direct. Two societies with the same campaigning, the same tolerance for disagreement and the same susceptibility to alarm will differ in whether the panic outlives the campaign, according to how tightly knit their everyday social ties are. This came from the real networks; no synthetic generator reproduced it.

#h4[Answering back intensifies the episode before it ends it] The organised defence of a stigmatised position raises disproportion for its first 9 to 24 steps, and most when it is most committed. The constructivist literature has long described defence and resistance as part of what escalates an episode @hierFolkDevilResistance2011 @zielinskaPolarizingMoralPanics2022, and the model supplies a mechanism involving neither tone nor provocation nor backlash psychology, none of which exist here. It is arithmetic on moral distance: the defence's own converts become the population's most distant neighbours, and such distance frightens @ameryOtheringPeakingPopulism2025.

A methodological warning belongs beside these. Panic incidence in our runs jumps where the underlying disproportion moves smoothly, so empirical episode counts, which apply coding rules to continuous public reaction, may inherit their sharpness from the coding rule.

== What bounds the results

The hard ceiling is set by what the panic index means. It measures alarm in excess of what the _same population in the same model_ would have felt with nobody campaigning, and not in excess of any real danger, because the model contains no danger to be in excess of. We have given the disproportionality criterion a definite structure and made it computable; we have not made it decidable for any actual episode @hierRethinkingProblemDisproportion2024, and no amount of further computation or better data would move that line.

Five things are left out. Networks do not rewire, which is the most consequential omission, since unfriending, blocking and deplatforming change who hears whom and the model holds that fixed; it is also why nobody in this model is actively repelled by the morally distant, because on a network that cannot change, being pushed away and sorting oneself away cannot be told apart. The model therefore under-states how far a population comes apart, without mis-attributing it. There is no algorithm and no recommender. Nobody can reassure anyone: every claims-maker arrives as one more frightened voice, and no message in the model says _there is no threat_, which makes the finding that defence works only by winning outright a property of what we built as much as a result about counter-campaigns. Panics leave no institutions here, only residual attitudes, so the model can show an episode outlasting its cause but not hardening into law or enforcement. Claims-makers also do not learn, which is why the defence in our third experiment gets a long uninterrupted run that no real contest would grant; the early overshoot is far more robust to this than the endpoint is.

Three scope conditions travel with the results. The persistence finding holds for a population with no pull back toward its pre-campaign convictions; give people such a pull and that pull, displacing othering, governs how long the alarm lasts, which is the reverse of what we claim. It holds while individual positions stay reasonably stable; let them drift several times as much and the drift explains more of what survives than othering does, and how much real moral positions drift is a question this model cannot settle. The accounting is also interpretable only from a population that starts out agreed, which matters for any empirical extension: measure the starting positions of a real population and it would usually land in the divided case, where alarm over pre-existing disagreement swamps the term we are trying to isolate.

The last limitation is structural: the parameter count advertises more than the model has. Six parameters turn out, in the runs, to be roughly three live ones: the single gate formed jointly by how hard a campaign pushes and how much disagreement people tolerate; how widely it reaches, which helps up to a point and then hurts; and how far disagreement is itself experienced as danger, which decides whether anything survives. How long alarm lingers in an individual explains almost none of the variation; how much is caught from others matters mainly by keeping the system below the self-sustaining boundary; and the spread of thresholds raises or lowers everything without changing its shape. We take that for parsimony and not a defect, but a reader who expects six independent levers will be misled.

Nothing here is a test of the model against the world. Three things would make it one: a network of _moral communication_, whose ties carry disagreement about a contested issue and not co-authorship or friendship @mihaylovaVozmozhnostiPrimeneniyaEgosetevogo2021; measured initial positions on that issue @mihaylovaIzmerenieMoralnoyPaniki2022; and an external threat referent, which better data cannot supply.


// ─────────────────────────────────────────────────────────────────────────────
= Conclusion
// ─────────────────────────────────────────────────────────────────────────────

Moral panic research has a definitional criterion it cannot apply, because disproportion requires a comparison with a world in which the claims-making did not happen and that world is not observable. A simulation can run it, and running it turns a standing disagreement in the field into an arithmetic question with an answer: 84 per cent of the alarm a campaign manufactures comes from the division it created and the population's fear of that division, against 14 per cent for the campaign's own signal.

The three results that generalise beyond this parameterisation are negative in form. Claims-making that reaches everyone cannot produce a panic, because manufactured division requires unequal exposure; claims-making too shallow to be disowned cannot produce one either, because it persuades instead of dividing; and answering back cannot lower alarm without first raising it, because the only channel left open for lowering it is the elimination of disagreement. If moral panics are becoming easier to start, the reason is not that reach has increased.

The concept was built around a comparison that remains uncomputed. Our index measures excess against the model's own campaign-free world, and no run of it can say that a real episode was out of proportion to a real danger; the criterion is made computable here, not decidable. Two extensions strike where the results are weakest. The first is an actor able to lower alarm directly, and not only by winning the argument, since our defence finding is conditional on no such actor existing. The second is a social network that changes as the episode runs, since every simplification in the present design pushes in the same direction, toward _under_-stating how far a population can come apart.


// ─────────────────────────────────────────────────────────────────────────────
#set heading(numbering: none)
= Appendix: notation
// ─────────────────────────────────────────────────────────────────────────────

Every symbol used in the paper, with the thing it stands for. Latin letters denote
people, their states and their networks; Greek letters denote the parameters that
govern how they behave.

#show figure: set block(breakable: true)

#figure(
  table(
    columns: (auto, auto, 1fr),
    align: (center + horizon, left + horizon, left + horizon),
    inset: (x: 5pt, y: 3.5pt),
    table.hline(stroke: 0.8pt),
    table.header([*Symbol*], [*Name*], [*What it stands for*]),
    table.hline(stroke: 0.4pt),

    table.cell(colspan: 3)[*People and what they carry*],
    [$N$], [population], [how many people are in a run; 1,000 throughout],
    [$i$, $j$], [a person, a contact], [$i$ is whoever is being updated, $j$ one of the people $i$ can hear],
    [$t$], [step], [one round of communicative exposure; read as earlier and later, never as days or weeks],
    [$b_i (t)$], [moral position], [_b for belief_: $-1$ is full alignment with the stigmatised position, $+1$ with the dominant moral claim, the middle indifference],
    [$a_i (t)$], [alarm], [_a for alarm_: how much danger this person feels is in the air, from $0$ to $1$; it does not record _what_ they fear],
    [$theta_i$], [panic threshold], [_#sym.theta for threshold_: the level of alarm past which this person starts amplifying],
    [$kappa_j (t)$], [social volume], [how loudly $j$ is heard: $gamma$ times normal once past their threshold, otherwise normal],
    [$overline(a)$, $overline(b)$, $overline(Phi)$], [population averages], [a bar means the average across everyone],

    table.hline(stroke: 0.3pt),
    table.cell(colspan: 3)[*The network*],
    [$cal(N)_i$], [contacts], [the set of people $i$ can hear],
    [$d_i$], [degree], [how many contacts $i$ has],
    [$⟨k⟩$], [mean degree], [average number of contacts per person; 10 at the operating point],
    [$Delta_(i j)(t)$], [moral distance], [how far apart two people's positions are: $0$ is agreement, $2$ is opposite poles],

    table.hline(stroke: 0.3pt),
    table.cell(colspan: 3)[*The claims-makers*],
    [$D$, $C$], [entrepreneur, counter-entrepreneur], [the two campaigners; outside the network, and never alarmed themselves],
    [$p_D$, $p_C$], [poles], [the position each argues for, $+1$ and $-1$],
    [$rho_X$], [reach], [_#sym.rho for reach_: the share of the population an actor addresses each step],
    [$n_X$], [audience size], [how many people that share works out to, $ceil(rho_X N)$ of them],
    [$alpha_X$], [depth], [_#sym.alpha for the strength of the ask_: how far toward its own pole an actor moves those it reaches],
    [$g^X_i (t)$], [reached or not], [$1$ if actor $X$ reaches $i$ this step, $0$ otherwise],
    [$m_i (t)$], [messages received], [how many claims-makers reach $i$ this step: none, one, or both],
    [$t_"off"$, $T$], [withdrawal, horizon], [the step at which the entrepreneur stops (150) and the last step of the run (400)],

    table.hline(stroke: 0.3pt),
    table.cell(colspan: 3)[*Quantities inside the rules*],
    [$S_i (t)$], [peer pull], [the net push $i$'s contacts exert on its position],
    [$I^X_i (t)$], [campaign pull], [the push a claims-maker exerts on someone it reaches],
    [$E_i (t)$], [alarm exposure], [how alarmed $i$'s social world looks, claims-makers included],
    [$Phi_i (t)$], [othering exposure], [_#sym.Phi for the experience of disagreement_: how morally distant the people around $i$ are],
    [$xi_i (t)$], [position noise], [small idiosyncratic drift, the reasons people shift for no social reason],

    table.hline(stroke: 0.3pt),
    table.cell(colspan: 3)[*Parameters (Table 1)*],
    [$epsilon$], [tolerance], [how much disagreement a person still listens to before tuning someone out],
    [$mu$], [memory], [how much of yesterday's alarm a person carries into today],
    [$delta$], [contagion], [how much alarm is caught from the people around one],
    [$omega$], [othering], [how far being surrounded by disagreement is itself experienced as danger],
    [$sigma$], [anchor], [how strongly people are held to the conviction they began with; zero throughout],
    [$gamma$], [amplification], [how much louder an alarmed person is heard],
    [$zeta$], [drift], [the size of the random jitter on positions],

    table.hline(stroke: 0.3pt),
    table.cell(colspan: 3)[*Measurement*],
    [$overline(a)^"null"$], [the campaign-free world], [average alarm with neither claims-making nor othering],
    [$overline(a)^"cm"$, $overline(a)^"oth"$], [one source only], [average alarm with claims-making alone, and with othering alone],
    [$Pi(t)$], [panic index], [_#sym.Pi for panic_: how much of the alarm is excess over the campaign-free world, from $0$ to $1$],
    [$q(t)$], [amplifying share], [what fraction of the population is past its own alarm threshold],
    [$Pi^*$, $q^*$, $W$], [the episode cuts], [how high, how widespread and for how long alarm must run to count as an episode],
    [$"Var"_i (sum_t g^D_i (t))$], [exposure concentration], [how unevenly the campaign spread its attention: near zero when everyone was addressed about equally, large when it kept returning to the same few],
    [BC], [bimodality coefficient], [whether the population's positions form one hump or two; the number in which a split into opposed camps shows up @pfisterGoodThingsPeak2013],
    [$s$; $(p_mu, p_delta, p_omega)$], [intensity; mix], [how strong alarm dynamics are overall, and how that total is divided between memory, contagion and othering],
    [$S_T$], [total-order Sobol index], [the share of an outcome's variation an input is responsible for, counting what it does jointly with the other inputs],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Notation, grouped by what it describes.],
) <tab:notation>


// ─────────────────────────────────────────────────────────────────────────────
// References
// ─────────────────────────────────────────────────────────────────────────────

#bibliography(
  ("../Moral Panic.bib", "../Computational Methods.bib"),
  style: "american-sociological-association.csl",
  title: "References",
)
