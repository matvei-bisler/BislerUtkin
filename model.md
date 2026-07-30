# An Agent-Based Model of Networked Moral Panic Escalation

> **Note on this specification.** The model is reported following the ODD protocol
> (Overview, Design concepts, Details; Grimm et al. 2006, 2010, 2020), the most
> widely used protocol for describing agent-based models, so that the model is
> reproducible from this document alone. Sections are ordered for readability
> rather than in strict ODD sequence; the crosswalk below maps each ODD element to
> its section. The dynamics combine three well-established model families —
> DeGroot/Friedkin–Johnsen opinion averaging with stubbornness,
> bounded-confidence interaction with repulsion (Hegselmann–Krause; Deffuant;
> Jager–Amblard; Flache et al.), and Granovetter-style threshold contagion with
> complex-contagion amplification (Centola–Macy) — and couples them to strategic
> external claims-makers in the sense of norm-entrepreneurship theory (Finnemore &
> Sikkink 1998), implemented in the tradition of normative agent-based systems
> (Hollander & Wu 2010). Each substantive mechanism is tied below to the
> moral-panic literature it operationalizes.

**ODD crosswalk.**

| ODD element | Section |
|---|---|
| Purpose and patterns | §1 |
| Entities, state variables, and scales | §2, §3, §4, §5 |
| Process overview and scheduling | §6 |
| Design concepts | §11 |
| Initialization | §8 |
| Input data | §9 |
| Submodels | §7 |
| *(supplementary: observation, experiments, artifacts, implementation)* | §10, §12–§15 |

**Notation conventions.** Subscript $i$ always indexes the focal agent, $j$ a
neighbor. Superscripts and subscripts $D$ and $C$ always label the two external
actors (§5) and never denote quantities. Time-varying quantities carry $(t)$;
fixed agent attributes and global parameters do not. Greek letters are global
parameters except $\tau_i,\sigma_i,\theta_i,\kappa_i,\Phi_i,\xi_i$, which are
agent-indexed.

---

## 1. Purpose and Patterns

### 1.1 Purpose

The model simulates the networked micro-dynamics of **moral panic escalation** in
heterogeneous social systems. It examines how strategic moral intervention,
perceived-threat exaggeration, peer conformity, "othering," threshold activation,
and network topology interact to produce polarization, clustering, persistence, or
containment of moralized social reactions.

The model does **not** claim to reproduce moral panic as a fully reducible
sociological phenomenon. It formalizes the *interactional mechanisms* and
*structural conditions* that increase or constrain the possibility of panic
escalation within networked communication environments. It is an analytical /
theoretical model addressed to the micro–macro gap in moral-panic research
(Mikhaylova 2021, 2022b): it shows how individual-level interaction generates
system-level escalation, the question discourse- and framing-analytic methods
cannot directly address.

The model runs in **discrete, synchronous time steps**. At each step $t \to t+1$,
every agent updates two internal states from the combination of: persistence of
prior states, local social influence (assimilative or repulsive), threat
contagion and othering, strategic external intervention, threshold activation, and
idiosyncratic noise.

### 1.2 Patterns used to judge model adequacy

Because the model is theoretical rather than calibrated, its adequacy is assessed
against **qualitative patterns** documented in the moral-panic and
opinion-dynamics literatures, not against point predictions. The model is
considered structurally adequate if, within a non-degenerate region of parameter
space, it reproduces all of the following simultaneously:

1. a **bimodal** rather than unimodal distribution of moral alignment (us/them
   structure; Cohen 1972; Goode & Ben-Yehuda 1994);
2. a **non-linear, cascade-shaped** rise in aggregate threat rather than smooth
   linear diffusion (Granovetter 1978; Centola & Macy 2007);
3. **community-localized** clusters of elevated threat rather than uniform
   system-wide alarm (Moran & Prochaska 2023; O'Brien 2023);
4. **slow decay** of aggregate threat after external claims-making ceases, i.e. a
   detectable legacy period (Goode & Ben-Yehuda 1994);
5. **containment** — escalation failing to spread — under at least some
   topologies and targeting strategies, so that escalation is not an artifact of
   the model always escalating.

Failure to reproduce (1)–(5) jointly indicates a structural rather than a
parametric problem. These are the patterns the sensitivity analysis (§12) is
organized around.

---

## 2. Entities, State Variables, and Scales

The model contains $N$ agents, a fixed social network, and two competing external
claims-makers.

Each agent carries **dynamic state variables** and a set of **fixed agent
attributes**.

### 2.1 Dynamic state variables

**Moral alignment** $\;b_i(t) \in [-1, 1]$

* $b_i = -1$: full alignment with the **counter-hegemonic** moral position;
* $b_i = +1$: full alignment with the **dominant** moral claim;
* intermediate values: partial alignment or neutrality.

**Threat perception** $\;\tau_i(t) \in [0, 1]$

* $\tau_i = 0$: no perceived threat;
* $\tau_i = 1$: maximal perceived social/moral danger.

> Threat perception is denoted $\tau$ (not $t$) to avoid collision with the time
> index. It operationalizes the perceived urgency, danger, hostility, and moral
> alarm that the literature identifies as the engine of panic — the "exaggerated
> threat" that claims-makers construct and amplify (Cohen 1972; Goode &
> Ben-Yehuda 1994; Amery & Mondon 2025). It is the central amplification
> mechanism of the model.
>
> Note that $\tau$ is **undirected**: it records how alarmed an agent is, not what
> the agent is alarmed about. The object of alarm is read off jointly with $b_i$
> (an alarmed agent at $b_i \approx +1$ fears the counter-hegemonic position; an
> alarmed agent at $b_i \approx -1$ fears dominant persecution). This is a
> deliberate simplification and constrains the interpretation of $E_i$ (§7.5).

### 2.2 Fixed agent attributes

| Symbol | Meaning | Domain |
|---|---|---|
| $c_i$ | conformity coefficient (responsiveness to neighbors) | $[0,1]$ |
| $\sigma_i$ | moral stubbornness (anchoring to initial conviction) | $[0,1]$ |
| $\theta_i$ | panic activation threshold | $[0,1]$ |
| $b_i(0)$ | initial moral conviction (retained as the stubbornness anchor) | $[-1,1]$ |

All are drawn from configurable distributions at initialization (§8) and held
constant during a run.

### 2.3 Derived quantities

| Symbol | Definition |
|---|---|
| $\mathcal N_i$ | network neighbors of agent $i$ |
| $d_i = \lvert \mathcal N_i \rvert$ | degree of agent $i$ |
| $\Delta_{ij}(t) = \lvert b_i(t)-b_j(t)\rvert \in [0,2]$ | moral distance between $i$ and $j$ |
| $a_i(t) = \mathbf 1[\tau_i(t) > \theta_i]$ | activation indicator (amplified regime) |
| $\kappa_i(t) = 1 + (\gamma-1)\,a_i(t)$ | activation weight ($=\gamma$ if active, else $1$) |
| $w_j(t) = \bigl(1+\beta\,\tau_j(t)\bigr)\,\kappa_j(t)$ | social weight of agent $j$ as a source of influence |

Note that $w_j$ is a property of the **source** agent $j$ alone, not of the dyad
$(i,j)$: an alarmed or activated agent is more influential on *all* of its
neighbors equally. The model contains no dyad-specific tie strength. (This is why
the weight is written $w_j$ rather than $w_{ij}$; the dyadic component of
influence enters separately through the sign $s_{ij}$ of §7.2.)

### 2.4 Scales

* **Temporal.** Time is discrete and dimensionless. One step represents one round
  of communicative exposure — the interval over which an agent encounters its
  neighbors' expressed positions and any claims-maker message. The model is not
  calibrated to clock time, so results are interpreted **ordinally** (faster/slower,
  earlier/later) and never as days or weeks. Runs use $T$ steps, with $T$ chosen
  long enough that the reported quantities are stationary or have demonstrably
  absorbed (checked per parameter cell, not assumed).
* **Spatial.** There is no metric space. The only notion of distance is
  **geodesic distance on $G$**; "local" means graph-adjacent. Network extent is
  $N$ nodes; resolution is the individual.
* **Population.** $N$ is a modeling choice, not an empirical target. Because
  several mechanisms (hub targeting, community localization) are degree- and
  size-dependent, all substantive findings are checked for finite-size effects
  across at least $N \in \{500, 1000, 2000\}$ (§12).

---

## 3. Parameters

| Symbol | Meaning | Typical domain |
|---|---|---|
| $N$ | number of agents | $\mathbb Z_{>0}$ |
| $T$ | number of time steps | $\mathbb Z_{>0}$ |
| $\beta$ | threat-driven amplification of social influence | $\ge 0$ |
| $\gamma$ | activation amplification multiplier | $>1$ |
| $\epsilon$ | confidence bound (moral distance below which influence is assimilative) | $[0,2]$ |
| $r$ | repulsion intensity beyond the confidence bound | $[0,1]$ |
| $\mu$ | threat persistence (memory) | $[0,1]$ |
| $\delta$ | weight on local threat contagion | $[0,1]$ |
| $\eta$ | weight on external panic signaling | $[0,1]$ |
| $\omega$ | weight on local disagreement ("othering" threat) | $[0,1]$ |
| $\zeta$ | s.d. of idiosyncratic belief noise | $\ge 0$ |
| $\alpha_{D},\alpha_{C}$ | per-contact influence intensity (depth) of each claims-maker | $[0,1]$ |
| $\lambda_{D},\lambda_{C}$ | institutional legitimacy → targeting-reach multiplier (breadth) | $\ge 0$ |
| $\rho$ | base targeting rate (fraction targeted per step) | $[0,1]$ |
| $\rho^{\text{eff}}_X=\min(1,\lambda_X\rho)$ | effective reach of actor $X$ | $[0,1]$ |

Subscripts $D$ and $C$ denote the **Dominant** and **Counter-hegemonic**
claims-makers (§5).

### 3.1 Range and stability conditions

Two conditions are exact and should be treated as constraints, not guidance.

**(C1) Threat stays in range without clipping.** Since $A_i,\Phi_i,E_i\in[0,1]$
and all four terms of the threat update (§7.5) are non-negative,

$$\mu+\delta+\omega+\eta \le 1 \;\Longrightarrow\; \tau_i(t)\in[0,1]\ \ \forall t,$$

by induction from $\tau_i(0)\in[0,1]$, so the $\mathrm{clip}_{[0,1]}$ in §7.5 is
inert. Violating (C1) does not break the model — clipping absorbs the excess —
but it makes the ceiling an active constraint and should be reported when it
occurs (fraction of agent-steps at $\tau=1$).

**(C2) Threat contagion is sub-critical.** In a homogeneous mean-field
approximation ($\tau_j \approx \bar\tau$, so $A_i \approx \bar\tau$), the threat
recursion linearizes to $\bar\tau(t+1) \approx (\mu+\delta)\bar\tau(t) +
\omega\bar\Phi + \eta\bar E$, with fixed point

$$\bar\tau^{*} = \frac{\omega\bar\Phi+\eta\bar E}{1-\mu-\delta},\qquad \mu+\delta<1 .$$

If $\mu+\delta \ge 1$, aggregate threat runs to the ceiling for *any* positive
input, and every parameter cell escalates trivially. **$\mu+\delta<1$ is
therefore the substantively meaningful constraint** — sharper than (C1) — and
$\bar\tau^{*}$ is the analytic benchmark against which the simulated aggregate is
verified in the no-activation limit ($\gamma=1$; §12.3).

**Belief range.** There is **no** analogous invariant for $b_i$. The
$\mathrm{clip}_{[-1,1]}$ in §7.4 is load-bearing: it binds whenever $r>0$, or
$\zeta>0$, or external intervention and social pull act in the same direction on
an already-extreme agent. Keeping $\alpha_X\le1$ guarantees only that the
intervention term *in isolation* is a convex combination of $b_i(t)$ and the
target pole and cannot overshoot. See §14.1.

---

## 4. Network Structure

Agents are embedded in a **static undirected graph** $G=(V,E)$. Topology is a
primary explanatory variable — it represents the decentralized infrastructures
through which contemporary networked panics propagate (Moran & Prochaska 2023;
O'Brien 2023). The generators are chosen to span the empirically documented
structural features of real communication networks, not merely mathematical
convenience.

Real social and online networks combine four robust "stylized facts": short path
lengths, **high clustering** (transitivity), **heavy-tailed degree
distributions** (hubs), and pronounced **community structure** (modular
echo-chambers) (Newman 2003, 2006; Barabási 2016). No single classical generator
reproduces all four, so the model uses a graded set.

**Realistic generators (used for the substantive results).**

* **Watts–Strogatz small-world** (Watts & Strogatz 1998) — short paths with
  tunable clustering; the canonical model of locally dense, globally connected
  social worlds.
* **Holme–Kim scale-free with tunable clustering** (Holme & Kim 2002) — preferred
  over plain Barabási–Albert because it reproduces hubs **and** the high
  clustering real networks display, which BA lacks. (Barabási–Albert (Barabási &
  Albert 1999) is retained only as a pure hub baseline; following Broido & Clauset
  (2019), we describe these as *heavy-tailed / hub-dominated* rather than strictly
  "scale-free," since exact power laws are empirically rarer than once assumed.
  This terminology is used consistently throughout, including in the hypotheses of
  §13.)
* **Stochastic block model with planted communities** (Holland, Laskey &
  Leinhardt 1983; Karrer & Newman 2011), optionally the LFR benchmark
  (Lancichinetti, Fortunato & Radicchi 2008) — the **most important addition for
  this model**, because it is the only family that natively generates the
  modular, community-segmented structure in which moral panics actually cluster.
  A mixing parameter $\nu\in[0,1]$ (the fraction of a node's ties that cross
  community boundaries) tunes echo-chamber strength: low $\nu$ = sealed
  communities, high $\nu$ = well-mixed. Community structure is not cosmetic here —
  complex contagions such as panic spread *more* effectively in clustered,
  community-rich networks than in random ones with long ties (Centola & Macy
  2007; Centola 2010), so $\nu$ is expected to be a first-order driver of
  escalation and clustering. Because the SBM plants a known partition, that
  partition is retained and used directly by the clustering metrics of §10.

**Theoretical baselines (null models, for comparison only).**

* **Erdős–Rényi random graph** — no clustering, no hubs, no communities; the
  structural null. (The $G(n,p)$ variant used here is due to Gilbert 1959;
  Erdős & Rényi 1959 introduced the $G(n,m)$ variant. The conventional label is
  retained.)
* **Cycle** and **complete** graphs — extreme low- and high-density references.

These baselines are reported as controls that isolate the effect of each
realistic feature, not as descriptions of empirical networks.

**Comparability across generators.** Topologies are compared at **matched mean
degree** $\bar d$, since otherwise a topology effect is confounded with a density
effect. Where a generator cannot hit a target $\bar d$ exactly, the realized
$\bar d$ is reported alongside the results.

**Isolates and disconnection.** Some generators (notably Erdős–Rényi at low $p$,
and the SBM at low within-block density) produce isolated nodes and multiple
components. The model runs on the **full generated graph, not the giant
component**, because isolation is a substantively meaningful condition (agents
reachable only by claims-makers). Isolated nodes ($d_i=0$) are handled explicitly
in every neighborhood operator (§7.2, §7.5): their social displacement, threat
contagion, and othering exposure are all defined to be zero, so an isolate's
threat relaxes to $\eta E_i/(1-\mu)$ and its belief to $b_i(0)$ in the absence of
targeting. The number of components and the isolate fraction are recorded per run.

**Empirical network (external validity).** Because synthetic graphs can only
approximate real structure, the principal findings are additionally replicated on
at least one **empirical network** — e.g. a platform ego-network or friendship
graph from a public repository (Leskovec & Krevl 2014, SNAP) — to confirm that
escalation patterns are not artifacts of a particular generator.

---

## 5. External Actors: Two Competing Claims-Makers

The model includes two strategic external actors who promote opposing moral
positions. This symmetric, **two-claims-maker** design is licensed by recent work
showing that the folk-devil / moral-entrepreneur distinction is a matter of
*position within a contest*, not a fixed ontological status: stigmatized actors
routinely act as entrepreneurs of their own counter-panic (Mikhaylova 2022b,
*Folk Devils or Moral Entrepreneurs?*), and resistance to dominant moral claims is
itself organized "antipreneurship" (Bloomfield & Scott 2018).

The actors are **not agents**: they have no internal state, occupy no position in
$G$, and do not update. They are exogenous forcing terms with a fixed pole and a
fixed strategy for the duration of a run (or until intervention ceases; §10, §14.2).

**Dominant claims-maker (D).** Promotes the dominant moral claim, pushing targeted
agents toward the pole $p_D = +1$ and injecting threat. Empirically this is the
elite/media/state moral entrepreneur of the literature (Becker 1963;
Flores-Yeffal & Elkins 2020; Conyers 2025; Shiran 2024). It is an analytically
simplified claims-making *position*, not an inherently "good" actor.

**Counter-hegemonic claims-maker (C).** Promotes the contested position, pushing
targeted agents toward the pole $p_C = -1$. It represents the organized defense of
the stigmatized position — the niche and micro-media through which "folk devils"
now answer back (McRobbie & Thornton 1995) — modeled as a counter-entrepreneur.

> The **folk devil as such is not an actor in the model**: it is the
> *stigmatized pole* ($b \approx -1$) around which threat, hostility, and
> clustering **emerge** from the dynamics (§7.5–7.6). This preserves the
> constructivist insight that folk devils are constituted through attribution
> while still giving the contest two strategic sides.

Each actor $X\in\{D,C\}$ has a **per-contact influence intensity** $\alpha_X$
(how hard each targeted agent is pushed) and an **institutional legitimacy**
$\lambda_X$ that scales its **reach** — the number of agents it can target per
step, $\rho^{\text{eff}}_X=\min(1,\lambda_X\rho)$ (§7.1). The two are deliberately
separated so that the *depth* and *breadth* of influence are independently
identifiable: a fringe actor may push hard but reach few ($\alpha$ high,
$\lambda$ low), whereas an institutionally legitimate actor reaches widely even at
modest per-contact intensity. Legitimacy thus operationalizes the diffusion-reach
advantage of established claims-makers; the *persistence* advantage the literature
attributes to legitimacy is carried endogenously by threat memory $\mu$ (§7.6),
not by a separate coefficient. (In the earlier formulation $\alpha$ and $\lambda$
entered only as the product $\alpha\lambda$ and were therefore not separately
identifiable; assigning them distinct roles removes that redundancy.)

---

## 6. Process Overview and Scheduling

Updates are **synchronous**: every quantity dated $t+1$ is computed from
quantities dated $t$ only. Because of this, the order of the steps below is
bookkeeping rather than substance — no step reads an output of a previous step
within the same tick. One step executes:

1. **Reset targeting** for both actors (targeting is re-decided each step and does
   not persist).
2. **Select targets** — each actor computes its indicator $g^X_i(t)\in\{0,1\}$
   from the **current-step** states $b_i(t)$ and the fixed degrees $d_i$ (§7.1).
3. **Compute social displacement** $S_i(t)$ — assimilative/repulsive (§7.2).
4. **Compute external interventions** $I^D_i(t), I^C_i(t)$ (§7.3).
5. **Update moral alignment** $b_i(t+1)$ (§7.4).
6. **Compute threat contagion $A_i(t)$, othering $\Phi_i(t)$, and signaling
   $E_i(t)$; update threat** $\tau_i(t+1)$ (§7.5).
7. **Record metrics** (§10).

Activation $a_i(t)$, weights $\kappa_i(t), w_i(t)$, distances $\Delta_{ij}(t)$,
and targeting indicators $g^X_i(t)$ are all evaluated once from the step-$t$ state
and used consistently in steps 2–6. In particular, $\Phi_i(t)$ in step 6 uses
$b(t)$, **not** the freshly computed $b(t+1)$.

Synchronous updating is a substantive choice, not a convenience: it makes the
dynamics deterministic given the noise draws, but it also admits period-2
oscillations under repulsion. This is examined in §14.3, where the principal cells
are replicated under asynchronous (random-order) updating.

---

## 7. Submodels

### 7.1 Targeting

Each actor $X$ targets a fraction $\rho^{\text{eff}}_X=\min(1,\lambda_X\rho)$ of
agents per step via an indicator $g^X_i(t)\in\{0,1\}$ — this is where legitimacy
enters, as reach. Write

$$n_X=\min\bigl(N,\;\lceil\rho^{\text{eff}}_X N\rceil\bigr)$$

for the number of agents actor $X$ targets. All strategies select exactly $n_X$
agents; `common` is the special case $\rho^{\text{eff}}_X = 1$ (i.e. $n_X = N$),
not a separate rule.

* `common` — broadcast: all agents ($g^X_i\equiv 1$);
* `random_target` — uniform random subset of size $n_X$, sampled without
  replacement, redrawn each step;
* `influencer_target` — the $n_X$ highest-degree nodes (operationalizes platform
  amplification / hub targeting);
* `close_target` — the $n_X$ agents minimizing $\lvert b_i(t)-p_X\rvert$
  (preaching to the choir);
* `distance_target` — the $n_X$ agents maximizing $\lvert b_i(t)-p_X\rvert$
  (conversion of opponents).

**Ties** in all ranked strategies are broken uniformly at random, re-drawn each
step; this matters for `influencer_target` on regular graphs (cycle, WS before
rewiring), where all degrees are equal and the strategy degenerates to
`random_target`.

**Temporal structure of the strategies differs and must not be conflated.**
Because degree is fixed, `influencer_target` selects the *same* set of agents at
every step (up to ties) — a sustained campaign on a fixed audience. `close_target`
and `distance_target` re-rank from $b(t)$ each step and therefore chase a moving
target, which can produce endogenous cycling in who is targeted. `random_target`
resamples independently. Any comparison across strategies is therefore also a
comparison across exposure schedules, and this is reported as part of the result
rather than treated as a nuisance.

The two actors target independently; an agent may be targeted by both, one, or
neither in a given step.

### 7.2 Social influence: assimilation and repulsion

Influence is **signed by moral distance**, the dyadic form of "othering":
agents move *toward* neighbors within their confidence bound and *away from*
neighbors beyond it.

$$
s_{ij}(t) =
\begin{cases}
+1, & \Delta_{ij}(t) \le \epsilon \quad\text{(assimilation)}\\
-\,r, & \Delta_{ij}(t) > \epsilon \quad\text{(repulsion)}
\end{cases}
$$

The net social displacement of agent $i$ is the weight-normalized signed pull of
its neighbors:

$$
S_i(t) =
\begin{cases}
\dfrac{\displaystyle\sum_{j\in\mathcal N_i} w_j(t)\,s_{ij}(t)\,\bigl(b_j(t)-b_i(t)\bigr)}
       {\displaystyle\sum_{j\in\mathcal N_i} w_j(t)}, & d_i>0,\\[2.4ex]
0, & d_i=0.
\end{cases}
$$

The denominator sums over **all** neighbors, assimilative and repulsive alike, so
an agent with a mix of near and far neighbors experiences partial cancellation
rather than the sum of two separate pulls. Threat-amplified and activated
neighbors (large $w_j$) dominate the pull, operationalizing recursive panic
amplification.

**Limiting cases (used for verification, §12.3).**

* $\epsilon = 2$: no pair can exceed the bound, so $s_{ij}\equiv+1$ and $r$ is
  inert; the rule becomes weighted assimilation. If additionally $\beta=0$ and
  $\gamma=1$, the weights are uniform and constant and $S_i$ reduces to the
  classical DeGroot neighbor-average displacement. With $\beta>0$ or $\gamma>1$ it
  is *state-dependent* averaging, which is no longer DeGroot in the strict sense.
* $r = 0$, $\epsilon < 2$: distant neighbors exert no influence at all; the rule
  is Hegselmann–Krause bounded confidence on the network.
* $r > 0$, $\epsilon < 2$: assimilation plus repulsion, which generates
  endogenous polarization and clustering rather than imposing them externally.

**A note on the repulsion form.** Because the repulsive term retains the factor
$(b_j - b_i)$, repulsion is *strongest for the most distant* neighbors. This
follows Jager & Amblard (2005) but is not the only option in the literature
(Flache et al. 2017 review fixed-magnitude and distance-decaying alternatives),
and it is the proximate cause of the boundary pile-up documented in §14.1. A
distance-decaying variant is examined as a robustness check.

### 7.3 External moral intervention

Targeted agents are pulled toward each claims-maker's pole, with strength
proportional to per-contact intensity and to the remaining distance from the pole
(a bounded zealot / external-field term):

$$
I^D_i(t) = \alpha_D\, g^D_i(t)\,\bigl(1-b_i(t)\bigr),
\qquad
I^C_i(t) = \alpha_C\, g^C_i(t)\,\bigl(1+b_i(t)\bigr).
$$

Both are non-negative **magnitudes**; direction is supplied by their signs in
§7.4, where $I^D$ enters positively (toward $p_D=+1$) and $I^C$ negatively (toward
$p_C=-1$). The distance factors mean that, acting alone, the intervention maps
$b_i \mapsto (1-\alpha_X)b_i + \alpha_X p_X$ — a convex combination for
$\alpha_X\in[0,1]$ — so a claims-maker can never push an agent past a pole and
stops moving an agent already at its pole. Acting together, the net map is still
affine with range contained in $[-1,1]$ for $\alpha_D,\alpha_C\in[0,1]$. This
guarantee does **not** survive addition of the social and noise terms (§3.1).

### 7.4 Moral alignment update

$$
b_i(t+1) = \mathrm{clip}_{[-1,1]}\!\Bigl[
\underbrace{\sigma_i\,b_i(0)}_{\text{conviction anchor}}
+ (1-\sigma_i)\bigl(\underbrace{b_i(t)}_{\text{persistence}}
+ \underbrace{c_i\,S_i(t)}_{\text{social influence}}\bigr)
+ \underbrace{I^D_i(t) - I^C_i(t)}_{\text{external intervention}}
+ \underbrace{\xi_i(t)}_{\text{noise}}
\Bigr],
$$

with idiosyncratic noise $\xi_i(t)\overset{\text{iid}}{\sim}
\mathrm{Normal}(0,\zeta^2)$ drawn independently for each agent and step. (The
symbol $\mathcal N$ is reserved for neighborhoods; the Normal distribution is
written out.) The stubbornness term $\sigma_i b_i(0)$ is the Friedkin–Johnsen
anchor representing durable moral conviction. Setting $\sigma_i=\zeta=0$,
$\epsilon=2$, $\beta=0$, $\gamma=1$ recovers a pure DeGroot-plus-zealot model, in
which $c_i$ plays the role of the agent's self-weight ($1-c_i$).

**Scope of stubbornness — a deliberate asymmetry.** The intervention term sits
*outside* the $(1-\sigma_i)$ factor. Stubbornness therefore attenuates **peer**
influence but not **claims-maker** influence: a maximally stubborn agent
($\sigma_i=1$) is immune to its neighbors yet fully responsive to targeting. This
is intentional — $\sigma_i$ is defined here as resistance to *conformity
pressure*, which is the quantity the moral-panic literature treats as varying
across individuals — but it is a strong assumption, and it departs from the
standard Friedkin–Johnsen form, in which exogenous forcing enters inside the
susceptibility factor. Because $\sigma_i$ is one of the model's headline
parameters, the alternative specification (intervention scaled by $(1-\sigma_i)$
as well) is run as a robustness check and reported alongside; see §14.5.

**Noise asymmetry.** Noise is added to $b$ but not to $\tau$. Belief noise
represents idiosyncratic exposure outside the modeled network; threat is treated
as fully determined by the modeled channels. This keeps the threat dynamics
analytically tractable (§3.1, C2) at the cost of making $\bar\tau$ smoother than
$\bar b$, which must be kept in mind when reading the volatility metric (§10).

### 7.5 Threat perception update

**Local threat contagion** (activation-weighted, normalized):

$$
A_i(t) =
\begin{cases}
\dfrac{\displaystyle\sum_{j\in\mathcal N_i}\kappa_j(t)\,\tau_j(t)}
       {\displaystyle\sum_{j\in\mathcal N_i}\kappa_j(t)}, & d_i>0,\\[2.2ex]
0, & d_i=0,
\end{cases}
\qquad A_i(t)\in[0,1].
$$

Activated neighbors ($\kappa_j=\gamma$) contribute disproportionately, producing
cascades and tipping points (complex contagion). Note that because $A_i$ is a
*normalized* average, $A_i \le \max_j \tau_j$: activation redistributes influence
among neighbors rather than inflating the total, so the tipping behavior comes
from *which* neighbors count, not from an unbounded gain. This is what makes
condition (C2) of §3.1 the correct stability criterion.

**Local disagreement / othering exposure** — perceived threat rises with exposure
to the morally distant, the mechanism by which a threat is "constructed,
homogenised and exaggerated… in the bodies of the Other" (Amery & Mondon 2025):

$$
\Phi_i(t) =
\begin{cases}
\dfrac{\displaystyle\sum_{j\in\mathcal N_i} w_j(t)\,\Delta_{ij}(t)/2}
       {\displaystyle\sum_{j\in\mathcal N_i} w_j(t)}, & d_i>0,\\[2.2ex]
0, & d_i=0,
\end{cases}
\qquad \Phi_i(t)\in[0,1].
$$

The division by 2 rescales $\Delta_{ij}\in[0,2]$ onto $[0,1]$ so that $\Phi_i$ is
commensurate with $A_i$ and $E_i$ and the coefficients $\delta,\omega,\eta$ are
directly comparable in magnitude. Weighting by $w_j$ means the disagreement of an
*alarmed* neighbor is more threatening than the same disagreement from a calm one.

**External panic signaling** — *both* claims-makers raise alarm about the
opposing position (a dominant panic and an answering counter-panic; McRobbie &
Thornton 1995; Mikhaylova 2022b). Because $\tau$ is an undirected level of
perceived danger (§2.1), the two signals are additive:

$$
E_i(t) = \mathrm{clip}_{[0,1]}\!\bigl[\alpha_D\, g^D_i(t) + \alpha_C\, g^C_i(t)\bigr].
$$

Two assumptions are embedded here and should be stated rather than left implicit.
(i) The **signaling intensity is set equal to the persuasive intensity** $\alpha_X$
rather than given its own coefficient. This is a parsimony choice — the model
already carries a dozen free parameters (§14.4) — and it encodes the claim that a
claims-maker's capacity to alarm and its capacity to persuade scale together.
Decoupling them (a separate $\alpha^\tau_X$) is the natural first extension if the
sensitivity analysis shows $\eta$ to be influential. (ii) Because $E_i$ does not
depend on $b_i$, an agent is alarmed by a message regardless of whether it agrees
with it. Under the undirected reading of $\tau$ this is coherent — both messages
assert that something dangerous is happening — but it means the model cannot
represent an agent being *reassured* by an aligned claims-maker.

**Threat update:**

$$
\tau_i(t+1) = \mathrm{clip}_{[0,1]}\!\Bigl[
\underbrace{\mu\,\tau_i(t)}_{\text{persistence}}
+ \underbrace{\delta\,A_i(t)}_{\text{contagion}}
+ \underbrace{\omega\,\Phi_i(t)}_{\text{othering}}
+ \underbrace{\eta\,E_i(t)}_{\text{external signaling}}
\Bigr].
$$

This couples the two state variables in both directions: threat amplifies social
influence (via $w_j$), while moral disagreement feeds threat (via $\Phi_i$) —
the self-reinforcing loop at the heart of escalation.

### 7.6 Threshold activation and threat persistence

An agent is **activated** when $\tau_i(t)>\theta_i$ (strict inequality; an agent
with $\theta_i=0$ is activated by any positive threat). Activation feeds back into
both $S_i$ (§7.2) and $A_i$ (§7.5) through $\kappa_i$, so activated agents exert
stronger influence and accelerate local escalation.

The persistence parameter $\mu$ governs how slowly threat decays after external
signaling stops. With $\omega=0$ and an isolated or quiescent neighborhood, threat
decays geometrically with rate $\mu$, giving a characteristic legacy time of
$-1/\ln\mu$ steps — the durable "informal and institutional legacy" of panics
noted by Goode & Ben-Yehuda (1994).

**On "hysteresis."** Slow decay is *persistence*, not hysteresis in the
dynamical-systems sense. Genuine hysteresis requires bistability — two coexisting
attractors at the same parameter values, so that the system's state depends on the
path taken. The threshold $\theta_i$ combined with the activation multiplier
$\gamma$ makes bistability *plausible*, but it is a hypothesis to be tested, not a
property to be asserted. The test is a **hysteresis-loop sweep** (§12.2): ramp a
forcing parameter (e.g. $\alpha_D$ or $\rho$) slowly up and then slowly back down,
and check whether the ascending and descending branches of $\bar\tau$ coincide.
Only a non-overlapping loop licenses the word "hysteresis" in reporting results.

---

## 8. Initialization

For each run:

1. Build the network $G$ for the chosen topology and size $N$; record realized
   $\bar d$, clustering coefficient, number of components, and isolate fraction.
2. Draw initial moral alignment $b_i(0)$; store it as the stubbornness anchor.
3. Draw initial threat $\tau_i(0)$.
4. Draw conformity $c_i$, stubbornness $\sigma_i$, and threshold $\theta_i$.
5. Set claims-maker parameters $\alpha_X,\lambda_X,\rho$, strategies, and the
   global parameters $\beta,\gamma,\epsilon,r,\mu,\delta,\eta,\omega,\zeta$.

**Default initial distributions.** These are the documented defaults; alternatives
are treated as experimental factors (§12), not as free choices made per run.

| Quantity | Default | Alternatives (as factors) |
|---|---|---|
| $b_i(0)$ | $\mathrm{Uniform}[-1,1]$ | seeded bipolar: $\pm$ mixture; seeded consensual: $\mathrm{Uniform}[-0.2,0.2]$ |
| $\tau_i(0)$ | $\mathrm{Uniform}[0,0.1]$ (low baseline) | seeded alarmed minority: $\tau=0.9$ for a random or community-localized 5% |
| $c_i$ | $\mathrm{Uniform}[0,1]$ | $\mathrm{Beta}(a,b)$ for skewed conformity |
| $\sigma_i$ | $\mathrm{Beta}(2,5)$ (most agents weakly anchored) | $\mathrm{Uniform}[0,1]$; constant |
| $\theta_i$ | $\mathrm{Uniform}[0,1]$ | $\mathrm{Beta}$ for skewed susceptibility; constant $\theta$ |

**Do not initialize $b_i(0)$ by clipping a normal draw.** A clipped
$\mathrm{Normal}(0,1)$ on $[-1,1]$ places roughly a third of the mass exactly at
$\pm 1$ as two point atoms. Those atoms are indistinguishable from the boundary
pile-up the dynamics themselves produce (§14.1), so a clipped-normal
initialization pre-loads the polarization metric with the very artifact the
robustness check is meant to detect. Use a truncated normal, a rescaled Beta, or
the uniform default instead.

**Randomization.** All stochastic choices draw from a single seeded generator, and
the seed is recorded with the run. Seeds are reused as **common random numbers**
across parameter cells — the same seed produces the same network and the same
initial draws — so that differences between cells are attributable to the
parameters rather than to sampling variation. Where a factor changes the network
generator itself, common random numbers apply only to the agent-attribute draws.

---

## 9. Input Data

The model uses **no external input data** in the ODD sense: no empirical time
series, no exogenous driving variables, and no calibrated parameter values. All
parameters are set by design (§8) and explored by sweep (§12).

The single exception is the **empirical network** used for the external-validity
replication (§4): an edge list from a public repository (Leskovec & Krevl 2014).
It enters as fixed structure only — node attributes, if any, are discarded and
agent states are initialized exactly as in §8. The specific graph, its source, its
retrieval date, and its summary statistics ($N$, $\bar d$, clustering, modularity,
number of components) are reported with the results.

---

## 10. Output Metrics

Recorded each step. Note that the activated fraction is written $\bar a(t)$;
the symbol $A$ with a subscript is reserved for the *local* threat contagion term
$A_i(t)$ of §7.5 and denotes a different quantity.

1. **Mean moral alignment** $\bar b(t)=\frac1N\sum_i b_i(t)$.
2. **Mean threat** $\bar\tau(t)=\frac1N\sum_i\tau_i(t)$ — primary panic-intensity
   indicator.
3. **Activated fraction** $\bar a(t)=\frac1N\sum_i a_i(t)$.
4. **Polarization** of $\{b_i(t)\}$, reported as three non-redundant quantities:
   * **variance** $\mathrm{Var}(b)$ — dispersion;
   * **Sarle's bimodality coefficient**
     $\mathrm{BC}=\dfrac{g_1^{2}+1}{g_2+\dfrac{3(n-1)^2}{(n-2)(n-3)}}$, with $g_1$
     the sample skewness and $g_2$ the excess kurtosis; $\mathrm{BC}>5/9$ (the
     uniform-distribution value) is the conventional bimodality flag;
   * **number of opinion clusters** — count of groups after single-linkage
     clustering of $\{b_i\}$ at tolerance $\epsilon$, the standard summary in the
     bounded-confidence literature and the least clipping-sensitive of the three.

   (The earlier formulation listed "variance, a bimodality coefficient, and
   dispersion"; variance *is* the dispersion measure, so the third slot is
   replaced by the cluster count, which carries independent information.)
5. **Cascade speed** — $\max_t\bigl[\bar\tau(t+1)-\bar\tau(t)\bigr]$ and the
   corresponding quantity for $\bar a$. Because a step-to-step maximum is highly
   sensitive to noise and to single-agent threshold crossings, it is computed on a
   centered moving average (window 5) and reported alongside a smoothing-free
   alternative, the **time to half of peak $\bar\tau$**.
6. **Clustering of threat.** "Modularity over high-$\tau$ agents" is not
   well defined — modularity is a property of a partition, not of a node subset —
   so three precise quantities are used instead:
   * **threat assortativity** $r_\tau$ — Newman's scalar assortativity
     coefficient, i.e. the Pearson correlation of $\tau$ across the two endpoints
     of each edge; positive values mean alarmed agents are adjacent to alarmed
     agents;
   * **activated-subgraph structure** — the size of the largest connected
     component of the subgraph induced on $\{i : a_i(t)=1\}$, and the number of
     such components, normalized by the number of activated agents;
   * **between-community share of threat variance** (SBM/LFR only, where a
     partition is planted and therefore known): the intraclass correlation
     $\mathrm{Var}_{\text{between}}(\tau)/\mathrm{Var}_{\text{total}}(\tau)$,
     which is the well-defined version of "panic localizes in communities."
     Modularity $Q$ is reported only for the *planted* partition, never inferred
     from the threat field itself.

   **Local homophily** is defined explicitly as
   $H(t)=\frac{1}{|E|}\sum_{(i,j)\in E}\bigl(1-\Delta_{ij}(t)/2\bigr)\in[0,1]$.
7. **Persistence** — with intervention switched off at a designated step $t_{\text{off}}$
   ($\alpha_D=\alpha_C=0$ thereafter), the number of steps until $\bar\tau$ first
   falls below $\bar\tau(t_{\text{off}})/2$, censored at $T$. Runs in which
   $\bar\tau$ never falls below the threshold are reported as censored rather than
   assigned $T$, since averaging censored durations understates persistence. See
   §14.2 for the confound with othering.
8. **Volatility** — temporal s.d. of $\bar\tau(t)$ over the post-transient window,
   with the transient window length stated per parameter cell.

**Panic-detection criterion.** An episode is *escalated* if $\bar a(t)\ge \bar a^{*}$
for at least $W$ consecutive steps (e.g. $\bar a^{*}=0.5$, $W=10$). Both thresholds
are conventions, not findings; results are reported for a small grid of
$(\bar a^{*},W)$ so that conclusions can be seen not to depend on the particular
cut. Because the dynamics are stochastic, escalation is reported as a **frequency
over seeds** for each parameter cell, together with onset time, peak $\bar a$, and
post-intervention decay time.

---

## 11. Design Concepts

The eleven ODD design concepts are addressed in order; those not represented are
listed explicitly rather than omitted, since a reader cannot otherwise distinguish
"absent by design" from "overlooked."

* **Basic principles.** Belief = persistence + bounded-confidence social influence
  with repulsion + Friedkin–Johnsen conviction anchor + zealot forcing; threat =
  threshold contagion + othering + external signaling. Each maps to a documented
  moral-panic mechanism (elite claims-making, threat exaggeration, othering,
  legacy).
* **Emergence.** Polarization, clustering, cascades, and the stigmatized "folk
  devil" pole are emergent, not imposed. The activated fraction and the community
  localization of threat are the primary emergent outcomes. What is *not* emergent
  and is imposed: the network, the two poles, and the claims-makers' strategies.
* **Adaptation.** Agents have **no adaptive traits and no decision rules**. They
  respond to their environment through fixed, involuntary update equations — what
  ODD classifies as *indirect* response rather than adaptive behavior. Strategic
  agency in the model resides entirely in the two claims-makers' targeting, and
  even that is fixed for the duration of a run. This is the deliberate division of
  labor by which the model addresses the micro–macro gap (Mikhaylova 2021, 2022b):
  macro escalation is generated by non-strategic micro-response to strategic
  macro-input.
* **Objectives.** Not represented. Agents maximize nothing and evaluate no
  objective function; there is no utility, fitness, or payoff in the model.
* **Learning.** Not represented. No agent attribute changes as a function of
  experience: $c_i,\sigma_i,\theta_i$ are fixed for the entire run, and the
  claims-makers do not update their strategies in response to outcomes. Adaptive
  claims-makers are the most obvious extension of the model and are noted as such.
* **Prediction.** Not represented. Agents are entirely backward- and
  present-looking; no agent anticipates future states or the consequences of its
  own update.
* **Sensing.** Agents observe, without error, noise, or lag: their neighbors'
  moral alignment $b_j(t)$ and threat perception $\tau_j(t)$, and — implicitly,
  through $\kappa_j$ — whether each neighbor is activated. This is a strong and
  substantive assumption: it means **alarm is publicly legible**, which is what
  makes complex contagion possible at all. Agents do *not* observe any global
  quantity ($\bar b$, $\bar\tau$, $\bar a$), any non-neighbor, any neighbor's fixed
  attributes ($c_j,\sigma_j,\theta_j$), or which claims-maker (if any) targeted a
  neighbor. Claims-makers, by contrast, observe global state: `close_target` and
  `distance_target` require the full belief vector, and `influencer_target` the
  full degree sequence. This asymmetry — locally-sighted agents, globally-sighted
  claims-makers — is the model's formal representation of the informational
  advantage of organized claims-making.
* **Interaction.** Local and undirected among agents (via $\mathcal N_i$, for
  $S_i, A_i, \Phi_i$); global and unidirectional from the claims-makers to
  targeted agents. Agents do not interact with the claims-makers in return, and
  the claims-makers do not interact with each other.
* **Stochasticity.** Four sources: (i) network generation; (ii) initial attribute
  and state draws (§8); (iii) `random_target` selection and tie-breaking in the
  ranked strategies (§7.1); (iv) per-step belief noise $\xi_i$ (§7.4). Escalation
  is therefore probabilistic and is reported as a rate over seeds, never from a
  single run.
* **Collectives.** In the SBM/LFR topologies, communities are **imposed**
  collectives: they are planted at initialization, are fixed, and are known to the
  analyst but not to the agents. Agents have no group membership variable and no
  in-group/out-group rule; all apparent group behavior operates through
  $\Delta_{ij}$ and network position alone. The clusters that appear in the belief
  distribution are **emergent** collectives and are distinct from the planted ones;
  §10.6 keeps the two separate by construction.
* **Observation.** The §10 metrics, recorded every step. Full state vectors
  $\{b_i(t)\},\{\tau_i(t)\}$ are
  retained for a subset of runs to permit post-hoc analysis not anticipated here.
  Per-run structural statistics (§8, step 1) and the seed are stored with them.

**Why these functional forms.** The choices are not arbitrary; each is the
simplest form in an established lineage that reproduces a documented feature of
moral panic. (i) A *hard* confidence bound $\epsilon$ (Hegselmann & Krause 2002;
Deffuant et al. 2000) rather than a smooth influence kernel encodes the
categorical quality of moral judgement — a position is "within the pale" or not —
and yields interpretable cluster boundaries; a smooth alternative is examined as a
robustness check (§14). (ii) *Repulsion* beyond the bound (Jager & Amblard 2005;
Flache et al. 2017) is included because assimilation-only models converge to
consensus and cannot generate the bimodal "us/them" structure central to moral
panic; repulsion supplies the social-identity divergence the othering literature
documents (Amery & Mondon 2025). (iii) A *Friedkin–Johnsen conviction anchor*
(Friedkin & Johnsen 1990) rather than plain DeGroot averaging (DeGroot 1974)
encodes the identity-laden stickiness of moral conviction and prevents the trivial
consensus that DeGroot produces on any connected, aperiodic graph. (The
aperiodicity qualifier matters: DeGroot averaging on a connected *bipartite* graph
without self-weight does not converge but oscillates. Here $c_i<1$ supplies a
self-weight, so the model's assimilation-only limit is genuinely
consensus-forming and the anchor is doing real work.) (iv) *Threshold / complex
contagion* for threat (Granovetter 1978; Centola & Macy 2007) — via the activation
multiplier $\gamma$ — reflects that panic spreads only with reinforcement from
multiple alarmed contacts, unlike simple linear diffusion. (v) The *othering*
coupling $\omega\Phi_i$ is the simplest monotone map from local disagreement to
threat; nonlinear variants are left to sensitivity analysis (§12).

---

## 12. Experimental Design

Results come from systematic exploration, not point estimates.

### 12.1 Factors and replication

* **Factors:** topology (incl. community mixing $\nu$ for the block model, at
  matched mean degree) × targeting strategy × $(\rho,\lambda)$ × initial
  conformity and stubbornness distributions ×
  $(\beta,\gamma,\epsilon,r,\mu,\delta,\omega,\eta)$, with the principal cells
  replicated on an empirical network (§9).
* **Finite-size check:** principal cells re-run at $N\in\{500,1000,2000\}$ to
  establish that conclusions are not size-dependent (§2.4).
* **Replication:** the number of seeds per cell is set from a pilot — enough that
  the Monte Carlo standard error of the escalation frequency is below a stated
  tolerance (e.g. $\pm0.03$, which needs on the order of 250–300 seeds for a
  frequency near 0.5) — not fixed by convention. Report distributions and
  escalation frequencies with their uncertainty; never single runs.

### 12.2 Dedicated protocols

* **Intervention-cessation protocol.** For the persistence metric (§10.7), each
  run has a designated $t_{\text{off}}$ at which both $\alpha_X$ are set to zero,
  chosen after the escalation transient has resolved.
* **Hysteresis-loop protocol.** For the bistability claim (§7.6), ramp $\alpha_D$
  (or $\rho$) upward in small increments to a maximum and back down over a single
  long run, holding each level long enough to relax, and compare ascending and
  descending branches of $\bar\tau$ and $\bar a$.

### 12.3 Verification (before validation)

Model *verification* — that the code implements this specification — is reported
separately from any substantive result, via limiting-case docking against models
with known behavior:

1. $\sigma_i=\zeta=0,\ \epsilon=2,\ \beta=0,\ \gamma=1,\ \alpha_X=0$ → DeGroot;
   beliefs must converge to a single consensus value on any connected graph.
2. $\sigma_i>0$, otherwise as above → Friedkin–Johnsen; beliefs must converge to
   the known FJ equilibrium $b^{*}=(I-(I-\Sigma)W)^{-1}\Sigma\,b(0)$.
3. $r=0,\ \epsilon<2$, no threat coupling ($\beta=0,\gamma=1,\delta=\omega=\eta=0$)
   → Hegselmann–Krause; the number of surviving opinion clusters must follow the
   known $\epsilon$-dependence.
4. $\gamma=1$, homogeneous parameters → the mean-field fixed point $\bar\tau^{*}$
   of §3.1 (C2) must be recovered to within Monte Carlo error.
5. $\alpha_X=\zeta=0$, $d_i=0$ for all $i$ (empty graph) → each agent must relax
   to $b_i(0)$ and $\tau_i\to0$.

### 12.4 Sensitivity analysis

One-factor-at-a-time variation is used for intuition only, since it cannot detect
interactions and the model is expected to be strongly interactive. The reported
sensitivity analysis is global and two-stage:

1. **Morris elementary-effects screening** over all continuous parameters, to
   partition them into influential and non-influential sets at low cost;
2. **Variance-based Sobol indices** (first-order and total-order, estimated with
   Saltelli sampling) on the reduced influential set, reported per outcome metric.

Latin-hypercube sampling is a design for generating the input sample, not a
sensitivity method in itself, and is used where a space-filling design is needed
for a surrogate rather than as a substitute for Sobol estimation.

---

## 13. Research Logic and Expected Outcomes

The model examines how strategic moral intervention, institutional legitimacy,
network topology, conformity, stubbornness, amplification, othering, and threshold
activation jointly determine whether panic escalation emerges, stabilizes,
fragments, or dissipates. It is a formalized analytical framework, not a
predictive representation of specific panics.

Candidate hypotheses the design can probe — stated as conjectures to be tested,
not as anticipated findings:

* hub-dominated (heavy-tailed) networks produce influencer-driven escalation under
  `influencer_target`, and are correspondingly fragile to it;
* small-world networks accelerate panic contagion relative to lattices at matched
  mean degree;
* strong community structure (low mixing $\nu$) localizes panic into persistent
  echo-chambers and raises polarization, while high $\nu$ favors either
  system-wide escalation or dilution;
* dense networks stabilize moral consensus when $r$ is low, but **amplify
  polarization** when repulsion $r$ is high;
* sparse networks generate fragmented, localized panics;
* high conformity raises cascade probability, while high stubbornness sustains
  polarization;
* strong othering ($\omega$) converts mere disagreement into self-reinforcing
  threat;
* institutional legitimacy ($\lambda$) asymmetrically amplifies escalation, with
  reach mattering more than per-contact depth above some $\rho$;
* high persistence ($\mu$) locks in durable moralized threat environments, and —
  if the §12.2 loop protocol finds a non-overlapping branch — genuine bistability.

---

## 14. Known Artifacts and Robustness Checks

Five properties of the dynamics require guarded interpretation and a corresponding
robustness check; reporting them is a precondition for treating the output metrics
as evidence.

1. **Boundary pile-up from clipping (polarization metric).** Beliefs are driven
   past $\pm 1$ by three distinct routes, not one: repulsive displacement
   ($r>0$); belief noise ($\zeta>0$) acting on already-extreme agents; and
   external intervention acting in the same direction as a strong social pull.
   Clipping then accumulates mass exactly at the poles, so bimodality and variance
   may partly reflect a clipping artifact rather than genuine opinion structure.
   Mitigation: report the *interior* bimodality coefficient (excluding the boundary
   atoms) and the cluster count (§10.4) alongside the raw measures; record the
   fraction of agent-steps at which clipping actually binds, separately by route;
   and replicate key parameter cells with a soft bound (a $\tanh$ squashing in
   place of hard clipping). Conclusions should be invariant across both. Note also
   that a clipped-normal *initialization* would create the same atoms at $t=0$ and
   is excluded for that reason (§8).

2. **Persistence–othering confound.** With $\omega>0$, agents on a cluster
   boundary retain permanent disagreement $\Phi_i>0$, so collective threat need
   never decay to baseline even after both actors withdraw; the fixed point of
   §3.1 (C2) is then $\omega\bar\Phi/(1-\mu-\delta)>0$ rather than zero. The §10.7
   persistence metric therefore conflates threat memory ($\mu$) with sustained
   othering. Mitigation: estimate post-intervention persistence on companion runs
   with $\omega=0$, and report the memory-driven and disagreement-driven components
   separately rather than as a single duration; the analytic fixed point gives the
   expected floor against which the simulated residual is checked.

3. **Oscillation under synchronous repulsion.** Two mutually repelling neighbors
   can flip-flop under synchronous updating, producing 2-cycles that masquerade as
   volatility or cascades. Mitigation: screen the belief series for short limit
   cycles (autocorrelation at lag 2 and direct period detection), and replicate the
   principal cells under asynchronous (random-order) updating to confirm that
   escalation results are not update-scheme artifacts.

4. **Parameter dimensionality.** The model carries roughly a dozen free
   parameters, and a full factorial sweep is neither feasible nor informative.
   Mitigation: identify the influential parameters by the two-stage global
   sensitivity analysis of §12.4, fix the non-influential ones at documented
   defaults, and report results over the reduced influential set. This keeps the
   explanatory claims attributable to a small number of mechanisms. The reduction
   itself is reported, since which parameters turn out not to matter is a result.

5. **Asymmetric scope of stubbornness.** As noted in §7.4, $\sigma_i$ attenuates
   peer influence but not claims-maker influence, which departs from the standard
   Friedkin–Johnsen treatment of exogenous forcing. Under the present
   specification, a highly stubborn population is *more* susceptible to
   claims-making relative to peer influence, which could by itself generate the
   result that stubbornness sustains polarization (§13). Mitigation: replicate the
   principal cells with the intervention term scaled by $(1-\sigma_i)$, and report
   any hypothesis whose sign depends on the choice as specification-dependent.

---

## 15. Implementation and Reproducibility

* **Software.** Python; `networkx` for graph generation and structural metrics,
  `numpy` for the vectorized state update, `SALib` for Morris and Sobol analysis.
  Exact versions are pinned in an environment file distributed with the code.
* **Random number generation.** A single `numpy.random.Generator` (PCG64) per run,
  seeded from an explicitly recorded integer; no reliance on global RNG state.
* **Determinism.** Given the seed, the topology, and the parameter vector, a run is
  exactly reproducible. Any use of parallelism draws independent substreams via
  `SeedSequence.spawn` rather than reseeding, so results are invariant to the
  number of workers.
* **Outputs.** Per-step metric time series, per-run structural statistics and seed,
  and full state vectors for a retained subset (§11, Observation), written in a
  documented tabular schema.
* **Availability.** Code, environment file, seed lists, and the empirical edge list
  (or its retrieval script) are archived so that every figure in the paper can be
  regenerated from this specification and the deposit alone.

---

## Appendix A. Citation and bibliography notes

Two housekeeping items affect reproducibility of the write-up rather than the
model, and are recorded here so they are not lost.

1. **Methods citations are absent from the project bibliography.** Neither
   `Moral Panic.bib` nor `Text/references.bib` currently contains entries for
   Grimm et al., DeGroot, Friedkin & Johnsen, Hegselmann & Krause, Deffuant et al.,
   Jager & Amblard, Flache et al., Granovetter, Centola & Macy, Centola, Watts &
   Strogatz, Barabási & Albert, Holme & Kim, Holland/Laskey/Leinhardt, Karrer &
   Newman, Lancichinetti et al., Erdős & Rényi, Gilbert, Newman, Broido & Clauset,
   or Leskovec & Krevl. Every formal claim in this document depends on them and
   they must be added before submission.
2. **Ambiguous and imprecise short citations.**
   * Becker's *Outsiders* is cited here as **Becker 1963**; the bibliography entry
     (`beckerOutsidersStudiesSociology1997`) is the 1997 reprint, so the entry
     needs `origdate = {1963}` for the short form to render correctly.
   * There are **two Mikhaylova 2022 items** in the bibliography — *Folk Devils or
     Moral Entrepreneurs?* (`mikhaylovaFolkDevilsMoral2022`) and *Измерение
     моральной паники на межличностном уровне* (`mihaylovaIzmerenieMoralnoyPaniki2022`).
     This document uses **2022b** for the former throughout; the a/b suffixes must
     be fixed consistently across the article. Note also that the surname is
     transliterated two ways across bibliography keys (`mihaylova` / `mikhaylova`),
     which will produce split author entries in some styles.
   * Hollander & Wu (2010) is a review of *normative agent-based systems*, not a
     statement of norm-entrepreneurship theory; the header note cites it for the
     implementation tradition and Finnemore & Sikkink (1998) for the theory.
   * The entry `hierRethinkingProblemDisproportion2024` carries `date = {2020-11}`
     and a `file` field pointing to a Walsh paper; the record appears to be
     corrupted and should be re-imported.
