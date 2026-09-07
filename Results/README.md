# Results

Hypothesis tests for the agent-based model specified in
[`../model_simplified.md`](../model_simplified.md), run against the reference
implementation in [`../Code/`](../Code/).

| File | Contents |
|---|---|
| [`H1_ignition.md`](H1_ignition.md) | Experiment A — ignition. Ten clauses, verdict each, figure commentary, interpretation, discussion |
| [`H2_handover.md`](H2_handover.md) | Experiment B + the §12.2 sensitivity design — handover |
| [`H3_defense.md`](H3_defense.md) | Experiment C — counter-claims-making |
| [`appendix_robustness.md`](appendix_robustness.md) | The §12.3 appendix replications on two empirical networks, and the §14.2 artifact checks |
| [`empirical_network.md`](empirical_network.md) | The two empirical graphs interpreted — what they show, and what they do and do not license |
| [`limitations.md`](limitations.md) | Every scope condition, instrument limit, structural exclusion and scalability bound, with a transfer checklist |
| [`roadmap.md`](roadmap.md) | What remains in code, in the specification and in compute — and the condition for calling this finished |
| [`hypothesis_figures.ipynb`](hypothesis_figures.ipynb) | One figure per hypothesis, four panels each |
| [`make_presentation_figures.py`](make_presentation_figures.py) | Slide figures: the twelve panels of the three paper figures cut into separate files, plus nine expository figures. Writes `../Presentation/figures/` |
| `figures/` | The three figures at 300 dpi |
| `data/` | Raw output of `../Code/run_hypotheses.py` and `run_appendix.py`; the notebook reads these and does not re-simulate |

## Reproducing

```bash
cd Code && pip install -r requirements.txt && python run_verification.py
```

`14/14 checks passed` confirms the code implements the specification (spec §12.3). Then:

```bash
cd Code && python run_hypotheses.py --seeds 250
```

**54 minutes on 15 cores**: 72 990 counterfactual sets, i.e. 291 960 simulation runs. Writes
`Results/data/*.json`. Pass `--seeds 20` for a 4-minute pilot — every point estimate here
matched that pilot to within 0.01, and the 250 seeds buy only the incidence tables, whose
standard error they bring from ±0.11 to ±0.032 (spec §12.1).

Figures for the talk (seconds, reads `data/` and never re-simulates the sweeps):

```bash
cd Results && python3 make_presentation_figures.py
```

Writes `Presentation/figures/{panels,concepts}/` as PDF and PNG, plus headline-free
copies under `figures/untitled/` that `Presentation/Presentation_final.typ` uses, so a
slide heading and its figure never state the same claim twice.

```bash
cd Code && python fetch_empirical_network.py ego-facebook && python fetch_empirical_network.py ca-grqc && python run_appendix.py --seeds 10
```

About 10 minutes: the §12.3 appendix replications and the §14.2 artifact checks. The downloads
write provenance records (URL, retrieval date, SHA-256, realised structure); the empirical
block is skipped with a message if they are absent. `run_appendix.py` **merges** into
`appendix.json`, so `--only <block>` refreshes one block and leaves the rest standing.

```bash
cd Code && python make_report_tables.py all
```

Regenerates every table in the three reports, in Markdown, from the JSON. Re-running it after
a re-run is the check that the reports have not drifted from the data.

## Operating point

Small world (Watts–Strogatz, $p=0.1$), $N=1000$, mean degree 10; $\epsilon=0.5$, $\mu=0.30$,
$\delta=0.25$, $\omega=0.35$; $\sigma=0$, $\gamma=3$, $\zeta=0.01$; entrepreneur on `base`
with $\alpha_D=0.7$, $\rho_D=0.25$, withdrawing at $t_{\text{off}}=150$; $T=400$; seeds 11–260.

Conditioning, recorded per run as spec §3.3 and §10.2 require: the C3 sub-criticality probe
passes ($\mu+\delta=0.55$, resting mean alarm $4\times10^{-53}$), $\max_t\bar
a^{\varnothing}=0.0515$ so the panic-index denominator stays in $[0.948,1]$, and
$\bar\Phi(0)=0.0672$ against the $\approx0.07$ the spec predicts for the consensual regime.

## Headline verdicts

| | Verdict |
|---|---|
| **H1** | Supported with two corrections. Amplification ($\Pi>\rho_D$) holds for every repertoire with a stable audience and never for `random`; ignition is smooth, not discontinuous; broadcast is self-limiting. `hub` does **not** degenerate to `random` on near-regular graphs, and the `fixed_random` control splits the reason: **schedule** is worth up to 7.0× and accounts for all of `hub`'s advantage above $\rho=0.30$; **degree** adds a further 2.2–2.5× below $\rho=0.10$ and nothing above 0.25. Depth is a **gate** and only then does reach dominate. |
| **H2** | Supported, with the ordering clause refuted and a scope condition on the strongest claim. The interaction runs 5.94× claims-alone and 62% of $\Pi$ survives 250 steps after withdrawal — but it overtakes at $t=2$, the earliest step §10.1 permits, **at every depth tested**, so the phase language has no regime. Persistence is maximised exactly at the $\omega$ vertex and the split carries $S_T=0.99$ against 0.03 for intensity — but the four-input design shows that holds only for $\zeta\lesssim0.02$; at five times the default noise, position noise out-explains the split 0.75 to 0.39. Both results need the C3 audit: 4 of 45 simplex points are supercritical and carry the highest raw persistence. |
| **H3** | Both pre-registered branches refuted. Every configuration raises $\Pi$ for 9–24 steps and then lowers it — a sequence, not a sign. The largest overshoot (+61%) belongs to the *lowest-reach* configuration, which is H3's own second channel. The reduction is total conversion, not reassurance, and leaves a permanent floor of $0.18\rho_C$. |

Each file states the limits its verdict rests on. Two that applied throughout are now
resolved. Seed counts meet the spec: at 250 seeds the standard error on incidence is ≤ ±0.032,
so the incidence tables are rates and not merely shapes. And the boundary artifact of §14.2
has been checked and **cleared** — the interior bimodality coefficient agrees with the raw one
to three decimals, and replicating under a bound that never pins anyone leaves $\Pi$ within
0.008, so the polarization these runs report is emergent, not pile-up.

Two limits are *not* resolved, and both are stated rather than hidden. The
counterfactual-validity horizon (§14.2) is reached between $t=191$ and $t=289$ in three of
five audited seeds, so late-run quantities such as $\Pi(399)$ are reported as distributions
over seeds and never as trajectories. And H2's persistence claim holds only for
$\zeta\lesssim0.02$ — a scope condition the model cannot itself settle, since how noisy moral
positions are is an empirical question.

## Specification coverage

Everything the specification names is now implemented and verified: §2–§11 in full; §12.1
experiments A/B/C including the $\alpha_D\times\rho_D$ grid; §12.2 with a self-contained
Saltelli/Jansen Sobol analysis (no SALib required, estimator docked against Ishigami to
0.0025); §12.3's five verification limits, seven property checks and all four appendix
replications; §10.2's grid over $(\Pi^*,q^*,W)$; and both artifact checks of §14.2.

Nothing remains. The two items open at the previous pass — the empirical network and the
handover guard — are closed, and the eleven statements in `model_simplified.md` the runs
contradicted have been corrected, along with seven further edits the runs turned up.

The hypotheses in §13 were **not** rewritten to match the findings. Each stands as registered,
followed by a *Registered outcome* table recording which clauses held and which failed;
rewriting predictions into descriptions would have destroyed the evidential value of both, and
the H3 result in particular means something only because two branches were fixed in advance
and neither occurred. [`roadmap.md`](roadmap.md) records the whole gap and its closure.
