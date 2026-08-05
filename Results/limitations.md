# Limitations, and the conditions under which the results hold

**Everything below is measured or specified, not speculated. Where a limit was found rather
than anticipated, it says so; where it was anticipated in `../model_simplified.md` §14.1 and
confirmed, it points there.**

The document has four parts, in descending order of how likely each is to change a reader's
mind about a claim:

1. **Scope conditions** — parameter windows outside which a stated result fails
2. **Instrument limits** — what the measurements can and cannot say
3. **Structural exclusions** — what the model does not represent at all
4. **Scalability** — what it costs to run, and what does and does not scale

A one-page checklist is at the end.

---

## 1. Scope conditions

These are not caveats. Each names a region of parameter space in which a result reported in
H1–H3 **fails**, and each was located by measurement.

### 1.1 The anchor must be exactly zero — $\sigma=0$

| $\sigma$ | 0.00 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| predicted relaxation $-1/\ln(1-\sigma)$ | ∞ | 19.5 | 9.5 | 4.5 |
| measured persistence | censored (111/125) | 13 | 9 | 4 |
| $\Pi$ 250 steps after withdrawal | 0.179 | 0.005 | 0.007 | — |

The anchor $\sigma b_i(0)$ is a restoring force toward each agent's *pre-campaign* position,
which under the consensual regime sits near zero. Any positive $\sigma$ therefore dissolves
manufactured division on its own timescale, whatever $\omega$ is, and post-withdrawal
persistence tracks $-1/\ln(1-\sigma)$ rather than othering. **This is the reverse of H2.**

Anticipated in §3.2 and confirmed quantitatively. The consequence for reading the model: H2's
persistence result is a statement about a population with **no restoring force toward its prior
convictions**. Whether real populations have one is not a question this model can answer, and
if they do, the result does not transfer.

### 1.2 Position noise must stay small — $\zeta\lesssim0.02$

Total-order Sobol indices on persistence, four-input design (§12.2):

| $\zeta$ box | split ($u_1+u_2$) | intensity $s$ | **noise $\zeta$** |
|---|---|---|---|
| $[0,\,0.02]$ — twice the default | **1.00** | 0.03 | 0.02 |
| $[0,\,0.05]$ — five times the default | 0.39 | 0.02 | **0.75** |

**This is the sharpest and least expected limit on the whole project.** Over a generous box,
position noise out-explains the alarm split roughly two to one; over a narrow one it is
irrelevant. The crossover lies between twice and five times the default, and the operating
point ($\zeta=0.01$) sits safely inside the region where othering governs — so nothing reported
in H1–H3 is affected. But the claim is conditional, and the condition is not derivable from
anything inside the model.

The mechanism is the same as §1.1 reached by a different route: at $\sigma=0$ bounded
confidence is absorbing, so the permanence of division *is* the structurally frozen state
$\zeta$ exists to prevent. A position that random-walks back across the tolerance boundary
re-enters its neighbours' audible range and clusters re-merge.

Substantively: **the permanence of manufactured division requires that moral positions not
drift.** How much they drift is an empirical question this model does not settle. Note the
asymmetry with $\sigma$ — the anchor's effect is signed and analytically predictable, whereas
$\zeta$'s is a threshold whose location had to be measured.

Handover time is untouched in both boxes ($S_T\le0.03$), so what noise governs is what
*survives*, not when the transfer happens.

### 1.3 Contagion must be sub-critical, and $\mu+\delta$ is not the test

Four of 45 simplex points fail the measured C3 probe, all near the $\delta$ vertex, and **all
four have $\mu+\delta\le0.60$** — comfortably below the $\approx0.7$ figure a scalar bound
suggests. The boundary is a **surface in the simplex**, not a value of $\mu+\delta$: an
amplifying neighbour enters at weight $\gamma$, so at the $\delta$ vertex the effective gain
$\delta\gamma=1.8$ already exceeds one.

Above the boundary alarm self-sustains from any positive seed whatever any claims-maker does,
the counterfactual decomposition loses its meaning because alarm no longer depends on the
forcing, and H2 comes out *true for the wrong reason*: in the raw simplex scan the highest
persistence in the study ($\Pi(399)=0.585$) sits at the supercritical $\delta$ vertex, against
0.097 at the $\omega$ vertex. **Without the audit the scan reads as a refutation of H2; with it
the maximum sits exactly on the $\omega$ vertex.**

Condition for transfer: the probe must be re-run at **every** reported parameter point and at
every mean degree, because the boundary moves with the degree distribution. It is not
inheritable from the operating point.

### 1.4 Depth must exceed tolerance — the gate

Below $\alpha_D(1-\bar b)\approx\epsilon$ the entrepreneur *converts*: reached agents stay
inside their neighbours' tolerance, $\bar b\to0.99$, the interaction term is zero and **no
amount of reach ignites anything**. Above it, $\alpha_D$ stops mattering (0.70, 0.80 and 0.90
differ by <0.02) and $\rho_D$ takes over.

The transition band is narrow and **bistable**: between $\alpha_D=0.62$ and $0.68$ the
across-seed s.d. of $\Pi$ inflates from 0.014 to 0.064, meaning that within a single parameter
cell some seeds cleave and others converge, depending on which agents happen to be reached
first. Reporting a mean there is misleading; the distribution is bimodal.

Tolerance is the same gate seen from the other side, and both must be reported as a pair, never
as separate dials.

### 1.5 The initial regime must be consensual for the decomposition to be interpretable

| Regime | $\bar\Phi(0)$ | interaction(149) | othering-alone(149) | guarded handover |
|---|---|---|---|---|
| consensual | 0.067 | **0.243** | 0.005 | 2 (250/250 seeds) |
| polarized | 0.386 | **0.024** | 0.500 | 4 (**28**/250 seeds) |

Under a divided start almost all the alarm is othering over division that pre-existed the
campaign, which is precisely what the interaction term is constructed to exclude. §10.3 calls
such a cell **attenuated rather than a clean test**, and it is reported as one. The substantive
reading — an already-divided population needs less entrepreneurship — is supported by the
interaction being an order of magnitude smaller; the *timing* claims cannot be evaluated there
at all.

This matters for any empirical extension: a measured $b_i(0)$ would put most real populations
into the attenuated case, not the clean one.

### 1.6 Density changes what survives, and the operating point is mid-range

From the two empirical networks and their matched generators
([`empirical_network.md`](empirical_network.md)):

- $\Pi$ **during** the campaign is nearly density-invariant: 0.227–0.270 across an eight-fold
  range of mean degree.
- $\Pi$ **after** withdrawal is not. At $\langle k\rangle=43.7$ topology decides nothing
  (0.191–0.198, indistinguishable). At $\langle k\rangle=5.5$ it decides a factor of twenty,
  monotone in clustering: 0.135 / 0.100 / 0.072 / **0.006** at $C$ = 0.530 / 0.439 / 0.268 /
  0.001.

Two mechanical consequences of degree that must travel with any density claim. The
claims-maker's share of an agent's alarm neighbourhood is $\psi=g/(d+g)$, which **falls** with
degree — 0.153, 0.091, 0.022 at $\langle k\rangle$ = 5.5, 10, 43.7 — so a claims-maker is
diluted on a dense graph. And the C3 boundary moves down with degree, so sub-criticality is not
inheritable across densities.

---

## 2. Instrument limits

### 2.1 Disproportion is internal, and this is the hard ceiling

$\Pi$ measures alarm in excess of **the model's own counterfactual**, not in excess of real
danger. The model has no objective threat referent against which a reaction could be judged
excessive. It formalizes the *structure* of Goode & Ben-Yehuda's disproportionality criterion
and makes it **computable**, without making it **decidable** for any real episode.

Anticipated in §14.1. No amount of further computation, better data or larger networks moves
this line — it is a property of what a counterfactual simulation can be. It should be as
visible in an abstract as it is here.

### 2.2 The counterfactual-validity horizon bounds late-run reading

Each arm replicated five times with the same population and different position-noise
substreams; the horizon is where the largest within-arm spread exceeds 10% of the
full-versus-null gap:

| Seed | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|
| horizon | not reached | not reached | 283 | **191** | 289 |

Everything read at or before withdrawal — the decomposition, $\Pi(149)$, the handover, $q$,
$\bar b$, $\bar\Phi$ — sits far inside the horizon in every seed. $\Pi(399)$ does not, in three
of five. **Operational rule, and it is followed throughout: late-run quantities are reported
as distributions over seeds, never as trajectories, and never from one run.**

The cause is expected rather than alarming: after withdrawal the system sits in a frozen
divided state whose exact partition depends on which agents were pushed past tolerance, so
noise that was irrelevant during forcing becomes what selects between nearby equilibria.

### 2.3 The handover time is nearly uninformative, and has been demoted

It was specified as "the primary quantity for H2". It is not, and §10.3 now says so:

- **Its answer is a constant.** The interaction overtakes claims-alone at $t=2$ — the earliest
  step §10.1 permits — at every depth, tolerance and topology at which it happens at all. The
  fine sweep across the gate closed the last escape route: there is **no regime in which the
  transfer is gradual.**
- **It needed a window guard.** Unguarded it fires at $t_{\text{off}}+1$ once claims-alone
  reaches zero — arithmetic, not a transfer.
- **It is a ratio test and fires on near-zero quantities.** At $\alpha_D=0.55$ it is met while
  $\Pi=0.045$ and the interaction is 0.000. It must be read beside a level and reported only
  for cells meeting the panic criterion.

The **composition ratio** (interaction ÷ claims-alone, at a stated step while $D$ acts) is the
primary quantity in its place: a magnitude rather than a date, defined whether or not any
threshold is crossed, and it degrades gracefully.

### 2.4 Persistence is censored, so it is a bound and not a measurement

At the operating point 210 of 250 seeds are censored at 250 steps; at $\omega\ge0.2$, 176–235
of 250. At $\sigma=0$ bounded confidence is absorbing, so clusters more than $\epsilon$ apart
can never re-merge and the floor never decays. "Alarm outlives its cause" is therefore
demonstrated as **bounded below**, not measured as a duration. The residual *level*
$\Pi(399)$ is the statistic with information in it, which is why the Sobol analysis uses the
residual ratio.

### 2.5 The apparent tipping point in panic incidence is an artifact of thresholding

Incidence goes from 0.08 to 0.96 between $\rho_D=0.15$ and $0.20$, while the underlying $\Pi$
moves smoothly from 0.177 to 0.234 with an across-seed s.d. of 0.015. A step function applied
to a smooth quantity with small variance is a step function.

This is why §10.2 requires reporting over a grid of $(\Pi^*,q^*,W)$ rather than at one cut —
and it is a warning worth carrying into the empirical literature, where episode counts may
inherit their sharpness from the coding rule rather than from the phenomenon.

### 2.6 One Sobol output is unusable and is flagged automatically

$\Pi(399)$ returns $S_T(s)=1.755$, above the theoretical bound of 1: near-zero output variance
with a large atom at exactly zero. `sobol_indices` marks it `reliable: False`. It is reported
as estimator failure, never as a finding. The two outputs the hypothesis actually rests on —
the residual ratio and the handover step — are reliable in every design run.

### 2.7 Alarm has no object

$a_i$ records *how* alarmed an agent is, not *what* it fears. The model cannot distinguish fear
of the folk devil from fear of the mob, and reads the object off $b_i$ by convention (§2.1).
Anticipated in §14.1.

### 2.8 Boundary pile-up: checked and cleared, with one residual caveat

The interior bimodality coefficient agrees with the raw one to three decimals (0.9886 vs
0.9893), the standing boundary share is 0.003 at run's end, and replicating under a bound that
can never pin anyone leaves $\Pi(149)$ at 0.284 against 0.292. **The polarization reported is
emergent, not artifact.**

The residual caveat is about the check, not the result: the soft bound is the identity on
$[-0.9,0.9]$ with a $C^1$ knee beyond. A plain $\tanh$ — which §14.2 originally asked for — is a
bound *and* a contraction toward the origin, and under it the effect spuriously collapsed
before the error was caught. Any future re-specification of the bound must preserve
identity-away-from-the-poles.

---

## 3. Structural exclusions

All specified in §14.1 and unchanged by the runs. Each was considered and left out because
including it would add mechanism without serving the claim of §1.2. Together they bound what
the results can be taken to show.

| Excluded | Consequence for the results |
|---|---|
| **Network rewiring** | The most consequential omission, and why repulsion is excluded too: on a static graph, active repulsion and structural sorting cannot be told apart. The model **under-represents** divergence rather than mis-attributing it, which is the safe direction |
| **Repulsion in §7.2** | Agents disengage from the morally distant but are not driven away by them, so divergence is attributable to one mechanism. Also why period-2 oscillations cannot arise, which the asynchronous check confirms |
| **Any algorithm or recommender** | `hub` targeting is a proxy for structural position, not for platform promotion. **Claims about platform dynamics should not be read off this model** |
| **A reassurance channel** | Every claims-maker enters the alarm neighbourhood of everyone it reaches as a maximally alarmed contact; no message says *there is no threat*. H3's finding that defense lowers alarm **only by total conversion** is conditional on this, and would be the first thing to test in an extension |
| **Institutional legacy** | Legacy here is purely attitudinal — residual alarm in individuals. The model can show a panic outlasting its cause; it cannot show it hardening into law or enforcement capacity |
| **Exit, disengagement, self-censorship** | The spiral of silence, well documented in moralized environments, is absent |
| **Learning claims-makers** | Repertoires are fixed within a run. Experiment C gives a one-shot response and nothing more; in a contest where $D$ could re-enter, $C$ would never get the 250 uninterrupted steps its conversion result depends on |
| **Planted community structure** | Echo chambers are not built in; clustering of alarm is measured where it emerges. The most natural extension |
| **Adaptation, objectives, learning, prediction in agents** | Agents respond through fixed involuntary update equations. Strategic agency lies entirely with the claims-maker — which is the division of labor by which the model addresses the micro–macro gap, and also its strongest simplification |

---

## 4. The model is narrower than its parameter count suggests

Six parameters and four rules, but the runs show **three effectively live dimensions**:

| Live | Dead or nearly so |
|---|---|
| $\alpha_D$ **versus** $\epsilon$ — one gate, not two dials | $\mu$ — the $\mu$-versus-rest split carries $S_T=0.001$ on persistence |
| $\rho_D$ — magnitude, non-monotone, peaking at intermediate reach | $\delta$ — matters only through C3 and the calm-regime decay |
| $\omega$ — persistence, subject to §1.1 and §1.2 | $\gamma$ — a pure quantitative dial: halving it lowers $\Pi$ by a third, no conclusion changes |
| | threshold dispersion — a gain multiplier (35–40% level shift), leaving shape and peak location untouched |

This is parsimony rather than a defect, and the model is better for it. But the ODD apparatus
advertises more dimensionality than the model has, and a reader who expects six independent
levers will be misled. Stating the reduction explicitly is more honest than leaving it to be
inferred from the sensitivity table.

---

## 5. Scalability

### 5.1 What scales well

**Population size.** $\Pi(149)$ agrees to three decimals across a fourfold change in $N$
(0.292 / 0.292 / 0.293 at $N$ = 500 / 1000 / 2000); only the across-seed dispersion moves, as
$N^{-1/2}$ (0.031 / 0.018 / 0.012). $N$ is a modelling choice, not an empirical target (§2.4).
**Raising $N$ is safe and buys nothing but tighter error bars.**

**The update scheme.** Synchronous against random-order asynchronous: $\Pi(149)$ = 0.300 vs
0.310, inside the across-seed dispersion. The scheme is not doing hidden work.

**Cost in the main design.** The full 250-seed program is 76 288 counterfactual sets — 305 152
simulation runs — in **54 minutes on 15 cores**. Per set, cost is roughly linear in $|E|$ and
in $T$.

### 5.2 What scales badly

**Dense graphs.** Cost tracks edges, not nodes: ego-Facebook (88 234 edges) runs about 17×
slower per step than the baseline (5 000 edges), so the eight-row empirical appendix alone took
8 minutes at 10 seeds. A 250-seed empirical design would be hours.

**The asynchronous sweep.** A Python loop, roughly 50× the vectorised path. Adequate for the
three-seed appendix check; anything more needs a compiled inner loop.

**Seeds, in the wrong place.** The 250-seed program costs 13× the 20-seed pilot and **every
point estimate matched the pilot to within 0.01.** The seeds buy only the incidence tables,
whose standard error they take from ±0.11 to ±0.032 (§12.1). A rational re-run puts 250 seeds
on the headline incidence cells and leaves the exploratory grid at 20 — about 8 minutes instead
of 54.

**Output volume.** 64 MB of JSON at 250 seeds, after per-seed onset grids and curves are
aggregated at grouping time. Without that aggregation it would be several hundred.

### 5.3 Statistical resolution actually achieved

| Quantity | Resolution |
|---|---|
| Panic incidence | s.e. ≤ ±0.032 at 250 seeds — meets the §12.1 tolerance |
| $\Pi$ and the decomposition terms | across-seed s.d. ≤ 0.05 in every cell; settled at 20 seeds |
| Sobol indices | $N=256$ base samples; reliable for the residual ratio and handover, not for $\Pi(399)$ |
| Simplex scan | 62 seeds per lattice point — adequate for ranking, not for point estimates |
| Appendix rows | 10 seeds (3 asynchronous) — comparisons only, not rates |

---

## 6. Checklist: conditions for the results to transfer

Before quoting any H1–H3 result at a new parameter point, network or scale:

- [ ] **C3 probe re-run at that point** — the boundary is a surface in the simplex and moves with mean degree; it is not inheritable
- [ ] **$\sigma=0$**, or persistence re-derived — at $\sigma>0$ the floor is the anchor's, not othering's
- [ ] **$\zeta\lesssim0.02$**, or the four-input Sobol design re-run — above it noise out-explains the split
- [ ] **Depth and tolerance reported as a pair**, with the gate located; a mean inside the bistable band $0.62<\alpha_D<0.68$ is misleading
- [ ] **Initial regime stated** — the polarized case is attenuated, not a clean test of the interaction term
- [ ] **$\max_t\bar a^{\varnothing}$ recorded** — the panic index divides by $1-\bar a^{\varnothing}$
- [ ] **$\bar\Phi(0)$ recorded** — so pre-existing distance is visible rather than inferred
- [ ] **Late-run quantities as seed distributions only**, and inside the validity horizon
- [ ] **Handover reported only where the panic criterion is met**, and beside a level
- [ ] **Interior bimodality beside the raw coefficient** whenever polarization is claimed
- [ ] **Results over a grid of $(\Pi^*,q^*,W)$**, never at one cut

And the one that cannot be checked off: **$\Pi$ is excess over the model's own counterfactual,
not over real danger.** Every quantitative claim in H1–H3 is a claim about this model. The
contribution is that the disproportionality criterion becomes computable and the elite-versus-
interactionist dispute becomes an apportionment — not that any actual episode has been
measured.
