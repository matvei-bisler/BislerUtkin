# What remained, and how it closed

A record of the gap between `../Code/` and `../model_simplified.md`, what closed it, and the
condition under which the model counts as implemented and the hypotheses as tested in full.

**Status: closed.** Every mechanism, measurement, experiment and check the specification
names exists, is verified and has been run; the specification has been corrected everywhere
the runs contradicted it; and the reports carry a verdict on every registered clause.

This document began as a list of what remained. It is kept as a record of what the gap
between code and specification turned out to be, because the shape of that gap is itself
worth reporting: **the code was nearly complete and the specification was not.** What the runs
produced was a set of specific, locatable places where the *specification's own predictions*
were wrong — and a specification that predicts something the model does not do is a defect in
the same sense as a bug. Sections 2 and 3 record those and their resolution; §5 is the
completed checklist; §6 is what remains deliberately out of scope.

---

## 1. Where things stand

**Implemented and verified.** §2–§11 in full; the three experiments of §12.1 including the
$\alpha\times\rho$ grid and the fixed-audience control; the simplex reparameterisation and a
self-contained Saltelli/Jansen Sobol analysis for §12.2; all five verification limits and nine
property checks for §12.3 (`14/14 checks passed`); the four appendix replications of §12.3;
both artifact checks of §14.2.

**Run.** 76 288 counterfactual sets for H1–H3, the Sobol designs and the appendix. Reported in
[`H1_ignition.md`](H1_ignition.md), [`H2_handover.md`](H2_handover.md),
[`H3_defense.md`](H3_defense.md), [`appendix_robustness.md`](appendix_robustness.md),
[`empirical_network.md`](empirical_network.md) and [`limitations.md`](limitations.md).

**Totals.** 76 288 counterfactual sets, i.e. **305 152 simulation runs**. 14/14 verification
checks. Twenty-two specification edits. Two empirical networks with provenance.

---

## 2. The eleven specification defects, and how each was resolved

Ranked by whether a claim in the paper depended on it. None was a matter of taste: each was a
sentence in `model_simplified.md` that the runs contradicted. All eleven are now fixed in the
specification; the numbers below are from the final 250-seed runs.

### Load-bearing — a stated hypothesis is wrong as written

| # | Where | What it says | What the runs show | Fix |
|---|---|---|---|---|
| 1 | §13, H2 | the interaction term "rises **later** and overtakes" claims-alone | it overtakes at $t=2$, the earliest step §10.1 permits, in 250/250 seeds — and at **every** depth in the fine sweep, so the phase language has no regime anywhere | H2 recorded as a claim about **composition** (5.94:1 endogenous over exogenous, 62% surviving withdrawal), not about phases; §1.2 now says the claim is an apportionment, not a chronology |
| 2 | §13, H1 | `hub` "degenerates to `random` where degrees are even" | at degree s.d. 1.00 it beats `random` by up to 14.8×, and the `fixed_random` control recovers 45–100% of that with no degree signal at all | §7.1 rewritten: four repertoires, with the schedule identified as the operative difference and the control defined to separate it from degree |
| 3 | §13, H1 | "reach dominates depth above a threshold" | true, but only above a **depth** gate: below $\alpha_D(1-\bar b)\approx\epsilon$ no reach ignites anything | Keep the clause, add the precondition. The gate is the sharpest structure in the whole study and deserves to be stated, not discovered |
| 4 | §13, H1 | ignition is amplifying, $\Pi>\rho_D$ "across the usable range" | true of `hub`, `base` and `fixed_random`, false of `random` at every reach | Qualified: amplification is a property of a **stable audience**, not of claims-making as such |
| 5 | §13, H3 | two branches, pre-registered | neither occurs: every configuration raises $\Pi$ for 9–24 steps and then lowers it | Record the third outcome. The pre-registration did its job — it is what makes "neither branch" reportable rather than a post-hoc story |

### Structural — a definition or a constant does not behave as described

| # | Where | Problem | Fix |
|---|---|---|---|
| 6 | §10.3 | The handover criterion (interaction > claims-alone, held $W_h$ steps) is **degenerate after withdrawal**: once claims-alone $\to0$ it is satisfied trivially. Under the polarized regime it fires at $t_{\text{off}}+1$, which is an artifact and not a handover | Guarded to the entrepreneur's own window, in spec and code. Testing it exposed a **second** defect — it is a ratio test and fires on a ratio between two near-zero quantities, e.g. at $\alpha_D=0.55$ where $\Pi=0.045$ — so §10.3 now requires it be read beside a level |
| 7 | §3.3, C3 | "At mean degree 10 and $\gamma=3$ this puts the boundary near $\mu+\delta\approx0.7$" — but four simplex points with $\mu+\delta\le0.60$ fail the measured probe, all near the $\delta$ vertex | The boundary is a **surface in the simplex**, not a value of $\mu+\delta$: an amplifying neighbour enters at weight $\gamma$, so the relevant scale is nearer $\mu+\delta\gamma$. Say so, and keep the instruction to measure it at every reported point |
| 8 | §3.2 | $\zeta$ "belongs to no hypothesis; its only role is to prevent structurally frozen states" | At $\sigma=0$ the permanence of division **is** the frozen state $\zeta$ prevents, so $\zeta$ competes with $\omega$ to explain persistence exactly as $\sigma$ does ($\Pi(399)$: 0.213 at $\zeta=0$, 0.178 at 0.01, 0.024 at 0.05). Either justify the default explicitly or add $\zeta$ to §12.2 |
| 9 | §14.2 (1) | asks for "a soft $\tanh$ bound" | Plain $\tanh$ is a bound **and** a contraction ($\tanh x<x$ for $x>0$), so it drives every position to zero with no forcing at all — a restoring force, the same pathology §3.2 identifies in $\sigma$. Specify a bound that is the **identity away from the poles** |
| 10 | §13, H2 | "low tolerance $\epsilon$ brings the handover forward" — but there is no gradient: the handover sits at its floor for every $\epsilon\le0.5$ and never occurs for $\epsilon\ge0.7$ | $\epsilon$ is the same gate as depth seen from the other side, $\epsilon\approx\alpha_D(1-\bar b)$. Stated once as a pair |
| 11 | §12.1 | seeds "chosen from a pilot so that the Monte Carlo standard error of panic incidence falls below a stated tolerance (e.g. ±0.03, requiring roughly 250–300 seeds)"  — 20 seeds gave s.e. up to ±0.11 | Re-run at **250 seeds**, s.e. ≤ ±0.032. §12.1 now states what the tolerance binds on: incidence needs 250, the continuous quantities were settled at 20 — every point estimate matched the pilot to within 0.01 |

Items 1–5 changed what the paper claims. Items 6–10 changed how it measures. Item 11 changed
how confident it is allowed to sound. Seven further edits followed from the runs and are
listed at the end of §5.

---

## 3. Code: done

All four items are closed.

**(a) The handover guard.** `CounterfactualResult.handover_step` now defaults to the
entrepreneur's own `active_until` and evaluates only inside it. Verification check **P9**
pins the bug it fixes: unguarded, the criterion fires at $t_{\text{off}}+1$ in the polarized
regime purely because claims-alone has reached zero; guarded, it declines. A second defect
surfaced while testing it — the criterion is a *ratio* test and fires on a ratio between two
near-zero quantities — and is recorded in §10.3 of the spec and in
[H2 §2.4](H2_handover.md).

**(b) `fixed_random`.** Implemented with a nested, seed-derived audience shared across the
four arms; verification check **P8** pins all three properties. It answered the question it
was built for, and the answer is more interesting than either candidate: **schedule** is worth
up to 7.0× and accounts for all of `hub`'s advantage at $\rho\ge0.30$; **degree** is worth a
further 2.2–2.5× below $\rho=0.10$ and nothing above $\rho=0.25$. Both channels are real and
they operate in different regimes ([H1 §2.3](H1_ignition.md)).

**(c) Empirical networks.** `ego-Facebook` and `ca-GrQc` retrieved with provenance records,
and the appendix row run with all three generators matched to each and the C3 probe repeated
per row ([appendix](appendix_robustness.md) §2). The result justified taking two rather than
one: at $\langle k\rangle=43.7$ topology decides nothing, at $\langle k\rangle=5.5$ it
decides a factor of twenty in what survives withdrawal, and no generator reproduces the sparse
empirical graph.

**(d) Housekeeping.** `sobol_indices` now returns a `reliable` flag and marks the $\Pi(399)$
row False automatically. The asynchronous sweep remains a Python loop; it is fast enough for
the three seeds the appendix needs.

Verification stands at **14/14**.

## 4. Compute: done

| | Run | Outcome |
|---|---|---|
| 1 | Headline cells at 250 seeds | Done — 59 875 + 9 540 + 2 250 counterfactual sets, 53 min. Incidence now carries s.e. ≤ ±0.032, the §12.1 tolerance. Every point estimate matched the 20-seed pilot to within 0.01 |
| 2 | `fixed_random` × topology × reach | Done — see §3(b) |
| 3 | Empirical networks + matched generators + C3 | Done — see §3(c) |
| 4 | Fine depth sweep around the gate | Done — **the phase language has no regime.** The handover step is 2 at every depth at which it occurs; the transition band $0.62<\alpha_D<0.68$ is bistable across seeds but never graded in *timing* |
| 5 | $\zeta$ as a fourth Sobol input | Done, over two boxes, and **it did not confirm what the bracket suggested.** Over $\zeta\in[0,0.02]$ the alarm split carries $S_T=1.00$ against 0.02 for noise; over $\zeta\in[0,0.05]$ the ordering **reverses**, 0.39 against 0.75. H2's persistence claim now carries a stated scope condition, $\zeta\lesssim0.02$, instead of an assumption. This was the seam worth closing, and closing it made the claim narrower and more defensible rather than stronger |

## 5. When this is finished

**Implementation.**
- [x] Every mechanism of §2–§11 in code, with each module naming the sections it implements
- [x] `run_verification.py` passes all five limiting cases and every property check (**14/14**)
- [x] Both artifact checks of §14.2 implemented and run
- [x] All four appendix replications of §12.3 implemented and run
- [x] §12.2 runnable without optional dependencies, estimator docked against a known function
- [x] The handover guard
- [x] `fixed_random`

**Evidence.**
- [x] Each of H1, H2, H3 has a verdict on every clause, with the disconfirmations stated
- [x] Every reported cell carries its C3 probe, its $\max_t\bar a^{\varnothing}$ and its $\bar\Phi(0)$
- [x] Results reported over a grid of the panic criterion rather than at one cut
- [x] The counterfactual-validity horizon computed, with a rule for what may be read past it
- [x] Headline cells at the seed count §12.1 asks for
- [x] Two empirical networks, with provenance

**Specification.**
- [x] The eleven corrections folded into `model_simplified.md`, plus eleven more the runs turned up
- [x] H1, H2 and H3 left as registered, each followed by a *Registered outcome* table recording which clauses held and which failed — the disconfirmations are results, and rewriting the hypotheses to match the findings would have destroyed them

**Reproducibility.**
- [x] One seed reproduces one trajectory bit-for-bit; asserted in code, not assumed
- [x] Every figure regenerable from the specification and the deposit alone
- [x] Every number in the reports generated by `make_report_tables.py`, not transcribed
- [x] The empirical edge lists archived with SHA-256 provenance records

**The list is closed, with nothing left open.** The last box — $\zeta$ in the Sobol design —
was the one worth spending compute on, and it changed the result: H2's persistence claim is
now conditional on $\zeta\lesssim0.02$ rather than unconditional. Nothing outstanding requires
a new mechanism, a new measurement or a redesign, which was the condition for calling the
model finished rather than merely working.

**One methodological point is worth recording for its own sake.** Three of the most
consequential findings came from checks the specification demanded on itself rather than from
the experiments: the C3 audit, without which the simplex scan would have confirmed H2 for the
wrong reason; the $\sigma$ caution; and the $\zeta$ analysis, which narrowed H2's strongest
claim. A fourth, the soft-bound correction, came from implementing an artifact check badly
enough to notice. The self-verification apparatus of §12.3 and §14.2 earned more than the
headline experiments did.

### What changed in the specification

Eighteen edits, in three classes. **Mechanisms and definitions** were corrected in place:
§3.2 ($\zeta$ is not inert), §3.3 (the C3 boundary is a surface in the simplex, not a value of
$\mu+\delta$), §7.1 (four repertoires, and the schedule is the operative difference), §10.3
(the handover guard, and the ratio-versus-level caveat), §14.2 (the soft bound must be the
identity away from the poles — plain $\tanh$ is a contraction), §15 (two quantities derived
from the seed rather than from a stream). **Scope and design** were extended: §4 and §12.3
(two empirical networks, bracketing the operating degree), §12.1 (the $\alpha\times\rho$ grid
and the fixed-audience control), §12.2 (what the seed tolerance actually binds on).
**Predictions** were left standing and answered: §1.2 (the claim is an apportionment, not a
chronology), §1.4 (containment is reproduced three ways, and amplification belongs to
stable-audience repertoires rather than to claims-making as such), and the three *Registered
outcome* tables in §13, now headed by a note directing any write-up to the tables rather than
to the registered wording.

Three later edits followed from the final runs. §3.2 and §12.2 carry $\zeta$ as a fourth
Sobol input with a measured scope condition in place of a three-point bracket. §10.3 demotes
the handover time from "the primary quantity for H2" to a supporting one and promotes the
**composition ratio** in its place, on the evidence that the handover's answer is the same
constant everywhere it is defined. And §13 gained the reading note above.

## 6. What is deliberately *not* on the list

Each of these would be a different paper, and §14.1 already says so. Recording them here so
that "the model is finished" is not confused with "the model is complete".

**Network rewiring.** The most consequential omission, and the reason repulsion is excluded
too: on a static graph, active repulsion and structural sorting cannot be told apart. The
model under-represents divergence rather than mis-attributing it, which is the safe direction.

**A reassurance channel.** H3's finding that defense lowers alarm only by total conversion is
conditional on the absence of any message that says *there is no threat* (§14.1). An actor
with a signed effect on alarm is the named test, and it would change H3's reading. It should
not be added quietly as a robustness check; it is a different model.

**An algorithm, institutional legacy, exit and silence, learning claims-makers, planted
community structure.** All named in §14.1. Each is a real feature of real panics and none is
needed for the claim of §1.2.

The line between §5 and §6 is exactly this: §5 is everything required for the current claims
to be sound, §6 is everything required for larger claims. Finishing §5 is what lets the paper
be written.
