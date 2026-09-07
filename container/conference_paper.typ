// ============================================================
// conference_paper.typ
// Agent-Based Modelling of "Moral Entrepreneurship" and the
// Dynamics of Moral Panics in Social Networks
//
// Bibliographies:  Moral Panic.bib           (Zotero export, substantive)
//                  Computational Methods.bib (Zotero export, methods)
// Citation style:  american-sociological-association.csl (this folder)
//
// Spelling: British ("modelling", "defence", "recognise"), following the title.
// Self-contained: no deposit, no pointers outside this text. One appendix (notation).
//
// Self-contained folder: all assets sit next to this file (Typst web app ready).
//   typst compile conference_paper.typ
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

  *Abstract.* Disproportion belongs to the definition of moral panic and is almost never measured: no one can observe how alarmed a population would have been without the claims-making that alarmed it. This paper makes that comparison computable. We specify an agent-based model in which 1,000 networked agents carry two coupled states, a moral position and a level of alarm, updated through bounded confidence, in which people are moved only by those they still find close enough to listen to; threshold contagion, in which alarm is caught from others and the alarmed are heard more loudly; and othering, the conversion of local moral disagreement into perceived threat. Two claims-makers act on the population from outside. Every setting is run four times on one seed in a $2 times 2$ design (claims-making on/off $times$ othering on/off), which decomposes aggregate alarm exactly and yields disproportion directly. Three pre-registered hypotheses were tested across some 292,000 runs. Amplification requires a stable audience; targeting the well connected adds to it only while reach is small. A targeting strategy that resamples its audience each step never exceeds its own forcing, and at full reach no strategy produces a panic at all. At the operating point, 84% of manufactured alarm is the interaction between campaign-created division and othering, and 62% of disproportion survives 250 steps after the entrepreneur withdraws. Counter-claims-making raises disproportion for 9 to 24 steps before lowering it, and lowers it only by converting the population. Disproportion is measured here against the model's own counterfactual; the model contains no real danger to measure it against.

  #v(0.7em)

  *Keywords:* moral panic; moral entrepreneurship; agent-based modelling; social networks; opinion polarization.
]

#v(1.4em)


// ─────────────────────────────────────────────────────────────────────────────
= Introduction
// ─────────────────────────────────────────────────────────────────────────────

Since Cohen's study of the mods and rockers, moral panic has named a recognisable sequence: a condition, episode, or group is defined as a threat to societal values; the definition is promoted and amplified by claims-makers; and the reaction that follows exceeds what the threat itself warrants @cohenFolkDevilsMoral1994 @goodeMoralPanicsCulture1994. Two roles drive the sequence. Moral entrepreneurs define the boundary and campaign for it @beckerOutsidersStudiesSociology1997; folk devils are the simplified figures onto which deviance is projected. The framework travels widely, and recent applications include cyber-organised crime @lavorgnaCyberorganisedCrimeCase2019, misinformation and platform activism @moranMisinformationActivismAnalyzing2023, immigration politics @zhangMoralPanicInsecurity2025, school curricula @leeds1619ProjectMoral2024, and gender quotas @shiranBacklashQuotasMoral2024.

That reach has not been matched by measurement. #cite(<goodeMoralPanicsCulture1994>, form: "prose") define panic partly by disproportion, concern in excess of what the situation warrants, and disproportion requires a comparison that empirical work can rarely make: one cannot observe how alarmed a society would have been without the claims-making that alarmed it. Since the counterfactual is unobservable, the criterion is asserted and left undemonstrated. Reviews of the field record what follows from that. Panic is invoked as self-evident while the criteria for recognising it go unstated @falkofMoralPanicDirections2020 @garlandConceptMoralPanic2008, and #cite(<hierRethinkingProblemDisproportion2024>, form: "prose") treats disproportion as the field's central unresolved problem. The same gap underlies the discipline's long-running disputes over agency, temporality, normative commitment, and how far the concept can be stretched before it stops discriminating, disagreements catalogued by #cite(<davidIdeaMoralPanic2011>, form: "prose") and, on the normative question, by #cite(<cohenWhoseSideWere2011>, form: "prose").

A second limitation concerns how the framework's elements are studied. Moral entrepreneurs, folk devils, and panic itself are usually treated as three objects with three literatures whose interaction few formalise. Work on networked panics has moved well beyond the mass-mediated model: #cite(<mcrobbieRethinkingMoralPanic1995>, form: "prose") rewrote it for multi-mediated societies, and #cite(<walshSocialMediaMoral2020>, form: "prose") assessed what platform communication does to societal reaction. Yet entrepreneur and folk devil are often kept as fixed statuses, when in practice stigmatised groups routinely act as entrepreneurs of their own defence @mikhaylovaFolkDevilsMoral2022 @hierFolkDevilResistance2011. The dominant instruments (discourse and framing analysis, case studies, ego-network description @mihaylovaVozmozhnostiPrimeneniyaEgosetevogo2021 @mihaylovaIzmerenieMoralnoyPaniki2022) are interpretively strong, but they are not built to show how micro-level interaction generates macro-level escalation over time.

A simulation can do what a case study cannot: run the counterfactual. It executes the same population, the same network and the same initial draws twice over, once with and once without the claims-making that is supposed to have caused the alarm, and the difference between the two is computed disproportion. The research question follows: which claims-making strategies ignite moral panic, under which network structures, and once ignited, what sustains it?

The instrument is an agent-based model, specified in full in Section 2. A run is a network of a thousand people, each holding a moral position on a contested issue and a level of alarm. Positions move as people are pulled by whichever claims-maker reaches them and by the neighbours they still find worth listening to; alarm moves as it lingers, as it is caught from others, and as it is generated by _othering_, the conversion of local moral disagreement into perceived threat. Nobody in the population decides anything. Agents respond through fixed rules, and all strategic agency sits with the two claims-makers outside the network. That division of labour is how the model addresses the micro-macro gap, since macro-level escalation is then produced by non-strategic micro-level response to strategic macro-level input. Three hypotheses, one for each phase of an episode, were fixed in writing before the runs: what ignites it, what keeps it alive, and what answering back does to it. Several of their clauses turned out to be wrong, and Section 3 prints each hypothesis as it was registered beside what actually happened.

The paper contributes three things. First, it makes the disproportionality criterion computable, so that the elite-versus-interactionist dispute becomes an apportionment between two terms. Second, it identifies the condition under which claims-making ignites anything at all, and that condition is a stable audience. Volume and structural position matter much less, which leaves universal reach as the one strategy that cannot produce a panic. Third, it supplies a mechanism for an observation the constructivist literature has long made qualitatively, that organised defence of a stigmatised position tends to intensify an episode before it ends it. Methodologically it follows the generative rationale that a social pattern is explained when a micro-specification grows it @epsteinGenerativeSocialScience2006; the nearest prior model of panic itself simulates its diffusion in an epidemic setting @guoModelingSimulatingOnline2021.


// ─────────────────────────────────────────────────────────────────────────────
= Model and methods
// ─────────────────────────────────────────────────────────────────────────────

An agent-based model is a description of one person's behaviour, executed a thousand times over. We write down how a single individual responds to the people around them and to whoever is campaigning at them, hand a thousand individuals those same rules, and let them act on one another for as long as we care to watch. Nothing about the population as a whole is written down anywhere. Whether the thousand end up agreed or split, calm or frightened, is an outcome of the model and never an assumption in it, and the only way to learn which it will be is to run the thing and look.

The instrument fits this question for a specific reason. A moral panic is a claim about a population, but the mechanisms it is supposed to run on, persuasion, fear, taking offence at one's neighbours, are all claims about individuals. Writing the individual claims down and inspecting the population that comes out is a way of asking whether the one really does produce the other. And because this population is ours, we can do what no student of a real episode can. We can run the same thousand people twice, identical in every respect except that in the second world nobody campaigns at them, and read off the difference. That difference is the quantity the field has never been in a position to observe.

Three words recur throughout and are worth fixing here. A _run_ is one execution of the model from start to finish. A _step_ is one round inside a run, in which every agent looks at whoever it can hear and updates; a step measures communicative exposure and stands for no particular stretch of clock time, so the model speaks of earlier and later and never of days or weeks. A _seed_ is the number that fixes every random draw a run will make. Two runs given the same seed begin from exactly the same thousand people, wired to each other in exactly the same way, so re-running one of them is a repetition and not an approximation.

The model itself has six parameters and four rules. A rule says how one quantity changes from one step to the next; a parameter is a dial that sets how strongly a rule acts, and it holds still for the whole of a run. Four parameters are global and two, depth and reach, are set separately for each claims-maker, so a run with both claims-makers active fixes eight numbers.#footnote[The description follows the ODD protocol (Overview, Design concepts, Details), the standard reporting checklist for agent-based models @grimmStandardProtocolDescribing2006 @grimmODDProtocolDescribing2020, in substance if not in its section order.] What the model leaves out is stated in Section 4.3.

== Entities, states, and structure

The model contains $N$ agents, a fixed undirected graph recording who can hear whom, and two external claims-makers. Each agent carries two states that change from step to step. The first is a _moral position_, written $b_i (t)$ ($b$ for belief, with the subscript naming the person and $t$ the step), which runs from $-1$, full alignment with the stigmatised position, to $+1$, full alignment with the dominant moral claim; the middle of the range stands for indifference or ambivalence. The second is _alarm_, written $a_i (t)$ and running from $0$ to $1$: how much danger this person feels is in the air. Alarm is deliberately undirected. It records how alarmed someone is and says nothing about what they fear; the object of the fear is read off jointly with their position, so that an alarmed agent near $+1$ fears the stigmatised group while one near $-1$ fears persecution. Each agent also carries a fixed _panic threshold_ $theta_i$ ($theta$ for threshold), the level of alarm past which they begin to amplify: once across it, a person is heard more loudly by everyone around them, in the way an agitated participant in a rumour is. Dispersion in those thresholds (people differ in how much alarm it takes to set them off) is the only difference between agents that the model keeps, because it fixes what share of the population is amplifying at a given level of alarm, and that share is the gain of the reinforcement loop described below @granovetterThresholdModelsCollective1978. Every symbol used in this section is collected, with its plain reading, in @tab:notation.

The network is the model's entire account of who can hear whom. It is a list of pairs: where two agents are joined, each hears whatever the other says at every step, and where they are not, neither reaches the other except through the people in between. How many contacts an agent has is its _degree_, and the average across everyone is the _mean degree_. Nobody makes or breaks a tie during a run, so the social world an agent inhabits at the last step is the one it was handed at the first.

Which network the thousand are wired into is the primary explanatory variable of the first experiment, and three generators supply it. Each produces a population with the same mean degree but a different social shape. The Watts--Strogatz small world is the acquaintance network of ordinary life: your contacts largely know one another, while a few long ties put anyone within a short chain of anyone else @wattsCollectiveDynamicsSmallworld1998. The Holme--Kim graph, or preferential attachment with clustering @holmeGrowingScalefreeNetworks2002, adds a handful of people who know an enormous number of others, the local notables and broadcasters, while keeping those closed triangles of mutual acquaintance that plain preferential attachment lacks @barabasiEmergenceScalingRandom1999. The Erdős--Rényi random graph @gilbertRandomGraphs1959 pairs people off at random, so it has neither notables nor triangles; it resembles no real society, and it earns its place as the comparison case in which structure does nothing. Following #cite(<broidoScalefreeNetworksAre2019>, form: "prose"), the second is called hub-dominated, not scale-free. Runs keep the whole graph, including any agent the generator happens to leave with no contacts at all, since that isolation is substantively meaningful: someone who can be reached by a campaign and by nobody else occupies a position that really exists in social life.

The model contains two kinds of entity, and the paper keeps them apart by name from here on. _Agents_ are the $N$ people in the network. Each carries the two states just described, responds through fixed rules, and chooses nothing. _Claims-makers_ are the two campaigners who act on the network from outside it. They carry no states, hold no position in the graph, cannot themselves become alarmed, and are the only source of strategy anywhere in the model. Nothing is both, and no third term is used for either: where the paper says agent it means one of the thousand, and where it says claims-maker it means $D$ or $C$.

The _moral entrepreneur_ $D$ promotes the dominant moral claim and pulls the agents it reaches toward its own pole, $p_D = +1$; the _counter-entrepreneur_ $C$ pulls toward the opposite pole, $p_C = -1$, standing in for the niche media through which folk devils answer back @mcrobbieRethinkingMoralPanic1995. A pole is simply the position a claims-maker argues for, and it never changes during a run. Because claims-makers stand outside the network, the two sources of alarm remain separable; one placed inside it would both cause alarm and absorb it. The symmetric design follows #cite(<mikhaylovaFolkDevilsMoral2022>, form: "prose"), for whom entrepreneur and folk devil name positions taken up within a contest and not fixed statuses of those who occupy them. The folk devil accordingly has no claims-maker of its own. It enters as the stigmatised pole around which alarm and clustering emerge, which preserves the constructivist insight that folk devils are constituted through attribution.

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

#h4[Targeting] Each active claims-maker $X$ reaches $n_X = min(N, ceil(rho_X N))$ agents per step, its reach $rho_X$ being read as a share of the population, so that $rho_X = 0.25$ means a quarter of it; we write $g^X_i (t) = 1$ for a person it reaches at that step and $0$ for everyone else.

_Which_ agents it reaches is decided by its _targeting repertoire_: the campaigning strategy by which a claims-maker picks its audience at each step. Beyond how widely it reaches and how hard it pushes, this is the only choice the model gives a claims-maker, and it is the strategic variable of the first experiment. Four repertoires are available, and they are set in typewriter type throughout the paper, which marks them as settings a claims-maker is run with and not as terms of the argument. `random` draws a fresh uniform subset every step, so that its audience turns over completely, and at $rho_X = 1$ it becomes mass broadcast to the whole population. `hub` takes the $n_X$ best-connected agents, which is the strategy of recruiting influential people. `base` takes the $n_X$ agents already closest to the claims-maker's own pole, which is the strategy of rallying the committed. `fixed_random` draws a uniform subset once and then addresses that same subset at every step.

The fourth is a measuring instrument rather than a strategy any campaigner would adopt. `hub` and `base` each depart from `random` along two dimensions at once, in _whom_ they select and in returning to the same people every step, so separating the two requires a control that departs along one dimension only: `random` against `fixed_random` isolates the exposure schedule, and `fixed_random` against `hub` isolates degree.

#h4[Peer influence] An agent is moved only by neighbours close enough to still be worth listening to. Someone whose view sits a little away from yours can shift you a little; someone whose view strikes you as beyond the pale does not shift you at all, and might as well not have spoken. The model draws that line at a fixed width, the tolerance $epsilon$, the same for everyone. Four pieces of notation carry the rule. _Moral distance_ $Delta_(i j)(t) = |b_i (t) - b_j (t)|$ is how far apart two people's positions are, so a distance of $0$ is agreement and of $2$ is the full width of the issue. $cal(N)_i$ is the set of $i$'s contacts and $d_i$ is how many of them there are. Finally, $kappa_j (t)$ is how loudly $j$ is heard: $gamma$ (three times the normal volume at the operating point) once $j$'s alarm is past its threshold, and $1$ otherwise. The net pull that $i$'s contacts exert on its position is then

$ S_i (t) = cases(
  (sum_(j in cal(N)_i) kappa_j (t) bb(1) [Delta_(i j)(t) <= epsilon] (b_j (t) - b_i (t))) / (sum_(j in cal(N)_i) kappa_j (t)) & "if" d_i > 0,
  0 & "if" d_i = 0.
) $ <eq:peer>

Read in words: average the disagreement of everyone whose position is within tolerance $epsilon$, weighting each of them by how loudly they are heard, and move that far. The bracketed indicator is a switch that counts a contact only while the gap to them stays inside tolerance; beyond it, the contact is tuned out and contributes nothing. This is bounded confidence without repulsion, following Hegselmann and Krause (2002) and #cite(<deffuantMixingBeliefsInteracting2000>, form: "prose"); #cite(<flacheModelsSocialInfluence2017>, form: "prose") survey the wider family. Agents disengage from the morally distant but are never driven away by them, which keeps divergence attributable to a single mechanism. Note that the denominator counts every contact, tuned out or not: being surrounded by people one has stopped listening to leaves less to move toward, and so shortens the distance anyone travels in a step.

#h4[Position update] Agents a claims-maker reaches are pulled toward its pole with a strength set by its _depth_ $alpha_X$ (how hard it pushes those it reaches) and by how far the person still has to travel: $I^D_i (t) = alpha_D g^D_i (t)(1 - b_i (t))$ for the entrepreneur and $I^C_i (t) = alpha_C g^C_i (t)(1 + b_i (t))$ for its opponent. The second factor shrinks as an agent approaches the pole, so a claims-maker acting alone moves each person a fixed _fraction_ of the remaining way. Two familiar features of campaigning follow from that one piece of arithmetic. Preaching to the converted yields almost nothing, since those who already stand where the campaign stands have hardly any distance left to be moved through. And no campaign can make anyone more committed than the claim it is itself making: a claims-maker who says the danger is grave cannot manufacture a public that thinks it graver still. Positions then update as

$ b_i (t+1) = "clip"_([-1,1])[ underbrace(sigma b_i (0), "anchor") + (1 - sigma)(underbrace(b_i (t), "persistence") + underbrace(S_i (t), "peers") + underbrace(I^D_i (t) - I^C_i (t), "claims-makers")) + underbrace(xi_i (t), "noise") ], $ <eq:position>

In words: an agent's position at the next step is where it already stood, moved by whatever its neighbours pulled it toward, moved again by whichever claims-maker reached it, and nudged by a small random amount. The braces under the equation name the four contributions in that order. Here $xi_i (t)$ is the nudge, a random jitter of size $zeta$ standing for the idiosyncratic reasons people shift a little without any social prompting, and the outer clip simply keeps positions inside the scale. The anchor $sigma$ deserves a paragraph of its own, because setting it to zero is the strongest assumption in the model. It is the Friedkin--Johnsen weight @friedkinSocialInfluenceOpinions1990, and substantively it asks whether people have convictions of their own that quietly reassert themselves once the pressure lets up: the colleague who is talked round at the meeting and has drifted back to their old view by the following week. Give agents any such conviction and they are pulled back toward where they stood before the campaign, which under a consensual start means back toward indifference. The pull works on a timetable of its own, $-1 slash ln(1 - sigma)$ steps, and it dissolves the manufactured division this paper exists to measure whatever value $omega$ takes. So the choice is between a population whose members are anchored, in which every episode ends on the anchor's schedule and nothing else is worth measuring, and a population with no such ballast, in which whatever the campaign builds it keeps. We take the second. It grants a campaign the most durable division it could possibly achieve, so the persistence results in Section 3.2 say how long a manufactured division can last and never how long it does. Section 4.3 pays for the choice explicitly. The only other work the anchor would do is to prevent the trivial consensus of plain neighbour averaging @degrootReachingConsensus1974, and bounded confidence already does that. Depth appears here and nowhere else: it scales persuasion and leaves alarm untouched, so a claims-maker is silenced by $rho_X = 0$ and never by $alpha_X = 0$.

#h4[Alarm update] Agents catch alarm; they never reason their way into it. A claims-maker enters the neighbourhood of each agent it reaches as though it were one more contact, maximally alarmed and permanently loud, which is what receiving an alarming message amounts to. Writing $m_i (t)$ for how many claims-makers reach $i$ this step (zero, one or both), the two things an agent is exposed to are _alarm exposure_ $E_i$, how alarmed its social world looks, and _othering exposure_ $Phi_i$, how much moral disagreement it is surrounded by:

$ E_i (t) = min(1, (sum_(j in cal(N)_i) kappa_j (t) a_j (t) + gamma m_i (t)) / (d_i + m_i (t))), quad
  Phi_i (t) = (sum_(j in cal(N)_i) kappa_j (t) Delta_(i j)(t) slash 2) / (sum_(j in cal(N)_i) kappa_j (t)), $ <eq:exposure>

The first expression asks how frightened the people around this agent appear to be, counting any campaigning message as one more frightened voice in the room. The second asks how far away those same people stand from the agent morally. Neither has anything to do with what the agent itself believes, and both are zero for someone with no contacts whom no claims-maker reaches. Alarm then updates as a weighted sum of three things: what the agent already felt, what its world feels, and how much it disagrees with the people around it.

$ a_i (t+1) = "clip"_([0,1])[ underbrace(mu a_i (t), "memory") + underbrace(delta E_i (t), "contagion") + underbrace(omega Phi_i (t), "othering") ]. $ <eq:alarm>

Memory is yesterday's fright carried into today; contagion is fright picked up from other people; othering is fright generated by the bare fact of disagreement. What is absent from the list is as telling as what is in it. Nobody in the model ever weighs evidence about whether the danger is real, because the model contains no danger to weigh evidence about. Alarm here is entirely a social product, and that is a decision about what to build, defended in Section 4.3 and paid for there.

Alarm exposure carries two features the results depend on. Both claims-makers raise alarm, because alarm is undirected: a message that a threat exists is alarming whoever sends it, so the defence of a stigmatised group frightens people exactly as the campaign against it does. And the denominator counts contacts, without summing their volume. Had we divided by total volume, exposure would be an average, and an average can never exceed its largest ingredient: no one could end up more alarmed than the most alarmed person they know. Dividing by the count instead lets alarmed contacts _accumulate_, so that someone with many agitated acquaintances ends up more alarmed than any one of them. That is the reinforcement described by complex contagion @granovetterThresholdModelsCollective1978 @centolaComplexContagionsWeakness2007, and it is why the expression is capped at $1$. Othering exposure, by contrast, excludes claims-makers altogether: it is the experience of being surrounded by morally distant peers, and not of receiving a message.

Since the whole paper turns on it, the role of _othering_ is worth stating plainly. It is the third term of @eq:alarm, $omega Phi_i (t)$: the rate at which an agent turns the moral distance between itself and the people it can hear into alarm about them. The weight $omega$ says how far mere disagreement is experienced as danger, and it is the single parameter the population's own contribution to a panic runs through. Three properties follow, and nothing else in the model has them. Othering is internal to the population and requires no campaign, so it is the second of the two manufactured sources of alarm that Section 2.3 separates, and the only one that keeps working when both claims-makers fall silent. It makes division self-reinforcing, because agents whom a campaign has driven apart then frighten one another simply by being apart, which no amount of broadcasting could do on its own. And it is the entire capacity of the model to outlast a campaign: at $omega = 0$ disagreement is merely disagreement, the population registers no threat in it, and an episode can only end when the claims-making does. The word is borrowed from a broader literature on the construction of out-groups @ameryOtheringPeakingPopulism2025; here it names this arithmetic on moral distance and nothing more, carrying no implication about the content of what is said, its tone, or anyone's intent.

Together, @eq:peer and @eq:exposure produce the model's central asymmetry. A neighbour beyond an agent's tolerance contributes nothing to its position and the most to its alarm: such neighbours cannot change its mind, and they frighten it more than anyone else can. A population sorted into opposed camps therefore manufactures its own alarm, and all three hypotheses rest on that.

== Measuring panic

Everything that follows rests on an experiment nobody can perform on a real society and that costs nothing to perform on this one. Run a population's history; then wind it back and run the same history again with one thing taken away. Because this population is a set of numbers, the winding back is exact: the same thousand people, the same acquaintances, the same opinions to start from, the same susceptibilities to alarm. Anything that differs at the end differs because of the one thing taken away, and there is nothing else it could be.

Alarm has two manufactured sources and each can be switched off independently: claims-making by silencing both claims-makers, othering by setting its coefficient $omega$ to zero, which stops disagreement being frightening in itself. Every setting is therefore executed four times, in a $2 times 2$ design: with neither source, with claims-making only, with othering only, and with both. Write $overline(a)$ for the population's average alarm and mark each version with a superscript, $overline(a)^"null"$ for the world with neither source, $overline(a)^"cm"$ for claims-making only, $overline(a)^"oth"$ for othering only, and plain $overline(a)$ for the full run. The four are strictly comparable, because a single random seed fixes the network, the initial positions, the initial alarm and the thresholds. They are the same thousand people living through four different worlds. Their averages then split the total exactly, at every step:

$ overline(a) = underbrace(overline(a)^"null", "warranted")
  + underbrace(overline(a)^"cm" - overline(a)^"null", "claims-making alone")
  + underbrace(overline(a)^"oth" - overline(a)^"null", "othering alone") \
  + underbrace(overline(a) - overline(a)^"cm" - overline(a)^"oth" + overline(a)^"null", "interaction"). $ <eq:decomp>

The first term is the alarm the situation warranted anyway; the next two are what each source produces on its own; the fourth, the _interaction_, is the term the design exists to isolate.

An interaction is what is left over when two causes together do more than the two of them do apart. Water a field and it grows a little; feed it and it grows a little; do both and it may grow far more than the two increments added together, and that excess belongs to neither input on its own. Here the two inputs are a campaign and a population for whom disagreement is frightening, and the excess is the alarm that exists only because a campaign divided a population which was then frightened by its own division. Neither input could have produced it alone: a campaign in a population indifferent to disagreement has nothing to work with, and a population sensitive to disagreement has nothing to be frightened of until something divides it. In a world where the two sources simply added up, this term would sit at zero, and every point below turns on the fact that it does not. One further property of the design matters for how the term should be read. Since all four worlds start identical, the interaction is exactly zero at the first step and can become non-zero only at the second, and then by a single route: the campaign has moved positions, which changes the moral distances that othering reads. Whatever the interaction later measures was therefore manufactured inside the run, and none of it is inherited from how divided the population happened to be at the start.

Disproportion is the total excess over what the situation warrants, normalised by the room available for it:

$ Pi(t) = (overline(a)(t) - overline(a)^"null" (t)) / (1 - overline(a)^"null" (t)) in [0, 1]. $ <eq:pi>

Read the fraction as a proportion of what was available. The top is how much extra alarm the campaigning produced; the bottom is how much extra alarm there was room for, given how alarmed this population already was with nobody campaigning at it. We call the result the _panic index_ $Pi$ ($Pi$ for panic). At zero the population is exactly as alarmed as it would have been had no one campaigned, and at one mean alarm has reached the top of its scale. The index is thus a statement about a comparison and never about a population on its own: no single society, looked at by itself, has a panic index at all. A _moral panic episode_ is then a stretch of at least $W$ consecutive steps in which the index stays above a cut $Pi^*$ and the share of the population past its own alarm threshold, written $q$, stays above a second cut $q^*$. Requiring both distinguishes panic from two things it is often confused with: concern that is widespread but proportionate, where many are alarmed and little of it is excess, and the successful manipulation of a small minority, which is the reverse. In the terms of #cite(<goodeMoralPanicsCulture1994>, form: "prose"), the pair makes disproportionality operational and approximates consensus. The placement of the three cuts is conventional, so incidence is reported across a grid of all three, and we show below that the conclusions do not depend on the choice. Alongside $Pi$ we record persistence after withdrawal, mean position, mean othering exposure, and two summaries of shape. Sarle's bimodality coefficient @pfisterGoodThingsPeak2013 asks whether the population's positions form one hump or two, which is how a split into opposed camps registers as a single number. The exposure concentration $"Var"_i (sum_t g^D_i (t))$ is the variance, across people, of the number of times each was addressed over the whole run: it sits near zero when a campaign spreads its attention evenly and grows large when the campaign keeps returning to the same few, which is what tells the four repertoires apart.

The instrument stays meaningful only under two conditions. The first is bookkeeping: the three weights on alarm must not sum past one, or alarm would run off the top of its scale, and we impose this on every parameter setting we sample. The second is substantive. Contagion must stay _sub-critical_, meaning that a spark of alarm dropped into an otherwise calm population dies out instead of feeding on itself; an epidemiologist would write the condition as a reproduction number below one. Above that boundary alarm sustains itself from any spark at all, whatever anyone campaigns about. Such a public is a real and interesting thing, a public so primed that any incident whatever would have served and the particular folk devil is close to incidental. It is not, however, a public whose alarm can be attributed to anybody's claims-making, and disproportion measured against a counterfactual has nothing to grip. The condition keeps that society outside the study, without denying it exists. The boundary is not a single number, because an alarmed contact is heard several times as loudly as a calm one and therefore counts for more than its share. We measure it at every point we report: silence both claims-makers, switch off othering, set a few per cent of the population at full alarm, and check that the alarm dies out.

== Experimental design and verification

A model with eight numbers in it has more settings than anyone can report, so the paper fixes one and moves away from it in one direction at a time. That fixed setting is the _operating point_, the concrete case returned to whenever a single number is wanted. Moving one dial through a range with everything else held still is a _sweep_; moving two at once through every combination is a _grid_, which is worth the extra runs only where the effect of one dial depends on where the other is set.

The operating point throughout is a Watts--Strogatz small world with $N = 1000$ and mean degree $10$; $epsilon = 0.5$, $mu = 0.30$, $delta = 0.25$, $omega = 0.35$; $sigma = 0$, $gamma = 3$, $zeta = 0.01$; the entrepreneur on `base` with $alpha_D = 0.7$ and $rho_D = 0.25$, withdrawing at $t_"off" = 150$; horizon $T = 400$. Three experiments follow the three phases of an episode, and each asks one question.

#h4[Experiment A: what it takes to start a panic] A single entrepreneur campaigns and nobody answers back ($C$ silent throughout). We vary three things about the campaign and the society it runs in: the strategy by which the entrepreneur picks its audience (the four targeting repertoires of Section 2.2), the shape of the society it campaigns in (the three network generators), and whether that society begins agreed or already split (the two initial position regimes). Inside each combination we then widen the campaign in fine increments, raising the share of the population it addresses each step from almost nobody to everybody ($rho_D$ from near $0$ to $1$), and cross that against how hard it pushes the people it reaches, on a full grid ($alpha_D times rho_D$). The two are crossed rather than varied separately because they interact: how hard a campaign pushes turns out to decide whether reaching more people helps at all.

#h4[Experiment B: what keeps a panic going once the campaigning stops] We take the settings from A that reliably ignite, switch the entrepreneur off in mid-run ($rho_D arrow 0$ at $t_"off" = 150$) while letting the population carry on to the horizon, and follow each of the four sources of alarm across that moment (the terms of @eq:decomp). The question is how much of the alarm disappears with the campaign and how much does not. We then vary how the population itself processes alarm, sweeping the weights on memory, contagion and othering ($mu$, $delta$, $omega$), to establish which of the three mechanisms the surviving alarm actually depends on.

#h4[Experiment C: what answering back achieves] This is the only experiment in which both claims-makers appear. The entrepreneur withdraws at $t_"off"$ and the counter-entrepreneur enters at the same step, so that the defence begins from the population the campaign left behind. It enters in three configurations: broad and shallow (reaching many people and pushing each of them gently, $alpha_C = 0.15$, $rho_C = 0.60$), narrow and deep (reaching few and pushing them hard, $0.90$, $0.10$), and one matched to the entrepreneur's own settings ($0.70$, $0.25$). The three span the trade-off between reaching many people and moving them far without mapping that trade-off exhaustively, and a separate sweep moves each lever on its own.

One run of a model like this establishes nothing on its own. It contains one particular set of random draws, and a striking result may be nothing more than the luck of that draw. Every setting is therefore run 250 times over, each time from a fresh seed and so on a freshly built thousand people, and what we report is the spread across those 250 runs. A finding is a claim about the spread; where a number appears below without qualification it is a mean over seeds, and panic incidence is the share of the 250 in which an episode occurred. At 250 seeds per setting the Monte Carlo standard error on incidence is at most $plus.minus 0.032$, which is how far a reported frequency could move if the same setting were re-run on a fresh batch of seeds. Since each seed produces all four counterfactual runs, the headline program is 72,990 counterfactual sets, or 291,960 simulation runs.

The second hypothesis asks which of three ways of keeping alarm alive actually keeps it alive, and the three are not merely three parameters. Each stands for a different account of what a moral panic is once the campaigning stops. Memory says an episode is a residue in individual minds that fades at its own rate. Contagion says it is fear passing from person to person, and would put panics in the same family as rumours and runs on banks. Othering says it is people frightened of one another across a division, and would make an episode a property of the relations between them rather than of anyone's state of mind. These are rival explanations of the same outcome, so testing one at a time will not settle between them; the analysis has to apportion a single outcome among competing inputs. A variance-based sensitivity analysis does exactly that. It asks what share of the variation in an outcome, across the whole space of settings, each input is responsible for, counting the effects it has jointly with the others @sobolGlobalSensitivityIndices2001. Such a share is called a Sobol index. The one we use throughout, written $S_T$, is the _total-order_ index, which credits an input both with what it does on its own and with what it does only in combination with the rest, so that a mechanism working entirely through another is still visible. An input whose index is near one drives the outcome; one whose index is near zero contributes nothing of its own.

Our version of it departs from the standard design in two places. First, the three alarm weights cannot be drawn independently, because they must not sum past one; drawing them freely and discarding the illegal combinations would leave the survivors correlated and the apportionment invalid. We therefore split each setting into two questions that _can_ be asked independently: the _total intensity_ $s$, how strong alarm dynamics are overall, and the _split_ between memory, contagion and othering, that is, what shares of that total each of the three receives. The split is a three-way mix whose parts add to one, a budget allocated across three headings, and the geometric name for the set of such mixes is a simplex. For three parts it is a triangle: each corner is one mechanism doing all the work, and every interior point is a blend, which is how @fig:h2 plots it. Asking about the split at fixed intensity poses the substantive question directly: granted that a population is inflammable, what keeps it inflamed? Second, the noise constant $zeta$ enters as a fourth input, run over two ranges, because how far positions drift for idiosyncratic reasons competes with othering to explain what survives. Estimation uses a standard sampling design and estimator @saltelliVarianceBasedSensitivity2010 @jansenAnalysisVarianceDesigns1999, written from scratch and checked against a test function whose answers are known analytically @ishigamiImportanceQuantificationTechnique1991, which it reproduces to within $0.0025$.

A simulation can fail in a way an argument cannot. The reasoning may be sound, the specification may say exactly what its author meant, and the code may still not do what the specification says, in which case every number in Section 3 describes a program rather than a model. That the code implements the specification is therefore established separately, and before any substantive result is looked at. The technique is to strip the model down until it becomes some simpler model whose behaviour is already known from the literature, and to check that our code reproduces that known behaviour: switch off tolerance and the two claims-makers and it must reduce to plain neighbour averaging, which converges to consensus; restore the anchor and it must land on the equilibrium Friedkin and Johnsen derived; keep tolerance and it must leave the number of surviving opinion clusters that the Hegselmann--Krause model leaves; hold everything homogeneous and mean alarm must settle where the analytic fixed point predicts; and on a graph with no ties at all the campaign world and the campaign-free world must coincide exactly, so that the panic index is zero by construction. All fourteen verification and property checks pass. The implementation is Python with `networkx` @hagbergExploringNetworkStructure2008 and `numpy` @harrisArrayProgrammingNumPy2020, and all randomness derives from one recorded seed through three substreams, for setup, targeting and noise: sharing a stream between targeting and noise would desynchronise the four arms, and the counterfactual would no longer hold the same population fixed.

// ─────────────────────────────────────────────────────────────────────────────
= Results
// ─────────────────────────────────────────────────────────────────────────────

Three conventions govern every number below, and it is worth fixing them before the numbers start arriving. The panic index $Pi$ is the share of the available alarm that the campaigning put there, so $Pi = 0.29$ says that just under a third of the room above the campaign-free baseline has been filled, and $Pi = 0$ says a campaign achieved nothing its population would not have felt anyway. The four terms of @eq:decomp are the parts $Pi$ divides into, and because they always add to the whole, a claim that one of them is large is at the same time a claim that the other three are small. Every figure quoted is a mean across 250 separately generated populations unless we say otherwise, and where the spread across those 250 bears on the argument we give it.

Each of the three subsections below opens with a hypothesis exactly as we wrote it down before any of these runs existed, set in smaller type. Printing the prediction beside the outcome is deliberate. A simulation will obligingly produce numbers for any hypothesis whatever, and the only real guard against reading those numbers to suit is to have said in advance what they ought to say. Several of the clauses turned out to be wrong, including both outcomes we specified in advance for the third hypothesis, and they are reproduced here unrevised.

Three things have to be true of every run before its numbers mean anything, and all three hold throughout. Alarm has to be unable to sustain itself, or an episode would prove nothing about the campaign that preceded it; a spark of alarm dropped into the calm population dies away to nothing, so no episode below is alarm feeding on itself. The campaign-free world has to stay calm, or the index would be dividing by almost nothing and any small absolute change would look enormous; its highest mean alarm across all runs is $0.052$, which leaves the denominator of @eq:pi close to one. And the population has to start genuinely agreed, or a campaign would get credit for division it inherited. At the first step the average moral gap between people who can hear each other is $0.067$ on a scale where $1$ is the width of the whole issue, against $0.386$ in the already-divided contrast. Whatever division the runs later show, the campaign made it. The three generators are matched on mean degree ($10.00$, $9.94$, $9.88$) and differ where they are meant to. Clustering, the chance that two of a person's contacts also know each other, is $0.487$, $0.212$ and $0.010$; degree dispersion, how unequally contacts are shared out across people, is $1.00$, $12.81$ and $3.22$, for Watts--Strogatz, Holme--Kim and Erdős--Rényi respectively.

== Ignition

#registered[
  H1, as registered. Which repertoire ignites a panic depends on network topology, and ignition is amplifying but not discontinuous: $Pi > rho_D$ across the usable range, while the response stays smooth and saturating rather than jumping at a critical value. `hub` ignites fastest in hub-dominated networks and degenerates to `random` where degrees are even.
]

A moral panic is a reaction out of proportion to its cause, and the model's counterpart of that is _amplification_: a population giving back more than was put into it. Panel (a) of @fig:h1 sets up the comparison directly. Along the bottom is how much of the population the entrepreneur addresses at each step; up the side is how much excess alarm results; and the diagonal marks where the two are equal, one unit of panic for one unit of campaigning. A curve running above that diagonal is a society returning more than it received. Amplification does appear, though not for claims-making in general. `hub` clears the diagonal from the smallest reach tested, `base` and `fixed_random` clear it out to $rho_D approx 0.4$, and `random` never clears it at any reach at all. `random` instead holds a flat ratio of response to campaign, $Pi slash rho_D approx 0.18$: whatever share of the population it addresses, it gets back about a fifth of that in excess alarm, and the fifth never grows. A society that returns a fixed fraction of what is put into it is not amplifying anything; it is passing the campaign through.

Which curves lie on top of one another tells us where the amplification comes from. `fixed_random` traces `base` almost exactly across the whole sweep, and those two repertoires have nothing whatever in common except that each addresses a settled audience. One picks the people who already agree with the campaign; the other picks its audience by coin-flip at the start and never revisits the choice. Since the second knows nothing about who anybody is, whatever the two share cannot be a property of the people chosen. What amplifies is reaching _the same_ people repeatedly; whether they are also the right people is a separate question, taken up in the next paragraph. In substantive terms, a campaign turns into a panic by working on a fixed constituency, and how many people it persuades matters far less. Repetition on the same audience opens a gap between that audience and everyone else, and the gap does the alarming.

#figure(
  image("fig1_h1_ignition.pdf", width: 100%),
  caption: [Ignition. (a) how much panic each of the four repertoires produces as its reach grows, on the small world, with the diagonal $Pi = rho_D$ drawn in: a curve above that line is a reaction larger than the campaign that caused it. (b) the same for `hub` alone across the three network types, with `random` repeated as a light reference, which isolates what topology does. (c) manufactured division (the interaction term) against reach, circles marking each peak, showing that it rises, peaks and then disappears. (d) $Pi$ across every combination of depth $alpha_D$ and reach $rho_D$, darker being higher, with the heavy rule drawn where a reached agent's one-step move $alpha_D (1 - overline(b))$ crosses the tolerance $epsilon = 0.5$: below that rule the campaign persuades, above it the campaign divides. All four panels read $Pi$ at $t = 199$. Mean over 250 seeds; bands are $plus.minus 1$ standard deviation across seeds.],
) <fig:h1>

We had registered that `hub` would collapse into `random` wherever people have roughly equal numbers of contacts, on the reasoning that with no one especially well connected there is nobody worth singling out. That clause is refuted, and the control shows why. On Watts--Strogatz, where contact counts barely vary between people (a standard deviation of $1.00$), `hub` still produces up to $14.8$ times the panic that `random` does.

That advantage divides in two, because `hub` differs from `random` in two ways at once, and each step of the comparison isolates one of them. Going from `random` to `fixed_random` changes only the schedule of exposure, from a fresh audience each step to a settled one, and it multiplies $Pi$ by up to $7.0$; at $rho_D >= 0.30$ this accounts for the whole of `hub`'s advantage, and the control actually outperforms `hub`. Going from `fixed_random` to `hub` changes only who is in the audience, and it is worth a further $2.2$ to $2.5$ times at $rho_D <= 0.10$ and nothing at all above $0.25$. Consistency is thus the larger effect and connectedness the smaller one, and connectedness stops mattering as soon as a campaign can afford an audience of any size.

The exposure concentration of Section 2.3 closes the argument, and it is worth reading the three numbers slowly. It measures how unevenly a campaign spread its attention across the run: address everybody about equally and it sits near zero; return to the same few and it rises. At $rho_D = 0.10$ it is $18$ for `random`, which by construction shares its attention out almost evenly, and $3600$ for `fixed_random`, the largest value the arithmetic permits, since that repertoire spends the entire run on one tenth of the population and never once addresses the other nine tenths. `hub` reaches only $2272$, because where many agents have identical contact counts the choice between them is arbitrary and its audience quietly turns over. So `hub` concentrates its attention _less_ than the control and still beats it at low reach, which can only mean it is drawing on something the control has no access to. The practical reading is that recruiting the well connected buys a campaign something real only while it cannot afford an audience of its own; past that point what pays is returning to the same people, and who those people are stops mattering.

Topology moves `hub` and almost nothing else, which is what panel (b) of @fig:h1 isolates: its peak runs $0.475$, $0.433$ and $0.386$ on Holme--Kim, Erdős--Rényi and Watts--Strogatz, while the other three repertoires vary by less than $0.02$. The registered topology clause holds, but for that one repertoire alone.

Once stated, the restriction is intelligible. `hub` is the only repertoire that consults the network before choosing whom to address, so it is the only one whose fortunes can turn on how that network is arranged. The others pick their audience by conviction or by lot and are indifferent to the shape of the society they arrive in. A campaign built on recruiting the well connected is thus placing a bet on the structure of the public it faces, and will do better in some societies than in others; a campaign built on rallying its own base places no such bet and travels between societies unchanged. Where the moral panic literature treats network structure as a background condition on episodes in general, the model puts it on one strategy in particular.

The sharpest structure lies in the axis the hypothesis treated as secondary: not how widely a campaign reaches, but how hard it pushes the people it does reach. Panel (d) of @fig:h1 crosses the two, and it reads row by row. The quantity that matters is how far a single exposure moves someone, $alpha_D (1 - overline(b))$, which is the depth of the push scaled by how much of the scale the person has left to travel. Compare that distance with the tolerance $epsilon$, the width of disagreement people will still listen across, and the grid falls into two halves.

Below the line the whole row stays pale, running from $Pi = 0.02$ at the narrowest reach to $0.13$ at $rho_D = 0.7$, because there a campaign _converts_ instead of dividing. It moves the people it reaches by less than their neighbours will tolerate, so those neighbours keep listening and are towed along; the population arrives at the entrepreneur's pole together, mean position $overline(b) arrow 0.99$, and the interaction term never leaves zero. Everyone agrees, and agreement frightens nobody. Above the line the rows are nearly identical to one another, the three depths $0.7$, $0.8$ and $0.9$ differing by less than $0.02$, while moving along any one of them changes $Pi$ six-fold and carries it as high as $0.44$. Below the line no reach ignites anything; above it, reach alone decides how large the episode becomes. Depth is a gate and reach is the dial.

Substantively, that gate is the point at which a campaign stops persuading and starts estranging. A moderate claim carries its audience along with their neighbours; a claim strong enough to be disowned takes the audience out of earshot of everyone else, and only then does it matter how many people were addressed. A fine sweep puts the gate between $alpha_D = 0.62$ and $0.68$, where the spread of $Pi$ across seeds swells from $0.014$ to $0.064$: at those settings the same campaign splits some populations and converts others, depending on nothing more than which thousand people it was given. That is the model's only knife-edge behaviour, and it sits in depth, not in reach.

Manufactured division peaks at intermediate reach and vanishes at full reach, which is the arch traced by panel (c) of @fig:h1. The interaction term peaks at $0.346$ (`fixed_random`) and $0.340$ (`base`) at $rho_D = 0.50$ and at $0.289$ (`hub`) at $rho_D = 0.20$, then collapses to $0.002$ for every repertoire at $rho_D = 1$, where all four repertoires become the same rule and exposure concentration falls to exactly zero because everyone is addressed at every step. No setting of the three episode cuts finds a single panic there: incidence is $0.00$ throughout the grid. The most powerful claims-maker imaginable, reaching everyone every step, is the one that cannot divide anybody. Universal address moves the whole population together, and a population that moves together has no internal distance left to be frightened by. Alarm is manufactured by unevenness in who receives the message, and the message itself does none of that work.

The experiment leaves two further observations, and the first is a warning about counting episodes at all. Between $rho_D = 0.15$ and $0.20$, the share of runs qualifying as an episode leaps from $0.08$ to $0.96$, which looks like a threshold being crossed. Underneath it, $Pi$ has merely drifted from $0.177$ to $0.234$, a distance of about four times the spread across seeds. What produces the leap is the counting rule: an episode is declared once $Pi$ clears a fixed cut, so a population inching past that cut in most of its runs rather than a few converts a gentle slope into an apparent jump. The tipping point belongs to the instrument, and the model underneath it has none.

Flattening the threshold distribution, so that everyone needs the same amount of alarm before they start amplifying, then lowers $Pi$ by 35 to 40 per cent at every reach while leaving the curve's shape and its peak untouched. Variation in how easily people are set off therefore scales the whole phenomenon up or down without changing where it happens. Of the nine registered clauses of H1, six held, two held only in part (amplification and the role of dispersion), and one, the degeneration of `hub`, was refuted.

== Handover

#registered[
  H2, as registered. The claims-making-alone term rises first and then plateaus, while the interaction term rises later and overtakes it. After the entrepreneur withdraws, $Pi$ remains elevated for a duration governed by othering rather than by passive decay: persistence is maximised near the $omega$ vertex of the alarm simplex, the split carries a larger total Sobol index than the intensity does, and $Pi$ decays to zero when $omega = 0$ but to a positive floor when $omega > 0$.
]

Once an episode is running, where does its alarm actually come from? This is the question the four-run design was built for, and it answers as four shares of one total. At the operating point the entrepreneur's own signal contributes $0.041$ to mean alarm, while the division it manufactures contributes $0.246$, close to six times as much; the ratio settles within twenty steps and holds for the rest of the campaign (@tab:h2, @fig:h2 panel (a)). Of all the alarm that would not have existed had nobody campaigned, 14 per cent is the campaign's own message, 2 per cent is disagreement the population brought with it, and 84 per cent is the interaction between the two.

The interaction could arise in either of two ways, and the design separates them cleanly. Othering may be feeding on disagreement that was there all along and has merely been made more audible, or on disagreement the campaign itself created. The othering-only world settles it, because nobody campaigns there, so any disagreement in it is original by construction. At the step before withdrawal, mean othering exposure stands at $0.189$ in the full run against $0.006$ in that world. Roughly three per cent of what the population is reacting to was already present; the entrepreneur made the other 97 per cent. Its durable product is the division, and not the alarm it broadcasts.

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
  caption: [The four terms of @eq:decomp across the entrepreneur's withdrawal, mean over 250 seeds. The four middle columns are contributions to mean alarm and add up to it exactly; $Pi$ is that total re-expressed as a share of the room available for it, and $q$ is the share of the population alarmed enough to be amplifying. The entrepreneur withdraws at $t_"off" = 150$, marked by the rule: the claims-alone column empties within five steps of that line while the interaction column barely moves.],
) <tab:h2>

The registered _ordering_, however, fails. The interaction overtakes claims-alone at $t = 2$ (the earliest step at which Section 2.3 permits it to be non-zero) in 250 of 250 seeds, and at every one of eight depths spanning the gate. There is no regime in which the panic belongs to the entrepreneur for a while and to the population later. Where a campaign pushes harder than its audience's neighbours will tolerate ($alpha_D > epsilon$), those neighbours stop listening the moment it first acts; the division is complete after one step, and othering has something to feed on by the second. The composition claim survives; the phase story does not. That matters for how the finding should be read. Ours is an accounting statement about where the alarm comes from, and it carries no chronology in which the entrepreneur holds the episode up alone before the public takes over.

The division outlives the entrepreneur that made it. Claims-alone falls to zero within five steps of withdrawal, and 250 steps later $Pi$ retains 62 per cent of its value at withdrawal; in 210 of the 250 seeds it was still elevated when the run ended, so those persistence figures are lower bounds on the true durations. The floor is made of othering and nothing else. Raising the othering weight while holding the other two fixed, so that the population's total capacity for alarm cannot change, moves what remains 250 steps after withdrawal from exactly zero to $0.286$; panel (b) of @fig:h2 puts the two moments side by side, $Pi$ at withdrawal and $Pi$ 250 steps later, against $omega$. Where disagreement is not itself experienced as danger, the episode ends with the campaign; where it is, the campaign is no longer needed.

#figure(
  image("fig2_h2_handover.pdf", width: 100%),
  caption: [Handover. (a) the four terms of @eq:decomp through the run, the dotted vertical marking the entrepreneur's withdrawal and the arrow the 5.94-to-one ratio of interaction to claims-alone; the gap between those two curves is the finding. (b) how much panic there is at withdrawal, and how much is still there 250 steps later, plotted against the othering weight $omega$ with $mu + delta$ held fixed, so that only the mix changes and not the population's total capacity for alarm. (c) what survives to the end of the run, $Pi(399)$, at each of 45 points on the triangle of alarm splits described in Section 2.4, the circle marking the maximum and the crosses the four points discarded for failing the sub-criticality probe. (d) total-order Sobol indices for the three reparameterised inputs, the share of the variation each is responsible for, with a pair of bars per input for the two outcomes: how much panic persists, and when the transfer happens. Almost everything sits on one input, the othering-versus-contagion balance.],
) <fig:h2>

That dependence sits in the _mix_ between the three alarm mechanisms and not in their total strength, and two independent instruments say so. The first scans the mix directly, and panel (c) of @fig:h2 is the result: holding total intensity fixed, we walk over 45 combinations of memory, contagion and othering, one point of the triangle each, and read off how much alarm survives at every one of them. Four of them have to be thrown out first, and the reason nearly reversed the result. Those four sit close to pure contagion, where alarm sustains itself regardless of any campaign, and they show the highest surviving alarm in the whole scan ($0.585$, against $0.097$ at pure othering). Plotting the scan without removing them would read as a refutation of the hypothesis; removing them without saying so would confirm it for the wrong reason. Among the 41 combinations that pass, the maximum sits exactly at pure othering.

The second instrument is the variance decomposition described in Section 2.4, drawn in panel (d) of @fig:h2 as one bar per input. It shares none of the first one's assumptions, gives the same answer, and locates it more sharply. Describing how a total divides three ways takes two numbers, and the analysis keeps them apart: one records how much of the total goes to memory, the other how whatever remains is split between contagion and othering. Only the second matters. It scores $S_T = 0.993$ for how much alarm survives and $1.004$ for when the transfer happens, meaning it accounts for essentially all of the variation in both. The memory number scores exactly zero on both, and the overall intensity of alarm three to four per cent. How long alarm lingers in an individual therefore makes no difference whatever to persistence; what decides it is whether the alarm circulating in the population is caught from others or generated by disagreement. An index slightly above one is estimation error and not a share exceeding the whole.

That result comes with one scope condition, and it is the sharpest limit in the study. With the drift of individual positions added as a fourth input, othering still explains essentially everything ($1.002$ against $0.022$) while drift stays below about twice its default; over a range five times the default the ordering _reverses_, to $0.389$ against $0.750$. The mechanism is intuitive once stated: if people's positions wander enough, someone who had drifted out of a neighbour's tolerance wanders back into it, the groups the campaign separated re-merge, and no permanent division is left for othering to feed on. Drift therefore governs what survives and leaves the timing of the transfer alone. The permanence of manufactured division depends on moral positions being fairly stable, and how stable they really are is not a question this model can answer. The anchor competes through the same channel. Give agents any pull back toward the convictions they began with and that pull, not othering, sets how long the episode lasts: at $sigma = 0.05, 0.10, 0.20$ the measured persistence is 13, 9 and 4 steps, tracking the anchor's own timescale of 19.5, 9.5 and 4.5 steps, and the floor vanishes altogether.

The registered clauses on tolerance and on the polarised regime need qualification. Low tolerance was predicted to bring the handover forward; the direction holds but there is no gradient, since $Pi(149)$ runs $0.320$ to $0.289$ across $epsilon <= 0.5$ and collapses to $0.045$ with no handover at all for $epsilon >= 0.7$. Tolerance and depth are one gate seen from two sides, $epsilon approx alpha_D (1 - overline(b))$. The polarised regime, predicted to hand over earlier with a smaller interaction, instead produces the largest $Pi(149)$ in the study ($0.566$) with the smallest interaction ($0.024$) and an othering-alone term of $0.500$: almost all of its alarm is division that existed before anyone acted. An already-divided population needs less entrepreneurship, but the cell is an attenuated test, and avoiding that attenuation is why the consensual default exists.

== Defence

#registered[
  H3, as registered, with both outcomes fixed in advance. A counter-entrepreneur acts through an immediate cost scaling with $rho_C$ and a delayed benefit scaling with $alpha_C$ that is not guaranteed in sign. _Branch 1:_ broad-and-shallow lowers $Pi$ while narrow-and-deep raises it, so defence works but only through reach. _Branch 2:_ no configuration lowers $Pi$, so counter-claims-making is structurally self-defeating in this model.
]

What does the stigmatised side achieve by answering back? We had committed in advance to two possible answers, one in which defence works through reach and one in which it cannot work at all. Neither occurred. Every configuration raises $Pi$ above the undefended baseline for its first 9 to 24 steps and lowers it permanently thereafter; panel (a) of @fig:h3 shows the three defended runs and the undefended baseline together, and panel (b) subtracts the baseline from each, so that the moment a defence starts helping is the moment its curve crosses zero. Broad and shallow ($alpha_C = 0.15$, $rho_C = 0.60$) overshoots by $0.077$ for nine steps and ends at $Pi(399) = 0.106$; narrow and deep ($0.90$, $0.10$) overshoots by $0.239$ for 24 steps and ends at $0.020$; matched to $D$'s values ($0.70$, $0.25$) overshoots by $0.135$ for eleven steps and ends at $0.045$, against an undefended baseline of $0.179$. All three lower $Pi$ at the horizon, in 95 to 98 per cent of seeds. Whether defence works has no single answer, because the difference from the undefended baseline changes sign at a step that depends on the configuration: the endpoint says defence works, the transient says it backfires, and both are true of the same run. A directional question about a dynamic process needs a time attached to it, and H3, as we registered it, did not have one.

The ordering of the three configurations carries the substance. The largest overshoot belongs to narrow and deep, the configuration with the lowest reach and therefore the smallest immediate cost, which rules out the first channel. The second channel produces it: pulling agents toward $p_C$ narrows moral distance only if it moves them toward the population's bulk, and at withdrawal the bulk sits at $overline(b) = +0.29$. Taking a tenth of the population to $-1$ in a single step does the opposite, driving mean othering exposure from $0.190$ to $0.309$ and $Pi$ to $0.467$, 61 per cent above what the panic would have been had nobody answered back. The defence of the stigmatised position, mounted intensively on a small base, is briefly the most panic-generating act in the study. The gate at work is the one that governs ignition, operated from the other side: $alpha_C = 0.15$ never exceeds tolerance and $overline(Phi)$ falls immediately, while $alpha_C = 0.90$ severs ties on contact and cleaves the population again before healing it.

#figure(
  image("fig3_h3_defense.pdf", width: 100%),
  caption: [Defence. (a) $Pi$ through $C$'s entry, for the three defended configurations and the undefended baseline. (b) each defended configuration with the baseline subtracted, so that zero is "the defence changed nothing" and the marked crossings are where it starts to help. (c) each run as a path across the $(overline(b), Pi)$ plane, from withdrawal (star) to the horizon (dot), which shows the fall in panic arriving together with the conversion of the population. (d) what is left at the horizon, $Pi(399)$, plotted against each of $C$'s two levers one at a time, with the guide $Pi = 0.18 rho_C$ drawn in. Mean over 250 seeds, 125 in panel (d).],
) <fig:h3>

The eventual reduction works by conversion. In all three configurations $Pi$ falls because $overline(b)$ goes to $-0.99$ and mean othering exposure collapses to $0.005$, the value of a population with nothing left to other. Panel (c) of @fig:h3 is where this is easiest to see: it plots each run as a path across the plane of mean position against panic, from the common start at withdrawal (star) to the end of the run (dot). The three defended paths all travel to the far left and end there, with the population converted; the undefended run holds its position and simply decays in place, which is the persistence of Section 3.2 seen from another angle. The counter-entrepreneur does not calm anyone; it wins totally, and a population that agrees about everything has no moral distance to be alarmed by. That is the only route the model leaves open, since no message in it can say _there is no threat_: alarm falls only when there is nothing left to disagree about. The finding is therefore conditional on that exclusion and is not a claim about what real counter-campaigns can achieve; Section 4.3 names the extension that would settle it.

The residue at the horizon is the price of speaking. Moving each of the counter-entrepreneur's two levers on its own, as panel (d) of @fig:h3 does, residual disproportion is $approx 0.18 rho_C$, running $0.020$ to $0.185$ as $rho_C$ goes from $0.10$ to $1.00$, and flat in depth at $0.087$ to $0.088$ across $alpha_C$. It depends on how many people the defence talks to, and not at all on how hard it argues. Every claims-maker enters the alarm neighbourhood of everyone it reaches as a maximally alarmed contact, and alarm is undirected, so once the population is converted that contact is all that is left. A defence cannot lower the panic index below what its own broadcasting costs, and the wide campaign of reassurance ends with five times the residual alarm of the narrow one, not because it reassures worse but because it keeps talking to more people.

== Robustness

A finding that holds only at the exact settings it was found at is a property of those settings and not of the model. This section varies the things that ought to make no difference, and confirms that they make none. The headline numbers are invariant to population size ($Pi(149) = 0.292$, $0.292$, $0.293$ at $N = 500, 1000, 2000$; only the spread across seeds moves, narrowing as the population grows at the rate ordinary sampling would predict) and to the update scheme (updating agents one at a time in random order, instead of all together, moves it by $0.010$, inside that dispersion). Replication on two public networks @leskovecGraphEvolutionDensification2007 @mcauleyDiscoveringSocialCircles2014, each accompanied by the three generators re-run at its own realised size and mean degree, shows that the parameters, not the graph, decide the episode produced _while an entrepreneur is acting_: across eight rows spanning an eightfold range of mean degree, $Pi(149)$ lies between $0.227$ and $0.270$. Structure decides what survives. In the dense graph it decides nothing, all four versions landing between $0.191$ and $0.198$; in the sparse one it decides a factor of twenty, and it does so in strict order of how likely two of a person's contacts are to know each other: $0.135$, $0.100$, $0.072$ and $0.006$ as that likelihood falls from $0.53$ to almost nothing. The mechanism is visible in the rules. Bounded confidence cuts the population into groups, and a group holds together only while its members reinforce one another faster than drift pulls them apart; mutual acquaintance supplies that reinforcement. Sparse and unacquainted is the one combination in which manufactured division fails to outlive the campaign.

Two checks belong to the instrument itself, and each guards against a way the paper could be claiming more than it has. The first asks whether the division we report is a real split in the population or an artefact of a scale that has to stop somewhere: agents pushed to the end of the range pile up against it, and a heap at each end would look like two camps without anyone having taken sides. Dropping every agent pinned at a pole leaves the bimodality coefficient unchanged to three decimals, and a version of the bound that can never pin anybody leaves $Pi$ within $0.008$, so the camps are camps.

The second asks how long the counterfactual comparison stays trustworthy. Two worlds that begin identically are compared step by step, but each accumulates its own random nudges, and eventually the difference between them owes as much to that accumulation as to the campaign we removed. Re-drawing the noise locates where this begins to bite, and it falls between $t = 191$ and $t = 289$ in three of five audited seeds. Beyond that point a single trajectory says little, which is why $Pi(399)$ is reported as a distribution over 250 populations and never as a curve through time.


// ─────────────────────────────────────────────────────────────────────────────
= Discussion
// ─────────────────────────────────────────────────────────────────────────────

== What the apportionment settles

Whether panics are held up by elite claims-makers or by the reaction of the public itself is disputed @goodeMoralPanicsCulture1994 @mcrobbieRethinkingMoralPanic1995, and the dispute has stayed rhetorical for want of any way to apportion the two. The four-run design apportions them, 14 per cent to 2 per cent to 84 per cent.

Neither camp is right as usually stated. The entrepreneur is _necessary_: where nobody campaigns nothing happens, and where the campaign is too mild to be disowned nothing happens either. It is also nearly irrelevant to the size of what follows. Its achievement is to divide the population far enough that alarm becomes self-sustaining, after which it is no longer needed. That has a consequence for how panics end, or fail to. The claims-maker cannot undo what it started, because the excess alarm no longer rests on the campaign; only a population for whom disagreement is not in itself frightening will shed that alarm entirely. Any intervention therefore has an object other than "stop the campaign", and the model names what an empirical study would have to measure: how morally far apart people are from those they actually talk to, in place of how much campaigning there is. The mechanism has a cousin in the cascade literature, where public reaction outruns the information that started it @kuranAvailabilityCascadesRisk1999. The two differ in what does the reinforcing: information and reputation there, disagreement itself here.

== Predictions for empirical research

#h4[Ignition depends on repeated exposure to the same audience] The mass broadcaster is, on this model, structurally the worst available moral entrepreneur. A campaign that reaches everyone equally leaves nobody more exposed than anyone else, and the population then moves as one: no division is manufactured and no episode occurs under any reading of the criterion. A claims-maker becomes dangerous by addressing some people and not others, repeatedly, so the fragmentation of audiences belongs to the mechanism itself and not merely to the setting in which the mechanism runs. The prediction is uncomfortable for a common intuition about mass media, since it implies that the mass-press episodes of the classic literature @cohenFolkDevilsMoral1994 and contemporary platform cases @carlsonFakeNewsInformational2020 @walshSocialMediaMigration2023 are doing different things under one label, and it makes the difference measurable, through the unevenness of exposure and not its volume. One caution comes from the same control. Since most of what targeting the well-connected achieves is achieved just as well by a fixed audience chosen at random, targeting by connectedness is a weak stand-in for algorithmic amplification, and nothing here licenses a claim about platform ranking.

#h4[Local density decides whether a panic outlives its campaign] Across two real networks and their matched synthetic counterparts, how large an episode grows while the campaign runs barely depends on the network at all; the network governs instead how much of the episode is left afterwards, and in the sparse case that is decided by how likely two of a person's contacts are to know one another. The mechanism is the one described in the results: division survives only inside groups whose members hold each other in place, and mutual acquaintance does the holding. The comparative prediction is direct. Two societies with the same campaigning, the same tolerance for disagreement and the same susceptibility to alarm will differ in whether the panic outlives the campaign, according to how tightly knit their everyday social ties are. This came from the real networks; no synthetic generator reproduced it.

#h4[Answering back intensifies the episode before it ends it] The organised defence of a stigmatised position raises disproportion for its first 9 to 24 steps, and most when it is most committed. The constructivist literature has long described defence and resistance as part of what escalates an episode @hierFolkDevilResistance2011 @zielinskaPolarizingMoralPanics2022, and the model supplies a mechanism involving neither tone nor provocation nor backlash psychology, none of which exist here. It is arithmetic on moral distance: the defence's own converts become the population's most distant neighbours, and such distance frightens @ameryOtheringPeakingPopulism2025.

A methodological warning belongs beside these. Panic incidence in our runs jumps where the underlying disproportion moves smoothly, so empirical episode counts, which apply coding rules to continuous public reaction, may inherit their sharpness from the coding rule.

== Limitations

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

The concept was built around a comparison that remains uncomputed. Our index measures excess against the model's own campaign-free world, and no run of it can say that a real episode was out of proportion to a real danger; the criterion is made computable here, not decidable. Two extensions strike where the results are weakest. The first is a claims-maker able to lower alarm directly, and not only by winning the argument, since our defence finding is conditional on no such claims-maker existing. The second is a social network that changes as the episode runs, since every simplification in the present design pushes in the same direction, toward _under_-stating how far a population can come apart.


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
    [$D$, $C$], [entrepreneur, counter-entrepreneur], [the two claims-makers; outside the network, and never alarmed themselves],
    [$p_D$, $p_C$], [poles], [the position each argues for, $+1$ and $-1$],
    [$rho_X$], [reach], [_#sym.rho for reach_: the share of the population a claims-maker addresses each step],
    [$n_X$], [audience size], [how many people that share works out to, $ceil(rho_X N)$ of them],
    [$alpha_X$], [depth], [_#sym.alpha for the strength of the ask_: how far toward its own pole a claims-maker moves those it reaches],
    [$g^X_i (t)$], [reached or not], [$1$ if claims-maker $X$ reaches $i$ this step, $0$ otherwise],
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
  ("Moral Panic.bib", "Computational Methods.bib"),
  style: "american-sociological-association.csl",
  title: "References",
)
