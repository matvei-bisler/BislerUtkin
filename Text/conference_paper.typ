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
// Self-contained: no appendix, no deposit, no pointers outside this text.
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
      Agent-Based Modelling of "Moral Entrepreneurship" and the Dynamics of
      Moral Panics in Social Networks
    ]
  ]

  #v(1.1em)

  #text(size: 11.5pt)[Matvei A. Bisler#super[\*] #h(1.2em) Sergei R. Utkin#super[\*\*]]

  #v(0.4em)

  #block(width: 88%)[
    #set text(size: 9pt)
    #set par(justify: false, first-line-indent: 0pt, leading: 0.6em)
    #super[\*] Doctoral School of Political Science, HSE University; Universal University \
    #super[\*\*] Doctoral School of Political Science, HSE University; International Center
    for the Study of Institutions and Development
    // TODO: corresponding author's email, if the venue requires one.
  ]
]

#v(1.4em)


// ── Abstract ─────────────────────────────────────────────────────────────────

#block(width: 100%, inset: (x: 1.2em))[
  #set text(size: 10pt)
  #set par(justify: true, first-line-indent: 0pt, leading: 0.68em)

  *Abstract.* Disproportion is central to how moral panic is defined and is almost
  never measured: no one can observe how alarmed a population would have been without
  the claims-making that alarmed it. This paper makes that comparison computable. We
  specify an agent-based model in which 1,000 networked agents carry two coupled
  states, a moral position and a level of alarm, updated through bounded confidence,
  threshold contagion, and othering, the conversion of local moral disagreement into
  perceived threat. Two claims-makers act on the population from outside. Every
  setting is run four times on one seed in a $2 times 2$ design (claims-making on/off
  $times$ othering on/off), which decomposes aggregate alarm exactly and returns
  disproportion directly. Three pre-registered hypotheses were tested across some
  292,000 runs. Amplification requires a stable audience rather than well-connected
  targets: a repertoire that resamples its audience each step never exceeds its own
  forcing, and at full reach no repertoire produces a panic at all. At the operating
  point, 84% of manufactured alarm is the interaction between campaign-created
  division and othering, and 62% of disproportion survives 250 steps after the
  entrepreneur withdraws. Counter-claims-making raises disproportion for 9 to 24 steps
  before lowering it, and lowers it only by converting the population. Disproportion
  here is excess over the model's own counterfactual, not over real danger.

  #v(0.7em)

  *Keywords:* moral panic; moral entrepreneurship; agent-based modelling; social
  networks; opinion polarization.
]

#v(1.4em)


// ─────────────────────────────────────────────────────────────────────────────
= Introduction
// ─────────────────────────────────────────────────────────────────────────────

Since Cohen's study of the mods and rockers, moral panic has named a recognisable
sequence: a condition, episode, or group is defined as a threat to societal values;
the definition is promoted and amplified by claims-makers; and the reaction that
follows exceeds what the threat itself warrants @cohenFolkDevilsMoral1994
@goodeMoralPanicsCulture1994 @garlandConceptMoralPanic2008. Two roles carry the
sequence. Moral entrepreneurs define the boundary and campaign for it
@beckerOutsidersStudiesSociology1997; folk devils are the simplified figures onto
which deviance is projected. The framework travels widely. In the last five years
alone it has been applied to cyber-organised crime
@lavorgnaCyberorganisedCrimeCase2019, misinformation and platform activism
@moranMisinformationActivismAnalyzing2023, immigration politics
@zhangMoralPanicInsecurity2025, school curricula @leeds1619ProjectMoral2024, gender
quotas @shiranBacklashQuotasMoral2024, and organised transphobia
@ameryOtheringPeakingPopulism2025.

That reach has not been matched by measurement. #cite(<goodeMoralPanicsCulture1994>, form: "prose")
define panic partly by *disproportion*, concern in excess of what the situation
warrants, and disproportion requires a comparison that empirical work can rarely
make: one cannot observe how alarmed a society would have been without the
claims-making that alarmed it. The counterfactual is unobservable, so the criterion
is asserted rather than demonstrated. Reviews of the field register the consequence.
Panic is invoked as self-evident while the criteria for recognising it go unstated
@falkofMoralPanicDirections2020 @garlandConceptMoralPanic2008
@mihaylovaKtoIspolzuetPonyatie2020, and #cite(<hierRethinkingProblemDisproportion2024>, form: "prose")
treats disproportion as the field's central unresolved problem. The same gap lies
under its long-running disputes over agency, temporality, normative commitment, and
how far the concept can be stretched before it stops discriminating
@davidIdeaMoralPanic2011 @critcherMoralPanicAnalysis2008 @cohenWhoseSideWere2011
@hierMoralPanicStudies2023.

A second limitation concerns how the framework's elements are studied. Moral
entrepreneurs, folk devils, and panic itself are usually treated as three objects
with three literatures, and their interaction is described rather than formalised.
Work on networked panics has moved well beyond the mass-mediated model
@mcrobbieRethinkingMoralPanic1995 @walshSocialMediaMoral2020
@carlsonFakeNewsInformational2020 @obrienComingStormMoral2023
@lemishSocialMediaMoral2023 @humphryAnxietyAgeMoral2026, yet entrepreneur and folk
devil are often retained as statuses rather than as positions in a contest, when in
practice stigmatised groups routinely act as entrepreneurs of their own defence
@mikhaylovaFolkDevilsMoral2022 @hierFolkDevilResistance2011. And the dominant
instruments --- discourse and framing analysis, case studies, ego-network description
@mihaylovaVozmozhnostiPrimeneniyaEgosetevogo2021 @mihaylovaIzmerenieMoralnoyPaniki2022
--- are interpretively strong but are not built to show how micro-level interaction
generates macro-level escalation over time.

A simulation can do what a case study cannot: run the counterfactual. The same
population, the same network, the same initial draws, executed with and without the
claims-making that is supposed to have caused the alarm. The difference is
disproportion, computed rather than argued. Doing this makes a second and older
question answerable. Alarm in the model has two manufactured sources, one injected by
claims-makers from outside and one generated by the population itself through
exposure to moral disagreement, and each can be switched off independently. Four runs
on one seed therefore isolate what either contributes alone and, more importantly,
the alarm that exists only because both are present. Our claim concerns that third
quantity: *a moral panic is ignited by claims-makers but sustained by the population
they divide.* This is an apportionment and not a chronology, a distinction we return
to in Section 3.2, because the transfer in this model is immediate rather than
gradual. It is also a numerical answer to a dispute that has been conducted
rhetorically, since whether panics are held up by elite claims-makers or by the
reaction of the public itself separates elite-driven from interactionist accounts and
no one could apportion the two. The research question follows: which claims-making
strategies ignite moral panic, under which network structures, and once ignited, what
sustains it?

Six parameters and four rules govern a population of agents, each carrying a moral
position and a level of alarm, connected in a static network and pushed at by two
external claims-makers. Positions move through bounded confidence and claims-maker
forcing; alarm moves through memory, contagion, and *othering*, the conversion of
local moral disagreement into perceived threat. Three hypotheses were registered
before the program was run, one per phase of an episode, and tested across roughly
292,000 simulation runs. Two clauses of the first, the ordering clause of the second,
and both pre-specified branches of the third failed. We report the registered wording
beside the outcome rather than rewriting predictions into descriptions, since the
third result means something only because two branches were fixed in advance and
neither occurred.

The paper makes three contributions. First, it makes the disproportionality criterion
computable, so that the elite-versus-interactionist dispute becomes an apportionment
between two terms rather than a matter of emphasis. Second, it identifies the
condition under which claims-making ignites anything at all, and that condition is
neither volume nor structural position but a stable audience, which makes universal
reach the one strategy that cannot produce a panic. Third, it supplies a mechanism
for something the constructivist literature has long observed qualitatively, that
organised defence of a stigmatised position tends to intensify an episode before it
ends it. Methodologically the paper joins a small body of generative and normative
agent-based work in sociology and political science
@epsteinGenerativeSocialScience2006 @hollanderCurrentStateNormative2010
@guoModelingSimulatingOnline2021 @ahremenkoKakInformacionnokommunikacionnyeTehnologii2023,
and treats moral panic as an escalation process rather than as a norm cascade
@finnemoreInternationalNormDynamics1998.


// ─────────────────────────────────────────────────────────────────────────────
= Model and methods
// ─────────────────────────────────────────────────────────────────────────────

The model carries six parameters and four rules. Four parameters are global and two,
depth and reach, are set per claims-maker, so a run with both actors active fixes
eight numbers.#footnote[
  The description follows the ODD protocol @grimmStandardProtocolDescribing2006
  @grimmODDProtocolReview2010 @grimmODDProtocolDescribing2020 in substance rather
  than in its section order.
] What the model leaves out is stated in Section 4.3.

== Entities, states, and structure

The model contains $N$ agents, a fixed undirected graph, and two external
claims-makers. Each agent carries two dynamic states: a *moral position*
$b_i (t) in [-1, 1]$, running from full alignment with the stigmatised position to
full alignment with the dominant moral claim, and *alarm* $a_i (t) in [0, 1]$, the
level of perceived social danger. Alarm is deliberately undirected --- it records how
alarmed an agent is, not what it fears, with the object read off jointly with $b_i$.
Each agent also carries a fixed panic threshold $theta_i$, past which it begins
amplifying. Threshold dispersion is the only heterogeneity retained, because it sets
what share of the population amplifies at a given level of alarm, and that share is
the gain of the reinforcement loop below @granovetterThresholdModelsCollective1978.

Structure is the primary explanatory variable of the first experiment. Three
generators are used at matched mean degree, each isolating one documented feature of
real social networks: the Watts--Strogatz small world, with short paths and high
local clustering @wattsCollectiveDynamicsSmallworld1998; preferential attachment with
clustering @holmeGrowingScalefreeNetworks2002, which supplies hubs together with the
triangles that plain preferential attachment lacks
@barabasiEmergenceScalingRandom1999; and the Erdős--Rényi random graph
@gilbertRandomGraphs1959, with neither, as the structural null. Following
#cite(<broidoScalefreeNetworksAre2019>, form: "prose"), the second is called
hub-dominated rather than scale-free. Runs use the full graph rather than its giant
component, since isolation is substantively meaningful: an agent reachable only by a
claims-maker is a real sociological position.

Two strategic actors push at this system from outside it. The *moral entrepreneur*
$D$ promotes the dominant moral claim and pushes agents it reaches toward $p_D = +1$;
the *counter-entrepreneur* $C$ pushes toward $p_C = -1$, representing the niche media
through which folk devils answer back @mcrobbieRethinkingMoralPanic1995. Neither is
an agent: they have no internal state, no position in the network, and cannot
themselves be alarmed. Standing outside it is what makes the two sources of alarm
separable, since an actor inside would both cause and absorb alarm. The symmetric
design follows #cite(<mikhaylovaFolkDevilsMoral2022>, form: "prose"): the
entrepreneur/folk-devil distinction is a position within a contest rather than a
fixed status. The folk devil is correspondingly *not* an actor here but the
stigmatised pole around which alarm and clustering emerge, which preserves the
constructivist insight that folk devils are constituted through attribution.

Initial positions are $"Uniform"[-0.2, 0.2]$ in the consensual default, against an
already-divided contrast drawn as an equal mixture of
$"Normal"(plus.minus 0.7, 0.15)$; thresholds are $"Uniform"[0, 1]$, against a
constant $theta = 0.5$. Initial alarm is $"Uniform"[0, 0.1]$, low but non-zero, which
is load-bearing: that baseline is what the model means by *warranted* concern.
@tab:params lists the parameters and their operating-point values.

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
    [$zeta$], [s.d. of position noise], [$>= 0$], [$0.01$], [---],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Parameters and fixed constants. The upper block is swept; the lower block
    is held fixed and replicated at alternative values. $X in {D, C}$ indexes the two
    claims-makers.],
) <tab:params>

== The four rules

#h4[Targeting] Each active actor $X$ reaches $n_X = min(N, ceil(rho_X N))$ agents per
step, setting $g^X_i (t) = 1$ for those it selects. `random` draws a uniform subset,
redrawn every step, and at $rho_X = 1$ it is mass broadcast; `hub` takes the $n_X$
highest-degree nodes; `base` takes the $n_X$ agents closest to the actor's own pole,
rallying the already committed; `fixed_random` draws a uniform subset once and
addresses it every step. The fourth is a measuring instrument, not a strategy: `hub`
and `base` differ from `random` in *whom* they select and in selecting *the same
people repeatedly*, so `random` against `fixed_random` isolates the exposure schedule
and `fixed_random` against `hub` isolates degree.

#h4[Peer influence] An agent is moved only by neighbours close enough to still be
worth listening to. Writing $Delta_(i j)(t) = |b_i (t) - b_j (t)|$ for moral
distance, $cal(N)_i$ for $i$'s neighbours, $d_i$ for its degree, and
$kappa_j (t) = gamma$ if $a_j (t) > theta_j$ and $1$ otherwise for the social weight
of an amplifying agent, the peer pull is

$ S_i (t) = cases(
  (sum_(j in cal(N)_i) kappa_j (t) bb(1) [Delta_(i j)(t) <= epsilon] (b_j (t) - b_i (t))) / (sum_(j in cal(N)_i) kappa_j (t)) & "if" d_i > 0,
  0 & "if" d_i = 0.
) $ <eq:peer>

This is bounded confidence without repulsion, following Hegselmann and Krause (2002)
and #cite(<deffuantMixingBeliefsInteracting2000>, form: "prose");
#cite(<flacheModelsSocialInfluence2017>, form: "prose") survey the wider family.
Agents disengage from the morally distant but are not driven away by them, which
keeps divergence attributable to one mechanism. The denominator runs over *all*
neighbours, so being surrounded by the morally distant reduces how far an agent
moves.

#h4[Position update] Agents a claims-maker reaches are pulled toward its pole with
strength set by depth and by the distance still to travel,
$I^D_i (t) = alpha_D g^D_i (t)(1 - b_i (t))$ and
$I^C_i (t) = alpha_C g^C_i (t)(1 + b_i (t))$, so that an actor acting alone maps
$b_i arrow.r.bar (1 - alpha_X) b_i + alpha_X p_X$ and can never push anyone past a
pole. Positions then update as

$ b_i (t+1) = "clip"_([-1,1])[ underbrace(sigma b_i (0), "anchor") + (1 - sigma)(underbrace(b_i (t), "persistence") + underbrace(S_i (t), "peers") + underbrace(I^D_i (t) - I^C_i (t), "claims-makers")) + underbrace(xi_i (t), "noise") ], $ <eq:position>

with $xi_i (t) tilde.op "Normal"(0, zeta^2)$. Here $sigma$ is the Friedkin--Johnsen
anchor weight @friedkinSocialInfluenceOpinions1990, set to zero for a substantive
reason: $sigma b_i (0)$ is a restoring force toward each agent's *pre-campaign*
position, which under a consensual start sits near zero, so any positive $sigma$
returns the population to consensus on its own timescale, $-1 slash ln(1 - sigma)$
steps, whatever $omega$ is, dissolving exactly the manufactured division this paper
is about. Preventing the trivial consensus of plain neighbour averaging
@degrootReachingConsensus1974 is the only other work the anchor would do, and bounded
confidence already does it. Depth appears here and nowhere else: it scales
persuasion, not alarm, and an actor is silenced by $rho_X = 0$, never by
$alpha_X = 0$.

#h4[Alarm update] Alarm is caught rather than reasoned into. A claims-maker enters
the neighbourhood of each agent it reaches as one maximally alarmed, permanently
amplifying contact; writing $m_i (t) = g^D_i (t) + g^C_i (t)$ for the number of
claims-makers reaching $i$, alarm exposure and othering exposure are

$ E_i (t) = min(1, (sum_(j in cal(N)_i) kappa_j (t) a_j (t) + gamma m_i (t)) / (d_i + m_i (t))), quad
  Phi_i (t) = (sum_(j in cal(N)_i) kappa_j (t) Delta_(i j)(t) slash 2) / (sum_(j in cal(N)_i) kappa_j (t)), $ <eq:exposure>

both zero for an isolate no actor reaches, and alarm updates as

$ a_i (t+1) = "clip"_([0,1])[ underbrace(mu a_i (t), "memory") + underbrace(delta E_i (t), "contagion") + underbrace(omega Phi_i (t), "othering") ]. $ <eq:alarm>

Two features of $E_i$ are load-bearing. Both claims-makers raise alarm, because alarm
is undirected: a message that a threat exists is alarming whoever sends it. And the
denominator is the neighbour *count* rather than the total weight, which would make
$E_i$ a weighted mean, incapable of exceeding its largest input; dividing by the
count lets amplifying neighbours *add*, which is the reinforcement complex contagion
describes @granovetterThresholdModelsCollective1978
@centolaComplexContagionsWeakness2007 and why the expression carries a cap at $1$.
Othering exposure excludes claims-makers: it is the experience of being surrounded by
morally distant *peers*, not of receiving a message.

Together, @eq:peer and @eq:exposure produce the model's central asymmetry. A
neighbour beyond an agent's tolerance contributes *nothing* to its position and *the
most* to its alarm: such neighbours cannot change its mind, and they are the ones who
frighten it. A population sorted into opposed camps manufactures its own alarm, and
all three hypotheses rest on this.

== Measuring panic

Alarm has two manufactured sources and each can be switched off independently:
claims-making by silencing both actors, othering by setting $omega = 0$. Every
setting is therefore executed four times on the identical seed, in a $2 times 2$
design whose arms we write $bar(a)^"null"$ (both off), $bar(a)^"cm"$ (claims-making
only), $bar(a)^"oth"$ (othering only) and $bar(a)$ (both on). The seed fixes the
network, the initial positions, the alarm and the thresholds, so the four arms are
the same population under different forcings, and they decompose aggregate alarm
exactly at every step:

$ bar(a) = underbrace(bar(a)^"null", "warranted")
  + underbrace(bar(a)^"cm" - bar(a)^"null", "claims-making alone")
  + underbrace(bar(a)^"oth" - bar(a)^"null", "othering alone") \
  + underbrace(bar(a) - bar(a)^"cm" - bar(a)^"oth" + bar(a)^"null", "interaction"). $ <eq:decomp>

The interaction term is the object of interest rather than a residual: it is the
alarm that exists only because claims-making and othering are both present, the
division an entrepreneur creates amplified by a population that then finds its own
divisions frightening. A purely additive world would leave it at zero. One further
property carries much of the argument. Under common random numbers all four arms
occupy the same state at $t = 0$, so the term is identically zero at $t = 1$ and can
first become non-zero at $t = 2$, through one route only: claims-making has moved
positions, changing the moral distances othering reads. The interaction therefore
carries no component of the population's initial dispersion.

Disproportion is the total excess over what the situation warrants, normalised by the
room available for it:

$ Pi(t) = (bar(a)(t) - bar(a)^"null"(t)) / (1 - bar(a)^"null"(t)) in [0, 1]. $ <eq:pi>

A *moral panic episode* is a period of at least $W$ consecutive steps during which
both $Pi(t) >= Pi^*$ and $q(t) >= q^*$, where $q(t)$ is the share of the population
past its threshold. Requiring both distinguishes panic from widespread but
proportionate concern, which is high $q$ at low $Pi$, and from successful
manipulation of a small minority, which is the reverse; in the terms of
#cite(<goodeMoralPanicsCulture1994>, form: "prose"), the pair operationalises
disproportionality and approximates consensus. Since $Pi^*$, $q^*$ and $W$ are conventions rather than findings,
incidence is reported over a grid of all three. Alongside $Pi$ we record persistence
after withdrawal, mean position, mean othering exposure, Sarle's bimodality
coefficient @pfisterGoodThingsPeak2013 and the exposure concentration
$"Var"_i (sum_t g^D_i (t))$, which separates repertoires addressing the same people
repeatedly from those spreading exposure thinly.

Two conditions keep the instrument meaningful. Alarm stays in range whenever
$mu + delta + omega <= 1$, imposed by construction on every sampled vector, and the
calm regime is sub-critical whenever $mu + delta < 1$. Contagion must also stay below
the threshold at which alarm self-sustains from any positive seed whatever a
claims-maker does, since there the decomposition loses its point. That boundary is a
surface in the simplex rather than a value of $mu + delta$, because an amplifying
neighbour enters at weight $gamma$, so it is *measured* at every reported point:
silence both actors, set $omega = 0$, seed a few per cent at full alarm, and check
that alarm dies.

== Experimental design and verification

The operating point throughout is a Watts--Strogatz small world with $N = 1000$ and
mean degree $10$; $epsilon = 0.5$, $mu = 0.30$, $delta = 0.25$, $omega = 0.35$;
$sigma = 0$, $gamma = 3$, $zeta = 0.01$; the entrepreneur on `base` with
$alpha_D = 0.7$ and $rho_D = 0.25$, withdrawing at $t_"off" = 150$; horizon
$T = 400$. Experiment A crosses the four repertoires with the three topologies and
the two initial position regimes, with $C$ silent, raising reach in fine increments
and varying depth against reach on a full grid, since the two interact. Experiment B
re-runs the settings that reliably ignite with $rho_D arrow 0$ at $t_"off"$, tracking
@eq:decomp across the withdrawal and sweeping the alarm parameters. Experiment C is
the only one in which both actors appear, $D$ withdrawing at $t_"off"$ and $C$
entering there at three configurations chosen to span the dilemma rather than map
it.

Every quantity is a distribution over seeds, with panic incidence as a frequency,
never a single run. At 250 seeds per setting the Monte Carlo standard error on
incidence is at most $plus.minus 0.032$, and since each seed carries all four runs
the headline program is 72,990 counterfactual sets, or 291,960 simulation runs,
taking 54 minutes on 15 cores.

Sensitivity analysis is confined to the three alarm parameters, the only ones
entering H2's testable claim. Sampling them independently on $[0,1]^3$ would be
wrong, since the range condition confines them to a simplex and rejecting violations
makes the surviving inputs dependent; the design therefore reparameterises as
$mu = s p_mu$, $delta = s p_delta$, $omega = s p_omega$, with intensity $s$ uniform
on $[0,1]$ and the split $(p_mu, p_delta, p_omega)$ uniform on the 2-simplex, so that
the Sobol inputs @sobolGlobalSensitivityIndices2001 are independent by construction.
The noise constant $zeta$ enters as a fourth input over two boxes, because at
$sigma = 0$ the permanence of division is exactly the frozen state noise exists to
prevent. Indices use the Saltelli design with the Jansen estimator
@saltelliVarianceBasedSensitivity2010 @jansenAnalysisVarianceDesigns1999, written
directly rather than taken from a library and docked against the Ishigami function
@ishigamiImportanceQuantificationTechnique1991 to within $0.0025$.

That the code implements the specification is established separately from any
substantive result, by docking against five models with known behaviour --- plain
neighbour averaging, the Friedkin--Johnsen equilibrium, the Hegselmann--Krause
cluster count, the mean-field fixed point of the alarm recursion, and the empty
graph, on which the full and null runs coincide and $Pi$ is identically zero. All
fourteen verification and property checks pass. The implementation is Python with
`networkx` @hagbergExploringNetworkStructure2008 and `numpy`
@harrisArrayProgrammingNumPy2020, and all randomness derives from one recorded seed
through three substreams, for setup, targeting and noise: sharing a stream between
targeting and noise would desynchronise the four arms, and the counterfactual would
no longer hold the same population fixed.

The three hypotheses, and both possible outcomes of the third, were fixed in writing
before the program was run, and where the runs contradicted a registered clause the
wording has not been revised. Section 3 states each hypothesis as registered and then
reports what happened. The third result in particular means something only because
two branches were fixed in advance and neither occurred.


// ─────────────────────────────────────────────────────────────────────────────
= Results
// ─────────────────────────────────────────────────────────────────────────────

The conditioning required by Section 2.3 holds throughout. At the operating point
$mu + delta = 0.55$ and the measured sub-criticality probe passes, seeded contagion
dying to a resting mean alarm of $4 times 10^(-53)$. Across all seeds
$max_t bar(a)^"null" = 0.052$, so the denominator of @eq:pi stays in $[0.948, 1]$.
Mean othering exposure at initialisation is $bar(Phi)(0) = 0.067$ under the
consensual default against $0.386$ under the polarised contrast, so pre-existing
moral distance is negligible by construction. The three generators are matched on
mean degree ($10.00$, $9.94$, $9.88$) and differ where they are meant to: clustering
is $0.487$, $0.212$ and $0.010$, and degree dispersion is $1.00$, $12.81$ and $3.22$
for Watts--Strogatz, Holme--Kim and Erdős--Rényi.

== Ignition

#registered[
  H1, as registered. Which repertoire ignites a panic depends on network topology,
  and ignition is amplifying but not discontinuous: $Pi > rho_D$ across the usable
  range, while the response stays smooth and saturating rather than jumping at a
  critical value. `hub` ignites fastest in hub-dominated networks and degenerates to
  `random` where degrees are even.
]

Amplification is the model's formal counterpart of a reaction out of proportion to
its cause: a point above the diagonal $Pi = rho_D$ in panel (a) of @fig:h1 is a
response larger than the forcing that produced it. It appears, but not for
claims-making as such. `hub` clears the diagonal from the smallest reach tested,
`base` and `fixed_random` clear it to $rho_D approx 0.4$, and `random` never clears
it at any reach, running at a flat $Pi slash rho_D approx 0.18$ --- the signature of
pure injection with no amplification. Which curves coincide says why:
`fixed_random` traces `base` almost exactly across the whole sweep, and the two have
nothing in common except a stable audience, since the control selects uniformly at
random and carries no degree signal. Amplification is a property of reaching *the
same people*, not of reaching *the right people*.

#figure(
  image("../Results/figures/fig1_h1_ignition.png", width: 100%),
  caption: [Ignition. (a) $Pi$ against reach for the four repertoires on the small
    world, with the diagonal $Pi = rho_D$ drawn in; (b) `hub` across the three
    generators, with `random` repeated as a light reference; (c) the interaction term
    against reach, circles marking each peak; (d) $Pi$ on the
    $alpha_D times rho_D$ grid, darker being higher, with the heavy rule where a
    reached agent's one-step displacement $alpha_D (1 - bar(b))$ crosses the tolerance
    $epsilon = 0.5$. Mean over 250 seeds; bands are $plus.minus 1$ s.d.],
) <fig:h1>

The registered clause that `hub` degenerates to `random` where degrees are even is
refuted, and the control identifies what it was really trading on. On Watts--Strogatz,
whose degree s.d. is $1.00$, `hub` still exceeds `random` by up to $14.8 times$.
Decomposing that advantage, `random` $arrow$ `fixed_random` isolates the exposure
schedule and is worth up to $7.0 times$, accounting for *all* of `hub`'s advantage at
$rho_D >= 0.30$, where the control exceeds `hub`; `fixed_random` $arrow$ `hub`
isolates degree and is worth a further $2.2$ to $2.5 times$ at $rho_D <= 0.10$ and
nothing above $0.25$. Exposure concentration closes the argument: at $rho_D = 0.10$,
$"Var"_i (sum_t g^D_i)$ is $18$ for `random` and $3600$ for `fixed_random`, the
attainable maximum, but only $2272$ for `hub`, whose audience churns where degrees
tie. `hub` is *less* concentrated than the control and still beats it at low reach,
the signature of a second, independent channel. A small budget benefits from
well-connected targets; a moderate one benefits only from consistency.

Topology moves `hub` and almost nothing else: its peak runs $0.475$, $0.433$ and
$0.386$ on Holme--Kim, Erdős--Rényi and Watts--Strogatz, while the other three
repertoires vary by less than $0.02$. The registered topology clause holds, but the
dependence belongs to one repertoire rather than to the model.

The sharpest structure lies in the axis the hypothesis treated as secondary. Panel
(d) of @fig:h1 reads row-wise: below $alpha_D (1 - bar(b)) approx epsilon$ everything
is flat at $Pi = 0.02$ to $0.13$ regardless of reach, because there the entrepreneur
*converts* rather than divides --- reached agents stay inside their neighbours'
tolerance and drag the population to the pole together, $bar(b) arrow 0.99$, with the
interaction term at zero. Above the gate the rows are nearly identical, while moving
along a row changes $Pi$ six-fold. Depth is a gate and reach is the dial, which
preserves the claim that legitimacy matters chiefly as access but gives it a
precondition: access converts into panic only where the claims-making is intense
enough to be disowned. A fine sweep locates the gate between $alpha_D = 0.62$ and
$0.68$, where the across-seed s.d. of $Pi$ inflates from $0.014$ to $0.064$: within
one cell some seeds cleave and others converge. That is the model's only knife-edge
behaviour, and it sits in depth rather than in reach.

Manufactured division peaks at intermediate reach and vanishes at full reach. The
interaction term peaks at $0.346$ (`fixed_random`) and $0.340$ (`base`) at
$rho_D = 0.50$ and at $0.289$ (`hub`) at $rho_D = 0.20$, then collapses to $0.002$
for every repertoire at $rho_D = 1$, where all four are the same rule and exposure
variance is exactly zero; panic incidence there is $0.00$ under every cut of the
criterion grid. The most powerful claims-maker imaginable, reaching everyone every
step, is the one that cannot divide anybody.

Two readings close the experiment. Incidence rises from $0.08$ to $0.96$ between
$rho_D = 0.15$ and $0.20$ while $Pi$ moves smoothly from $0.177$ to $0.234$ with an
across-seed s.d. of $0.015$: the apparent tipping point is in the instrument, not in
the model. And flattening the threshold distribution lowers $Pi$ by 35 to 40 per cent
at every reach while leaving the curve's shape and peak untouched, so dispersion sets
the gain of the reinforcement loop rather than the geometry of the response. Of the
nine registered clauses of H1, six held, two held only in part --- amplification and
the role of dispersion --- and one, the degeneration of `hub`, was refuted.

== Handover

#registered[
  H2, as registered. The claims-making-alone term rises first and then plateaus,
  while the interaction term rises later and overtakes it. After the entrepreneur
  withdraws, $Pi$ remains elevated for a duration governed by othering rather than by
  passive decay: persistence is maximised near the $omega$ vertex of the alarm
  simplex, the split carries a larger total Sobol index than the intensity does, and
  $Pi$ decays to zero when $omega = 0$ but to a positive floor when $omega > 0$.
]

The apportionment is not close. At the operating point the entrepreneur's own signal
contributes $0.041$ to mean alarm and the division it manufactures contributes
$0.246$, a ratio of $5.94$ to one reached within twenty steps and stable for the rest
of the campaign (@tab:h2, @fig:h2 panel (a)): 14 per cent of the manufactured alarm
is the claims-making signal, 2 per cent is pre-existing division, and 84 per cent is
the interaction. Its two channels separate cleanly, since at $t = 149$ mean othering
exposure is $0.189$ in the full run against $0.006$ in the othering-only run, so 97
per cent of the exposure sustaining the episode is over distance the campaign
created.

#figure(
  table(
    columns: 7,
    align: (center + horizon, center, center, center, center, center, center),
    inset: (x: 5pt, y: 4pt),
    table.hline(stroke: 0.8pt),
    table.header([$t$], [warranted], [claims\ alone], [othering\ alone],
                 [*interaction*], [$Pi$], [$q$]),
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
  caption: [The decomposition of @eq:decomp across withdrawal, mean over 250 seeds.
    The entrepreneur withdraws at $t_"off" = 150$; the rule marks that step. $q$ is
    the share of the population past its threshold.],
) <tab:h2>

The registered *ordering*, however, fails. The interaction overtakes claims-alone at
$t = 2$ --- the earliest step at which Section 2.3 permits it to be non-zero --- in
250 of 250 seeds, and at every one of eight depths spanning the gate. There is no
regime in which the panic belongs to the entrepreneur for a while and to the
population later, because at $alpha_D > epsilon$ ties are severed on contact: the
division is complete on the first step and othering works on the second. What
survives is the composition claim, not the phase story, which is why the paper's
thesis is an apportionment.

What the entrepreneur leaves behind outlives it. Claims-alone falls to zero within
five steps of withdrawal, and 250 steps later $Pi$ retains 62 per cent of its value
at withdrawal, censored at the end of the run in 210 of 250 seeds. The floor is made
of othering and nothing else: sweeping $omega$ at fixed $mu + delta = 0.55$, so that
total intensity cannot move, $Pi(399)$ rises monotonically from $0.000$ at
$omega = 0$ to $0.286$ at $omega = 0.45$ --- exactly zero where disagreement is not
itself alarming.

#figure(
  image("../Results/figures/fig2_h2_handover.png", width: 100%),
  caption: [Handover. (a) the four decomposition terms through the run, with the
    dotted vertical at withdrawal and the arrow marking the 5.94-to-one ratio of
    interaction to claims-alone; (b) $Pi$ at withdrawal and 250 steps later against
    $omega$, at fixed $mu + delta$; (c) residual $Pi(399)$ over the simplex of alarm
    splits at fixed intensity, the circle marking the maximum and the crosses the four
    points that fail the sub-criticality probe; (d) total-order Sobol indices on the
    reparameterised inputs.],
) <fig:h2>

Two independent instruments locate that dependence in the *split* between the three
alarm parameters rather than in their total intensity. On the simplex at fixed
intensity, four of 45 lattice points fail the sub-criticality probe, all near the
$delta$ vertex and all with $mu + delta <= 0.60$, which is why a scalar threshold in
$mu + delta$ is not safe: an amplifying neighbour enters at weight $gamma$, so there
the effective gain $delta gamma = 1.8$ already exceeds one. Those four carry the
highest raw persistence in the scan ($Pi(399) = 0.585$ against $0.097$ at the $omega$
vertex), so plotting the scan without excluding them reads as a refutation of H2
while excluding them silently would confirm it for the wrong reason. Restricted to
the 41 sub-critical points the maximum sits exactly on the $omega$ vertex. The
variance decomposition agrees by a route sharing none of the same assumptions: the
$omega$-versus-$delta$ dial carries a total-order index of $0.993$ on persistence and
$1.004$ on handover time, against $0.032$ and $0.040$ for intensity.

That result carries one scope condition, the sharpest limit in the study. With the
noise constant as a fourth input, the split still carries $S_T = 1.002$ against
$0.022$ for noise over $zeta in [0, 0.02]$, but over $zeta in [0, 0.05]$ the ordering
*reverses* to $0.389$ against $0.750$: othering governs persistence only while
position noise stays below roughly twice its default, above which positions
random-walk back across the tolerance boundary and separated clusters re-merge. What
noise governs is therefore what *survives*, not when the transfer happens. The anchor
competes through the same channel: at $sigma = 0.05, 0.10, 0.20$ measured persistence
is 13, 9 and 4 steps against the $-1 slash ln(1 - sigma)$ prediction of 19.5, 9.5 and
4.5, and the floor disappears.

Two registered clauses need qualification. Low tolerance was predicted to bring the
handover forward; the direction holds but there is no gradient, since $Pi(149)$ runs
$0.320$ to $0.289$ across $epsilon <= 0.5$ and collapses to $0.045$ with no handover
at all for $epsilon >= 0.7$. Tolerance and depth are one gate seen from two sides,
$epsilon approx alpha_D (1 - bar(b))$. And the polarised regime, predicted to hand
over earlier with a smaller interaction, produces the largest $Pi(149)$ in the study
($0.566$) with the *smallest* interaction ($0.024$) and an othering-alone term of
$0.500$: almost all of its alarm is division that existed before anyone acted. An
already-divided population needs less entrepreneurship, but the cell is an attenuated
test rather than a clean one, which is what the consensual default exists to
avoid.

== Defence

#registered[
  H3, as registered, with both outcomes fixed in advance. A counter-entrepreneur acts
  through an immediate cost scaling with $rho_C$ and a delayed benefit scaling with
  $alpha_C$ that is not guaranteed in sign. *Branch 1:* broad-and-shallow lowers $Pi$
  while narrow-and-deep raises it, so defence works but only through reach.
  *Branch 2:* no configuration lowers $Pi$, so counter-claims-making is structurally
  self-defeating in this model.
]

Neither branch occurred. Every configuration raises $Pi$ above the undefended
baseline for its first 9 to 24 steps and lowers it permanently thereafter (@fig:h3).
Broad and shallow ($alpha_C = 0.15$, $rho_C = 0.60$) overshoots by $0.077$ for nine
steps and ends at $Pi(399) = 0.106$; narrow and deep ($0.90$, $0.10$) overshoots by
$0.239$ for 24 steps and ends at $0.020$; matched to $D$'s values ($0.70$, $0.25$)
overshoots by $0.135$ for eleven steps and ends at $0.045$, against an undefended
baseline of $0.179$. All three lower $Pi$ at the horizon, in 95 to 98 per cent of
seeds. The question has no single answer, because the answer changes sign at a step
that depends on the configuration: the endpoint says defence works, the transient
says it backfires, and both are true of the same run.

The ordering is the substance. The largest overshoot belongs to narrow and deep, the
configuration with the *lowest* reach and therefore the smallest immediate cost,
which rules out the first channel. What produces it is the second: pulling agents
toward $p_C$ narrows moral distance only if it moves them toward the population's
bulk, and at withdrawal the bulk sits at $bar(b) = +0.29$. Taking a tenth of the
population to $-1$ in a single step does the opposite, driving mean othering exposure
from $0.190$ to $0.309$ and $Pi$ to $0.467$, 61 per cent above what the panic would
have been had nobody answered back. The defence of the stigmatised position, mounted
intensively on a small base, is briefly the most panic-generating act in the study.
The gate is the one that governs ignition, operated from the other side:
$alpha_C = 0.15$ never exceeds tolerance and $bar(Phi)$ falls immediately, while
$alpha_C = 0.90$ severs ties on contact and cleaves the population again before
healing it.

#figure(
  image("../Results/figures/fig3_h3_defense.png", width: 100%),
  caption: [Defence. (a) $Pi$ through $C$'s entry for the four configurations;
    (b) each configuration minus the undefended baseline, with the crossings marked;
    (c) the $(bar(b), Pi)$ plane traced from withdrawal (star) to the horizon (dot);
    (d) residual $Pi(399)$ against each of $C$'s two levers one at a time, with the
    guide $Pi = 0.18 rho_C$. Mean over 250 seeds, 125 in panel (d).],
) <fig:h3>

The eventual reduction is conversion rather than reassurance. In all three
configurations $Pi$ falls because $bar(b)$ goes to $-0.99$ and mean othering exposure
collapses to $0.005$, the value of a population with nothing left to other. The
counter-entrepreneur does not calm anyone; it wins totally, and a population that
agrees about everything has no moral distance to be alarmed by. That is the only
route the specification leaves open, since no message in the model says *there is no
threat*.

What remains at the horizon is the price of speaking. Residual disproportion is
$approx 0.18 rho_C$, running $0.020$ to $0.185$ as $rho_C$ goes from $0.10$ to
$1.00$, and flat in depth at $0.087$ to $0.088$ across $alpha_C$. Every claims-maker
enters the alarm neighbourhood of everyone it reaches as a maximally alarmed contact,
and alarm is undirected, so once the population is converted that contact is all that
is left. A defence cannot lower the panic index below what its own broadcasting
costs, and the wide campaign of reassurance ends with five times the residual alarm
of the narrow one, not because it reassures worse but because it keeps talking to
more people.

== Robustness

The headline numbers are invariant to population size ($Pi(149) = 0.292$, $0.292$,
$0.293$ at $N = 500, 1000, 2000$, with only the across-seed dispersion moving, roughly
as $N^(-1 slash 2)$) and to the update scheme (random-order asynchronous updating
moves it by $0.010$, inside that dispersion). Replication on two public networks
@leskovecGraphEvolutionDensification2007 @mcauleyDiscoveringSocialCircles2014, each
accompanied by the three generators re-run at its own realised size and mean degree,
shows that the episode produced *while an entrepreneur is acting* is a property of
the parameters rather than of the graph: across eight rows spanning an eightfold range
of mean degree, $Pi(149)$ lies between $0.227$ and $0.270$. What structure decides is
what *survives*. At mean degree $43.7$ it decides nothing, all four rows landing at
$Pi(399) = 0.191$ to $0.198$; at mean degree $5.5$ it decides a factor of twenty, and
monotonically in clustering: $0.135$, $0.100$, $0.072$ and $0.006$ at clustering
coefficients of $0.530$, $0.439$, $0.268$ and $0.001$.

Two instrument checks bound the reading. The polarisation reported here is not
boundary pile-up: the interior bimodality coefficient, taken after dropping every
agent pinned at a pole, agrees with the raw one to three decimals, and a bound that
can never pin anyone leaves $Pi$ within $0.008$. And the counterfactual-validity
horizon --- where re-drawing the position noise moves one arm by more than a tenth of
the effect being resolved --- falls between $t = 191$ and $t = 289$ in three of five
audited seeds, so $Pi(399)$ is reported as a distribution over seeds, never as a
trajectory.


// ─────────────────────────────────────────────────────────────────────────────
= Discussion
// ─────────────────────────────────────────────────────────────────────────────

== What the apportionment settles

Whether panics are held up by elite claims-makers or by the reaction of the public
itself is an old division in the field @goodeMoralPanicsCulture1994
@garlandConceptMoralPanic2008 @mcrobbieRethinkingMoralPanic1995, argued rhetorically
because there was no way to apportion the two. The four-run design apportions them,
14 per cent to 2 per cent to 84 per cent.

Neither camp is right as usually stated. The entrepreneur is *necessary* --- at
$rho_D = 0$ nothing happens, and below the tolerance gate nothing happens either ---
and nearly irrelevant to the magnitude of what follows. Its achievement is not to
hold a population in a state of alarm but to divide it far enough that alarm becomes
self-sustaining, after which it is no longer required. This is also why panics are
hard to end: in this model the entrepreneur cannot end what it started, since the
only thing that returns $Pi$ to zero is $omega = 0$, a population that does not find
disagreement frightening. That is a different object of intervention from "stop the
campaign", and it names the quantity an empirical study would have to measure: not
the volume of claims-making but the distribution of moral distance across ties. The
mechanism has a cousin in the cascade literature, where public reaction outruns the
information that started it @kuranAvailabilityCascadesRisk1999; the difference is
that here what does the reinforcing is disagreement itself.

== Three predictions for empirical research

#h4[Ignition is about repetition, not reach] The mass broadcaster is, on this model,
structurally the *worst* available moral entrepreneur, since at full reach exposure
variance is zero, the interaction term collapses and panic incidence is zero under
every cut of the criterion. What makes a claims-maker dangerous is addressing some
people and not others, repeatedly, so the fragmentation of audiences is a mechanism
rather than a background condition. The prediction is uncomfortable for a common
intuition about mass media: Cohen's mass-press episodes @cohenFolkDevilsMoral1994 and
contemporary platform cases @walshSocialMediaMoral2020
@carlsonFakeNewsInformational2020 @walshSocialMediaMigration2023 would be doing
different things under one label, and the difference is measurable as the
concentration of exposure rather than its volume. One caution follows from the same
control: since most of what degree targeting achieves is achieved by a fixed audience
carrying no degree signal, `hub` is a weak proxy for algorithmic amplification.

#h4[Local density decides whether a panic outlives its campaign] Across two empirical
graphs and their matched generators, disproportion during the campaign barely notices
what graph it is running on, while what survives withdrawal is decided by structure
and, at low density, tracks clustering monotonically. Bounded confidence carves the
population into clusters, and a cluster holds only if its members reinforce each other
faster than noise walks them back across the tolerance boundary; triangles supply that
reinforcement. The comparative prediction is direct: two societies with identical
claims-making, tolerance and alarm parameters will differ in whether the panic
outlives the campaign, according to how clustered their social ties are. No synthetic
generator produced this.

#h4[Answering back intensifies the episode before it ends it] The organised defence of
a stigmatised position raises disproportion for its first 9 to 24 steps, and most when
it is most committed. The constructivist literature has long described defence and
resistance as part of what escalates an episode rather than as its remedy
@hierFolkDevilResistance2011 @mikhaylovaFolkDevilsMoral2022
@zielinskaPolarizingMoralPanics2022, and the model supplies a mechanism involving
neither tone nor provocation nor backlash psychology, none of which exist here. It is
arithmetic on moral distance: the defence's own converts become the population's most
distant neighbours, and distance is what alarms @ameryOtheringPeakingPopulism2025.

A methodological warning belongs beside these. Panic incidence in our runs jumps
where the underlying disproportion moves smoothly, so empirical episode counts, which
apply coding rules to continuous public reaction, may inherit their sharpness from
the rule rather than from the phenomenon @critcherMoralPanicAnalysis2008
@davidIdeaMoralPanic2011.

== What bounds the results

The hard ceiling is the meaning of $Pi$ itself. It measures alarm in excess of the
*model's own* counterfactual, not in excess of real danger. The paper formalises the
structure of the disproportionality criterion and makes it computable; it does not
make it decidable for any actual episode @hierRethinkingProblemDisproportion2024, and
no amount of further computation or better data moves that line.

Four exclusions bound the substance. Networks do not rewire, the most consequential
omission, since homophilous unfriending and deplatforming are among the
best-documented drivers of polarisation @flacheModelsSocialInfluence2017; it is also
why repulsion is excluded from the peer rule, because on a static graph active
repulsion and structural sorting cannot be told apart, so the model under-represents
divergence rather than mis-attributing it. There is no algorithm and no recommender.
No actor can reassure, since every claims-maker enters the alarm neighbourhood as a
maximally alarmed contact and no message says *there is no threat*, which makes the
finding that defence works only by conversion a property of the specification as much
as a result. And panic leaves no institutions: legacy is purely attitudinal, so the
model can show an episode outlasting its cause but not hardening into law.
Claims-makers also do not learn, which is why the counter-entrepreneur gets 250
uninterrupted steps that no real contest would grant --- the transient overshoot is
far more robust to this than the endpoint is.

Three scope conditions travel with the results. The persistence result requires
$sigma = 0$, since with any restoring force toward pre-campaign convictions
persistence tracks the anchor's relaxation time rather than othering, which is the
reverse of what H2 claims. It requires $zeta lt.approx 0.02$, since at five times the
default noise position drift out-explains the alarm split by roughly two to one, and
how noisy real moral positions are is an empirical question this model cannot settle.
And the decomposition is interpretable only from a consensual start, which matters for
any empirical extension: a measured initial distribution would put most real
populations into the attenuated case rather than the clean one.

One limitation is structural rather than parametric, and we state it because the
parameter count advertises more than the model has. Six parameters resolve, in the
runs, into roughly three live dimensions: the gate formed jointly by depth and
tolerance, reach as a non-monotone magnitude, and othering as what survives. Memory
carries a total-order index of $0.001$ on persistence, contagion matters mainly
through the sub-criticality condition, and threshold dispersion is a gain multiplier
that leaves shape and peak untouched. This is parsimony rather than a defect, but a
reader who expects six independent levers will be misled.

Nothing here is a test of the model against the world. Three things would make it one:
a network of *moral communication*, whose ties carry disagreement about a contested
issue rather than co-authorship or friendship
@mihaylovaVozmozhnostiPrimeneniyaEgosetevogo2021; measured initial positions on that
issue @mihaylovaIzmerenieMoralnoyPaniki2022; and an external threat referent, which
cannot be bought with better data at all.


// ─────────────────────────────────────────────────────────────────────────────
= Conclusion
// ─────────────────────────────────────────────────────────────────────────────

Moral panic research has a definitional criterion it cannot apply, because
disproportion requires a comparison with a world in which the claims-making did not
happen and that world is not observable. A simulation can run it, and running it
turns the oldest dispute in the field into an arithmetic question with an answer: 84
per cent of the alarm a campaign manufactures is not the campaign's signal but the
division it created, amplified by a population that finds its own divisions
frightening.

The three results that generalise beyond this parameterisation are negative in form,
which is what makes them useful. Claims-making that reaches everyone cannot produce a
panic, because manufactured division requires unequal exposure; claims-making too
shallow to be disowned cannot produce one either, because it persuades instead of
dividing; and answering back cannot lower alarm without first raising it, because the
only channel left open for lowering it is the elimination of disagreement. If moral
panics are becoming easier to start, the reason is not that reach has increased.

What remains uncomputed is the thing the concept was built around. $Pi$ is excess over
the model's own counterfactual, and no run of it can say that a real episode was out
of proportion to a real danger: the criterion is made computable here, not decidable.
Two extensions strike where the results are weakest --- an actor with a signed effect
on alarm, and a rewiring network, since every omission in the present design pushes
toward *under*-stating how far a population can come apart.


// ─────────────────────────────────────────────────────────────────────────────
// References
// ─────────────────────────────────────────────────────────────────────────────

#bibliography(
  ("../Moral Panic.bib", "../Computational Methods.bib"),
  style: "american-sociological-association.csl",
  title: "References",
)
