# Appendix — robustness and artifact checks

**Spec §12.3 (appendix checks) and §14.2 (known artifacts). Produced by
`../Code/run_appendix.py`, 10 seeds per cell (3 for the asynchronous sweep), four runs per
seed. Reported as one table rather than in the main text, as the spec requires.**

Headline setting throughout: small world, $N=1000$, $\langle k\rangle=10$, $\epsilon=0.5$,
$\mu=0.30$, $\delta=0.25$, $\omega=0.35$, `base` repertoire, $\alpha_D=0.7$, $\rho_D=0.25$,
withdrawal at $t_{\text{off}}=150$, $T=400$.

Columns: $\Pi(149)$ is disproportion at withdrawal; $\Pi(399)$ is what survives 250 steps
later; **BC** is Sarle's bimodality coefficient on positions; **BC int** is the same
excluding agents pinned at $\pm1$; **bdry** is the share of agents sitting on a pole.

---

## 1. Population size (§12.3)

| $N$ | $\Pi(149)$ | $\Pi(399)$ | BC | BC int | bdry | handover |
|---|---|---|---|---|---|---|
| 500 | 0.292 ± 0.031 | 0.170 ± 0.088 | 0.856 | 0.856 | 0.003 | 2 (10/10) |
| 1000 | 0.292 ± 0.018 | 0.178 ± 0.051 | 0.987 | 0.987 | 0.003 | 2 (10/10) |
| 2000 | 0.293 ± 0.012 | 0.199 ± 0.011 | 0.989 | 0.989 | 0.005 | 2 (10/10) |

**Invariant.** $\Pi(149)$ agrees to three decimals across a fourfold change in population,
and only the across-seed dispersion moves — 0.031 → 0.018 → 0.012, i.e. roughly as
$N^{-1/2}$, which is what finite-size sampling noise should do and not a size effect. $N$ is
a modelling choice, not an empirical target (§2.4), and nothing in H1–H3 turns on it.

## 2. Empirical networks (§12.3)

Two graphs, retrieved by `../Code/fetch_empirical_network.py`, which records the URL, page,
citation, retrieval date, SHA-256 and realised structure alongside each edge list. Both enter
as **fixed structure only** (§9): direction, weights and any node attributes are discarded and
agent state is initialized exactly as in §8. Each is accompanied by the three generators of §4
re-run at its own realised $N$ and $\langle k\rangle$, so a structure effect is not confounded
with a density effect. The C3 probe was repeated on every row and **all eight pass**.

| Graph | topology | $N$ | $\langle k\rangle$ | $C$ | comp. | $\Pi(149)$ | $\Pi(399)$ | BC int | handover |
|---|---|---|---|---|---|---|---|---|---|
| **ca-GrQc** | empirical | 5 241 | 5.53 | 0.530 | 354 | 0.232 ± 0.004 | **0.135 ± 0.011** | 0.845 | 5 |
| | Watts–Strogatz | 5 241 | 6.00 | 0.439 | 1 | 0.268 ± 0.006 | 0.100 ± 0.027 | 0.980 | 3 |
| | Holme–Kim | 5 241 | 6.00 | 0.268 | 1 | 0.270 ± 0.009 | 0.072 ± 0.061 | 0.949 | 3 |
| | Erdős–Rényi | 5 241 | 5.43 | 0.001 | 23 | 0.244 ± 0.009 | **0.006 ± 0.001** | 0.385 | 3 |
| **ego-Facebook** | empirical | 4 039 | 43.69 | 0.606 | 1 | 0.238 ± 0.009 | 0.191 ± 0.007 | 0.991 | 2 |
| | Watts–Strogatz | 4 039 | 44.00 | 0.534 | 1 | 0.230 ± 0.005 | 0.198 ± 0.004 | 0.997 | 2 |
| | Holme–Kim | 4 039 | 43.51 | 0.104 | 1 | 0.227 ± 0.010 | 0.197 ± 0.009 | 0.997 | 2 |
| | Erdős–Rényi | 4 039 | 43.49 | 0.011 | 1 | 0.227 ± 0.003 | 0.198 ± 0.002 | 0.997 | 2 |

Sources: SNAP (Leskovec & Krevl 2014), retrieved 2026-08-04. ego-Facebook is Leskovec &
McAuley (2012), ten merged friendship circles; ca-GrQc is Leskovec, Kleinberg & Faloutsos
(2007), arXiv GR-QC co-authorship. Both realised sizes are one node and a few edges below the
published figures, because self-loops are removed on load.

**The headline result replicates on both, and $\Pi$ during the campaign is remarkably
insensitive to structure.** Across all eight rows — two empirical graphs, three generators
each, mean degree varying eight-fold — $\Pi$ at withdrawal lies between 0.227 and 0.270. The
episode the model produces while an entrepreneur is acting is essentially a property of the
parameters, not of the graph.

**What structure decides is what survives.** At $\langle k\rangle=43.7$ it decides nothing:
all four rows land at $\Pi(399)=0.191$–$0.198$ and are indistinguishable. At
$\langle k\rangle=5.5$ it decides almost everything, and the spread is a factor of twenty —
0.135 on the empirical graph against **0.006** on matched Erdős–Rényi, with the two clustered
generators in between at 0.100 and 0.072. Sparse *and* unclustered is the one combination in
which the division does not survive withdrawal: with mean degree 5.5 and no triangles, the
clusters bounded confidence carves out are too thin to hold, and noise re-merges them.

**No generator reproduces the sparse empirical graph.** ca-GrQc retains 0.135 where the best
matched generator retains 0.100 and the null retains 0.006. Its clustering (0.530) exceeds
Watts–Strogatz's at the same degree (0.439) and it carries 354 components against 1 — and the
model runs on the full graph rather than the giant component precisely because isolation is
substantively meaningful (§4). This is the row that justifies the appendix: at the operating
density the three generators bracket the empirical case, and at low density they do not.

**Two cautions.** Both graphs are denser than the operating point, and mean degree enters the
model in two load-bearing places — the claims-maker's share of an agent's alarm neighbourhood
is $\psi=g/(d+g)$, which *falls* as $d$ rises, so a claims-maker is diluted on a dense graph;
and the C3 boundary moves down with mean degree. The probe was therefore repeated per row and
passes everywhere, but the dilution is real and is why ego-Facebook's $\Pi$ is no higher than
the sparse cases despite far more contagion pathways. Second, ca-GrQc is a co-authorship
network rather than a friendship graph; it was chosen to bracket the operating degree from
below and for its component structure, not as a better instance of the type.

## 3. The fixed constants (§3.2, §12.3)

| Cell | $\Pi(149)$ | $\Pi(399)$ | BC | BC int | bdry | persistence |
|---|---|---|---|---|---|---|
| default | 0.292 ± 0.018 | 0.178 ± 0.051 | 0.987 | 0.987 | 0.003 | censored |
| $\sigma=0.05$ | 0.299 ± 0.014 | **0.005 ± 0.000** | 0.336 | 0.336 | 0.000 | 14 (0/10 censored) |
| $\sigma=0.10$ | 0.269 ± 0.013 | **0.007 ± 0.000** | 0.364 | 0.364 | 0.000 | 9 (0/10) |
| $\gamma=2.0$ | 0.198 ± 0.009 | 0.140 ± 0.029 | 0.987 | 0.987 | 0.003 | censored |
| $\gamma=5.0$ | 0.415 ± 0.014 | 0.368 ± 0.045 | 0.984 | 0.985 | 0.003 | censored |
| $\zeta=0.0$ | 0.289 ± 0.018 | 0.213 ± 0.041 | **0.996** | **0.660** | **0.192** | censored |
| $\zeta=0.05$ | 0.281 ± 0.025 | **0.024 ± 0.000** | 0.324 | 0.324 | 0.000 | censored |

Three separate readings.

**$\gamma$ is a quantitative dial and nothing more.** Halving it to 2 lowers $\Pi$ by a third,
raising it to 5 raises $\Pi$ by 42%; the shape, the handover step and the sign of every
conclusion are unchanged. Fixing $\gamma$ at 3 rather than making it a parameter costs
nothing (§3.2).

**$\sigma$ is not neutral, exactly as §3.2 warns.** Measured persistence is 14 and 9 steps
against the predicted $-1/\ln(1-\sigma)$ of 19.5 and 9.5, and $\Pi(399)$ collapses to 0.005.
The anchor is a restoring force toward each agent's *pre-campaign* position, which under the
consensual regime sits near zero, so it dissolves the manufactured division on its own
timescale whatever $\omega$ is. This is the reverse of H2 and it is why $\sigma=0$ is the
operating point. It also means the appendix check here is not a robustness result: it is a
demonstration that the constant cannot be fixed at a positive value and left out of the
analysis.

**$\zeta$ is not neutral either, and this was not anticipated.** At $\zeta=0.05$, $\Pi(399)$
falls to 0.024 and bimodality collapses to 0.324. Noise five times larger than the default
lets agents random-walk back across the tolerance boundary, at which point bounded confidence
stops being absorbing and the clusters re-merge. §3.2 originally said $\zeta$ "belongs to no
hypothesis; its only role is to prevent structurally frozen states" — right about its purpose
and wrong about its consequences, since at $\sigma=0$ the permanence of division *is* that
frozen state.

**This three-point bracket was not enough, and the four-input Sobol design replaced it.** The
spec's own standard, applied to $\sigma$, is that a constant competing with $\omega$ must
either be justified explicitly or enter §12.2. $\zeta$ now enters it, over two boxes
([H2 §2.6](H2_handover.md)): over $\zeta\in[0,0.02]$ the alarm split carries total index
**1.00** against 0.02 for noise, and over $\zeta\in[0,0.05]$ the ordering reverses to **0.39
against 0.75**. The default sits safely inside the first region, so nothing reported here
changes — but the H2 conclusion is now stated with a scope condition, $\zeta\lesssim0.02$,
instead of an assumption. §3.2 and §12.2 have been rewritten accordingly.

## 4. Update scheme (§12.3)

| Scheme | $\Pi(149)$ | $\Pi(399)$ | BC | bdry | handover |
|---|---|---|---|---|---|
| synchronous | 0.300 ± 0.024 | 0.208 ± 0.018 | 0.987 | 0.004 | 2 (3/3) |
| asynchronous | 0.310 ± 0.019 | 0.217 ± 0.011 | 0.986 | 0.004 | 2 (3/3) |

**No effect.** Random-order sequential updating moves $\Pi$ by 0.010, well inside the
across-seed dispersion, and leaves the handover step, the bimodality and the boundary share
alone. This is the expected result and the reason is stated in §14.2: excluding repulsion
from §7.2 means the period-2 oscillations that afflict synchronously updated repulsive models
cannot arise, so synchronous updating is not doing hidden work. The check is worth keeping
because it is cheap to state and expensive to assume.

## 5. Boundary pile-up (§14.2, artifact 1)

| Cell | one-step displacement at $b=0$ | $\Pi(149)$ | $\Pi(399)$ | BC | BC int | bdry | clip rate |
|---|---|---|---|---|---|---|---|
| clip, $\alpha_D=0.7$ | 0.700 | 0.292 ± 0.018 | 0.178 ± 0.051 | 0.987 | 0.987 | 0.003 | 4.55% |
| **tanh**, $\alpha_D=0.7$ | 0.604 | 0.284 ± 0.017 | 0.153 ± 0.056 | 0.986 | 0.986 | **0.000** | 0% |
| clip, $\alpha_D=0.9$ | 0.900 | 0.306 ± 0.013 | 0.221 ± 0.013 | 0.988 | 0.988 | 0.004 | 5.11% |
| **tanh**, $\alpha_D=0.9$ | 0.716 | 0.300 ± 0.011 | 0.194 ± 0.014 | 0.987 | 0.987 | **0.000** | 0% |

**The polarization is real, not pile-up.** This is the check the three hypothesis reports were
waiting on, and it clears them. Two independent lines say so. The interior coefficient, which
drops every agent sitting on a pole before taking moments, agrees with the raw coefficient to
three decimals (0.987 vs 0.987) — so the bimodality is not being produced by the atoms. And
replacing the hard clip with a bound that can never pin anyone leaves $\Pi$ within 0.008 at
withdrawal and the bimodality within 0.001, at zero boundary share. The 4.55% clip rate
counts *events* over the whole run — agents pushed past a pole and pushed back — not standing
mass: the standing boundary share at $t=399$ is 0.003. During the campaign it is higher,
0.110 at $t=149$, and even there the interior coefficient (0.9886) matches the raw one
(0.9893).

**A correction to the soft bound, which is worth recording.** The obvious implementation,
$b=\tanh(\text{raw})$, is wrong, and wrong in a way that produced a spurious collapse before
it was caught: $\tanh(x)<x$ for every $x>0$, so plain tanh is not only a bound but a
contraction toward the origin, and with no forcing at all it drives every position
geometrically to zero. That is a restoring force toward the pre-campaign consensus — the same
pathology §3.2 identifies in $\sigma$ — and under it $\Pi(399)$ fell to 0.005 for reasons
having nothing to do with the boundary. The implementation used above is the identity on
$[-0.9,0.9]$ with a tanh knee beyond it: $C^1$ at the join, strictly interior everywhere, and
unchanged wherever the hard clip would not have bound. **§14.2 should say "soft bound", not
"soft $\tanh$ bound", and should specify that the replacement must be the identity away from
the poles.**

## 6. Counterfactual validity (§14.2, artifact 2)

The decomposition assumes the four arms stay comparable. Each arm is replicated five times
with the same network, initial positions, alarm and thresholds but a different position-noise
substream; the horizon is the first step at which the largest within-arm spread exceeds 10%
of the full-versus-null gap the comparison is trying to resolve.

| Seed | horizon | largest within-arm noise s.d. | full − null gap at $T$ |
|---|---|---|---|
| 11 | not reached in the run | 0.0064 | 0.229 |
| 12 | not reached in the run | 0.0040 | 0.216 |
| 13 | 283 | 0.0310 | 0.149 |
| 14 | **191** | 0.0290 | 0.161 |
| 15 | 289 | 0.0247 | 0.200 |

**What is reportable.** Everything the three hypothesis reports read at or before withdrawal
— $\Pi(149)$, the decomposition curves, the handover step (which is 2), $q$, $\bar b$,
$\bar\Phi$ — sits far inside the horizon in every seed, with a margin of at least 40 steps in
the worst case. The quantity that does *not* sit inside it in every seed is $\Pi(399)$: in
three of five seeds the within-arm noise passes the tolerance somewhere between $t=191$ and
$t=289$.

That does not invalidate $\Pi(399)$, and it should not be read as doing so. Past the horizon
a *single trajectory* is no longer a reliable read of the counterfactual, because re-drawing
the noise moves one arm by more than a tenth of the effect; the seed-averaged level is still
estimable, which is why §2.2 of the H2 report gives $\Pi(399)$ as a mean ± s.d. over 20 seeds
rather than as a trajectory. The operational rule this check produces: **report late-run
quantities as distributions over seeds only, never as curves, and never from one run.**

The mechanism is the one to expect. After withdrawal the system is in a frozen divided state
whose exact partition depends on which agents happened to be pushed past tolerance, so noise
that was irrelevant during forcing becomes the thing that picks between nearby equilibria.
It is also why the horizon correlates with the gap: seeds 11 and 12, whose full−null gap is
largest, never trip the criterion at all.

---

## 7. Provenance

`../Code/networks/` holds each edge list beside a `*.provenance.json` recording the source
URL, the dataset page, the citation, the retrieval date, the SHA-256 of the file and its
realised structure, so the appendix rows above can be audited without re-downloading. The
retrieval script also lists a third candidate it did not use, `email-Eu-core` ($N=1005$,
$\langle k\rangle=32$), whose size matches the headline population exactly but which is
directed at source and would require discarding direction — a real simplification that the
two chosen graphs do not force.

```bash
cd Code && python fetch_empirical_network.py --list
```
