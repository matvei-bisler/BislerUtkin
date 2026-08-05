# `moralpanic`

Reference implementation of the agent-based model specified in
[`../model_simplified.md`](../model_simplified.md). Every module names the
specification sections it implements, and every non-obvious choice in the code
points back to the section that requires it.

## Install and check

```bash
pip install -r requirements.txt
python run_verification.py
python run_reproduction.py    # optional: regenerates every table below (~1 min)
python run_hypotheses.py      # the three experiments of §12.1 (~4 min, 15 cores)
python run_appendix.py        # the §12.3 appendix and §14.2 artifact checks (~2 min)
```

`run_verification.py` runs the five limiting cases of spec §12.3 plus seven
property checks. It should print `14/14 checks passed`. Verification asks only
whether the code implements the specification; it is reported separately from
any substantive result. `run_reproduction.py` regenerates the pilot tables in
this README from the specification alone, over seeds 11–20, so none of the
numbers below has to be taken on trust.

| Check | What it pins down |
|---|---|
| 1. DeGroot consensus | positions converge to one value at `sigma=0, epsilon=2, gamma=1` |
| 2. Friedkin–Johnsen equilibrium | positions hit `(I-(1-sigma)M)^-1 sigma b(0)` at `sigma>0` |
| 3. Hegselmann–Krause clustering | surviving cluster count falls as `epsilon` rises, reaching 1 at `epsilon=2` |
| 4. Mean-field fixed point | simulated steady alarm matches the analytic `a*` of spec §3.3 |
| 5. Empty graph | positions relax to their anchors, alarm decays to zero, `Pi` is identically zero |
| P1. Interaction zero at `t=1` | the §10.1 property holds to machine precision |
| P2. Determinism | one seed reproduces one trajectory bit-for-bit |
| P3. Silencing is by reach | `alpha=0` does **not** silence an actor; `rho=0` does |
| P4. Interior bimodality | boundary atoms inflate Sarle's coefficient; the interior version ignores them (docked against an analytic three-point case) |
| P5. The soft bound | under `BoundMode.TANH` nothing is ever pinned to a pole |
| P6. Asynchronous updating | a scheme change only: identical step-0 record, reproducible under a fixed seed |
| P7. Counterfactual validity | re-drawing the noise moves one arm far less than the full-vs-null gap |
| P8. `fixed_random` | the control addresses one set every step, carries no degree signal, and is shared across the 2x2 arms |
| P9. Handover guard | the criterion declines after withdrawal instead of firing on the entrepreneur's exit |

## Minimal use

```python
from moralpanic import (
    Parameters, NetworkSpec, RunConfig, Repertoire, Topology,
    entrepreneur, run_counterfactual_set,
)

config = RunConfig(
    seed=11,
    n_steps=500,
    network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=600, mean_degree=10.0),
    parameters=Parameters(epsilon=0.5, mu=0.30, delta=0.25, omega=0.35),
    actor_d=entrepreneur(alpha=0.7, rho=0.25,
                         repertoire=Repertoire.BASE, active_until=150),
)

result = run_counterfactual_set(config)     # four runs on one seed
d = result.decomposition

d.panic_index          # Pi(t), spec §10.2
d.claims_alone         # what the entrepreneur injected
d.interaction          # what the division it created then generated
d.othering_alone       # division that pre-existed the episode

result.handover_step()          # spec §10.3, the primary quantity for H2
result.persistence(t_off=150)   # censored duration after withdrawal
```

## Layout

| Module | Spec sections | Contents |
|---|---|---|
| `config.py` | §3, §5, §8 | parameters, constants, actor specs, initialization regimes |
| `rng.py` | §8, §15 | the three seeded streams |
| `network.py` | §4 | the three generators at matched mean degree |
| `actors.py` | §7.1 | the four claims-making repertoires |
| `model.py` | §6, §7 | the four update rules, synchronous |
| `measures.py` | §10.3 | per-step measurements |
| `counterfactual.py` | §10.1, §10.2 | the 2×2 design, decomposition, panic index |
| `sensitivity.py` | §12.2 | simplex reparameterization, Saltelli/Jansen Sobol estimators, Ishigami validation |
| `experiments.py` | §12.1 | Experiments A, B and C, and the depth x reach grid |
| `appendix.py` | §12.3, §14.2 | population size, empirical network, fixed constants, update scheme, boundary pile-up, counterfactual validity |
| `verification.py` | §12.3 | the limiting cases and property checks |

| Script | Does |
|---|---|
| `run_verification.py` | the 12 checks above |
| `run_reproduction.py` | the pilot tables in this README |
| `run_hypotheses.py` | Experiments A/B/C and the Sobol design, to `../Results/data/` |
| `run_appendix.py` | the §12.3 appendix table and the §14.2 artifact checks |
| `fetch_empirical_network.py` | retrieves one public network for §12.3 and records its provenance |

## Four things the code enforces that are easy to get wrong

**Silencing is by reach, never by depth.** `alpha` appears only in the position
update. An actor with `alpha=0` and `rho>0` persuades no one but still enters
the alarm neighbourhood of everyone it reaches as a maximally alarmed contact,
so the "null" arm of the 2×2 would not be null. `ActorSpec.silenced()` sets
`rho=0`, and `P3` in the verification suite fails loudly if the two are ever
confused.

**Common random numbers are asserted, not assumed.** All four arms are built
from the same seed and must produce an identical network, identical initial
positions, alarm and thresholds. `run_counterfactual_set` compares fingerprints
across arms and raises if they differ. Targeting and noise draw from separate
streams so that the silent arms, which consume no targeting draws, still see the
same noise sequence.

**Time-`t` quantities are all computed before either state array is written.**
The othering exposure reads `b(t)`, never the freshly computed `b(t+1)`. The
update is synchronous in fact and not only in intent.

**The polarized regime is truncated by rejection, never by clipping.** Clipping
a Normal onto `[-1, 1]` leaves point atoms at the bounds that are
indistinguishable from the boundary pile-up the dynamics produce, which would
pre-load the polarization measure with the artifact the robustness check exists
to detect.

## What the pilot runs show

All numbers below come from `run_reproduction.py` (seeds 11–20, small world,
`N=600`, mean degree 10, `epsilon=0.5, mu=0.30, delta=0.25`, `base` repertoire,
`alpha=0.7`, withdrawal at `t_off=150`, `T=400`; means ± s.d. over seeds).

**The exposure rule decides whether the model can escalate at all.** Under the
weighted-mean form (`ExposureMode.PROPORTIONAL`), `E_i` is a mean of neighbour
alarm and so can never exceed its largest input. The population maximum then
contracts geometrically under C2 and endogenous escalation is impossible — this
was checked up to `gamma = 1000`, where the peak still never rose. Amplification
only re-weights who counts, and the response damps the forcing. Dividing by the
neighbour **count** instead (`ExposureMode.REINFORCING`, the default) lets
alarmed neighbours add rather than re-weight, and the response amplifies it
(spec §1.4, patterns 1–2):

| `rho` | `Pi(149)` reinforcing | `Pi/rho` | `Pi(149)` proportional | `Pi/rho` |
|---|---|---|---|---|
| 0.05 | 0.063 ± 0.009 | **1.26** | 0.051 ± 0.005 | 1.01 |
| 0.10 | 0.125 ± 0.017 | **1.25** | 0.089 ± 0.011 | 0.89 |
| 0.20 | 0.240 ± 0.026 | **1.20** | 0.149 ± 0.016 | 0.75 |
| 0.40 | 0.404 ± 0.021 | 1.01 | 0.218 ± 0.016 | 0.54 |

The two forms coincide exactly at `gamma = 1`.

**Mass broadcast is self-limiting.** The interaction term peaks at intermediate
reach and collapses at full reach, because moral distance arises from
*differences* in exposure:

| `rho` | 0.05 | 0.10 | 0.25 | 0.40 | 0.70 | 1.00 |
|---|---|---|---|---|---|---|
| interaction at `t=149` | 0.050 | 0.104 | 0.243 | **0.332** | 0.291 | 0.001 |
| persistence after withdrawal | censored | censored | censored | censored | censored | **2** |

At full reach the population moves toward one pole together and homogenizes, so
broadcast unites rather than divides. This is the H1 clause in spec §13.

**Othering is what survives withdrawal, in the sub-critical regime.** At
`mu=0.30, delta=0.25` (C3-subcritical: the seeded-contagion probe dies out;
the null run's mean alarm never exceeds 0.053):

| `omega` | `Pi` at 149 | `Pi` at 299 | persistence |
|---|---|---|---|
| 0.00 | 0.041 ± 0.001 | 0.000 | 2 |
| 0.20 | 0.156 ± 0.015 | 0.077 ± 0.035 | mostly censored |
| 0.35 | 0.290 ± 0.031 | 0.191 ± 0.059 | mostly censored |
| 0.45 | 0.389 ± 0.029 | 0.311 ± 0.055 | all censored at 250+ |

This is H2's prediction met: `Pi` decays to zero when `omega = 0` and to a
positive floor when `omega > 0`.

**Depth against tolerance decides whether claims-making divides or converts.**
The one-step displacement of a reached agent is roughly `alpha * (1 - b)`. When
that stays below `epsilon`, reached agents remain audible to their neighbours
and drag the whole population to the pole: at `alpha = 0.2–0.4` mean position
ends near `+0.98`, the interaction term is ~0, and there is nothing to hand
over — the entrepreneur wins the argument and gets no panic. When it exceeds
`epsilon` (`alpha = 0.7`), reached agents sever their bounded-confidence ties in
one step, the population cleaves, and the interaction term (~0.26) outlives the
campaign. Division, not persuasion, is what persists.

**The anchor dissolves manufactured division.** `sigma` defaults to `0` for a
reason. The term `sigma * b_i(0)` is a restoring force toward each agent's
*pre-campaign* position; under the consensual regime those all sit near zero, so
a positive `sigma` returns the population to consensus after the entrepreneur
withdraws. Measured persistence tracks the anchor's relaxation time
`-1/ln(1-sigma)` rather than `omega`:

| `sigma` | predicted `-1/ln(1-sigma)` | measured persistence |
|---|---|---|
| 0.00 | infinite | censored at 250+ |
| 0.05 | 19.5 | 14 |
| 0.10 | 9.5 | 7–9 |
| 0.20 | 4.5 | 4–5 |

That is the reverse of H2, which predicts `omega` governs persistence. At
`sigma=0` bounded confidence is absorbing, division is permanent, and `Pi`
decays to the positive floor H2 predicts. See spec §3.2.

**Stay below the reinforcement threshold (spec §3.3, C3).** Above roughly
`mu + delta = 0.7` at mean degree 10 and `gamma = 3`, alarm self-sustains from any
positive seed and settles at `delta/(1-mu)` whatever the claims-maker does. There
H2 is true for the wrong reason and the counterfactual loses its point, because
alarm no longer depends on the forcing. Check any new parameter point with
`counterfactual.is_subcritical(config)`, which measures the property rather than
asserting a closed form, since the threshold depends on the degree distribution.

**Not achievable: a discontinuity in reach.** Panic incidence responds smoothly
and concavely to `rho` at every `gamma` tried, in both exposure modes. The
model's qualitative signature is amplification (`Pi > rho`), not a tipping point.
Spec §1.4 and H1 were corrected accordingly.

## Two controls worth knowing about

**`Repertoire.FIXED_RANDOM` is a measuring instrument, not a strategy.** `hub` and `base`
differ from `random` in two ways at once -- whom they select, and that they select the
*same* people every step -- so an effect attributed to degree targeting may be an effect
of a fixed audience. `fixed_random` has `random`'s selection rule and `hub`'s exposure
schedule, which makes the two separable. Its audience is nested in `rho` and derived from
(seed, actor), so it is identical across the four arms of the 2x2.

**`handover_step` is guarded by the actor's own window.** After withdrawal claims-alone is
zero, so `interaction > claims_alone` holds for any positive interaction whatever and the
unguarded criterion reports a handover on the exit step. It defaults to the entrepreneur's
`active_until`; pass `require_active=False` to recover the unguarded definition.

## Three more things the code enforces

**Bimodality is reported twice, and the pair is the diagnostic.** `bimodality`
includes the atoms the hard clip accumulates at the poles;
`bimodality_interior` drops every pinned agent before taking moments. A gap
between them means the polarization is pile-up rather than structure (spec
§14.2). At the operating point there is no gap: 0.9886 against 0.9893.

**The soft bound is the identity away from the poles, not a plain tanh.**
`tanh(x) < x` for every `x > 0`, so plain tanh is a bound *and* a contraction
toward the origin -- a restoring force that dissolves manufactured division for
reasons having nothing to do with the boundary, exactly the pathology spec §3.2
identifies in `sigma`. `model.soft_bound` is the identity on `[-0.9, 0.9]` with a
`C1` tanh knee beyond it.

**The asynchronous sweep order comes from (seed, step), not from a stream.**
Taking it from `targeting` would desynchronise it across the arms of the 2x2,
because the silent arms consume no targeting draws; taking it from `noise` would
desynchronise the noise. Either breaks the common random numbers.

## Reproducibility

One `numpy.random.Generator` (PCG64) per run, seeded from a recorded integer, no
global RNG state. Parallelism should draw independent substreams via
`SeedSequence.spawn` rather than reseeding, so results stay invariant to worker
count. Given a seed, a topology and a parameter vector, a run is exactly
reproducible.
