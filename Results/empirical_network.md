# The empirical networks — what they show and what they license

**Spec §4 and §12.3. Two public graphs, each with the three synthetic generators re-run at its
own realised size and mean degree. 10 seeds per row, four runs per seed; produced by
`../Code/run_appendix.py --only empirical`, tabulated in
[`appendix_robustness.md`](appendix_robustness.md) §2.**

---

## 1. The graphs, and why these two

| Key | Source | $N$ | $\langle k\rangle$ | $C$ | components | isolates |
|---|---|---|---|---|---|---|
| `ego-facebook` | SNAP, Leskovec & McAuley (2012) — ten merged Facebook friendship circles | 4 039 | 43.69 | 0.606 | 1 | 0% |
| `ca-grqc` | SNAP, Leskovec, Kleinberg & Faloutsos (2007) — arXiv GR-QC co-authorship | 5 241 | 5.53 | 0.530 | 354 | 0% |

Retrieved 2026-08-04 by `../Code/fetch_empirical_network.py`, which records the URL, dataset
page, citation, retrieval date, SHA-256 and realised structure in a `*.provenance.json`
alongside each edge list. Both realised sizes are one node and a few edges below the published
figures because self-loops are removed on load.

**Two rather than one, and deliberately.** The spec asks for "one empirical network". One
cannot support the claim the appendix needs, because any single graph differs from the
generators in size, density *and* clustering at once, and the three are then inseparable.
These two **bracket the operating point of $\langle k\rangle=10$ from both sides** — 5.53 and
43.69 — which turns a single comparison into a gradient. That decision paid for itself: the
answer at one end of the bracket is the opposite of the answer at the other.

Each graph is accompanied by Watts–Strogatz, Holme–Kim and Erdős–Rényi re-run at *its* $N$ and
$\langle k\rangle$, so a structure effect is never confounded with a density effect (§4). The
C3 sub-criticality probe was repeated on all eight rows and all eight pass, which matters
because the reinforcement boundary moves with mean degree.

---

## 2. The result

| Graph | topology | $C$ | comp. | $\Pi(149)$ | $\Pi(399)$ | $q(149)$ | handover |
|---|---|---|---|---|---|---|---|
| **ca-GrQc** ⟨k⟩=5.5 | empirical | 0.530 | 354 | 0.232 ± 0.004 | **0.135 ± 0.011** | 0.229 | 5 |
| | Watts–Strogatz | 0.439 | 1 | 0.268 ± 0.006 | 0.100 ± 0.027 | 0.271 | 3 |
| | Holme–Kim | 0.268 | 1 | 0.270 ± 0.009 | 0.072 ± 0.061 | 0.273 | 3 |
| | Erdős–Rényi | 0.001 | 23 | 0.244 ± 0.009 | **0.006 ± 0.001** | 0.251 | 3 |
| **ego-Facebook** ⟨k⟩=43.7 | empirical | 0.606 | 1 | 0.238 ± 0.009 | 0.191 ± 0.007 | 0.240 | 2 |
| | Watts–Strogatz | 0.534 | 1 | 0.230 ± 0.005 | 0.198 ± 0.004 | 0.233 | 2 |
| | Holme–Kim | 0.104 | 1 | 0.227 ± 0.010 | 0.197 ± 0.009 | 0.229 | 2 |
| | Erdős–Rényi | 0.011 | 1 | 0.227 ± 0.003 | 0.198 ± 0.002 | 0.230 | 2 |

Three readings follow, in increasing order of how much they change the paper.

### 2.1 Magnitude is a parameter property, not a structural one

Across all eight rows — two empirical graphs, three generators each, mean degree varying
eight-fold — **$\Pi$ at withdrawal lies between 0.227 and 0.270**, and the share of the
population amplifying lies between 0.229 and 0.273. The episode the model produces *while an
entrepreneur is acting* is essentially set by $(\epsilon,\alpha_D,\rho_D,\omega)$ and barely
notices what graph it is running on.

This is a stronger invariance than the appendix was designed to test, and it is worth stating
positively: the ignition results of H1 are not artifacts of the three generators. It also
sharpens what H1's topology clause was ever about — topology decides *which repertoire* works
(H1 §2.2, where `hub`'s peak varies 0.386–0.475 across generators), not how large the episode
becomes once one does.

### 2.2 Persistence is a structural property, and at low density it tracks clustering

At $\langle k\rangle=43.7$ structure decides nothing: all four rows land at
$\Pi(399)=0.191$–$0.198$ and are statistically indistinguishable. At $\langle k\rangle=5.5$ it
decides almost everything, and the spread is a factor of twenty. More than that, the ordering
is **monotone in clustering**:

| $C$ | 0.530 (ca-GrQc) | 0.439 (WS) | 0.268 (HK) | 0.001 (ER) |
|---|---|---|---|---|
| $\Pi(399)$ | 0.135 | 0.100 | 0.072 | 0.006 |

Sparse *and* unclustered is the one combination in which manufactured division does not
survive withdrawal at all. The mechanism is legible from §7.2: bounded confidence carves the
population into clusters, and a cluster holds only if its members reinforce each other's
positions faster than noise walks them back across the tolerance boundary. Triangles supply
that reinforcement. With mean degree 5.5 and no triangles, the clusters are too thin to hold
and they re-merge — which is the same failure mode the $\zeta$ analysis identifies
parametrically (§3.2), reached here structurally instead.

**This is a genuine prediction and it is new.** *Local density is what makes manufactured
division permanent.* Two societies with identical claims-making, identical tolerance and
identical alarm parameters will differ in whether the panic outlives the campaign, according
to how clustered their social ties are.

### 2.3 Why topology stops mattering at high density

The convergence at $\langle k\rangle=43.7$ is not a null result to be passed over; it has a
mechanism, and the mechanism predicts the gradient in §2.2.

With $N=4039$ and $\langle k\rangle=43.7$ each agent's neighbourhood is a sample of roughly 1%
of the population, and — crucially — a sample large enough that every agent's neighbourhood
resembles every other agent's. Othering exposure $\Phi_i$, an average over that neighbourhood,
therefore concentrates around its population mean, and the differences between topologies wash
out. The model becomes self-averaging. As the graph gets sparser, neighbourhoods stop being
representative, $\Phi_i$ acquires real variance across agents, and topology re-enters — which
is exactly the ordering §2.2 shows.

An alternative explanation is available and I did **not** separate it: at high degree the cap
inside $E_i$ (§7.4) may bind more often, saturating alarm exposure and flattening differences.
Distinguishing self-averaging from cap saturation would need a counter on how often the cap
binds, which is not instrumented. The self-averaging account is the more parsimonious and it
predicts the low-density gradient, which the saturation account does not — but this is
reasoning, not measurement, and should be labelled as such if it goes into the paper.

### 2.4 Two smaller observations

**The handover is 5 on ca-GrQc, and this is the only place in the entire study where it
exceeds 2 under an active campaign.** Everywhere else — every depth, every tolerance, every
topology at the operating density — the interaction overtakes claims-alone at $t=2$, the first
step §10.1 permits. On a sparse, highly clustered, many-component graph it takes five. The
effect is small and it does not rescue H2's phase language, but it identifies where to look if
that language is ever to be rescued: **sparsity, not depth.**

**Bimodality and retained disproportion do not co-move, and the discrepancy is unexplained.**
ca-GrQc has the *lowest* interior bimodality of its four rows (0.845 against Watts–Strogatz's
0.980) and the *highest* retained $\Pi$. Whatever is holding alarm up on the empirical graph is
not simply "the population is more polarized". Its 354 components are the obvious suspect —
small disconnected groups can hold positions that a connected graph would average away, and
they contribute to $\Phi_i$ locally without registering as a clean two-mode split globally —
but this was not tested and should not be asserted.

---

## 3. What the empirical networks license, and what they do not

**They license:** the claim that the H1–H3 results are not artifacts of the three synthetic
generators, and the claim in §2.2 that persistence depends on clustering at low density —
which no generator would have produced, since none of them reaches $C=0.53$ at
$\langle k\rangle=5.5$.

**They do not license anything empirical about moral panic.** Five limits, in order of how
easily they are mistaken for something weaker.

**(i) The graphs enter as fixed structure only (§9).** Node attributes, edge direction, weights
and timestamps are all discarded; every agent's position, alarm and threshold is drawn exactly
as in §8. Nothing about these datasets' actual content touches the model. An "empirical
replication" here means *the adjacency matrix came from the world*, and no more.

**(ii) Neither graph is a moral-communication network.** The model's edges mean "who hears whom
about a contested issue". ca-GrQc's mean "who co-authored a general-relativity paper with
whom"; ego-Facebook's mean "who accepted whose friend request". There is no reason to think
either is the graph along which moral disagreement travels, and every reason to think the
relevant graph is denser in some places and sparser in others than these are.

**(iii) ego-Facebook is a merged ego-network, which is a peculiar sampling design.** It is ten
egos' complete neighbourhoods stitched together. Complete neighbourhoods are unusually
clustered by construction, so its $C=0.606$ is inflated relative to a random sample of the same
friendship graph, and its mean degree of 43.7 reflects the sampling rather than a typical
person's friend count. Its role in the bracket is as a *dense, highly clustered* graph, and it
plays that role honestly; it is not a sample of Facebook.

**(iv) ca-GrQc is a co-authorship network, not a friendship graph.** It was chosen to bracket
the operating degree from below and for its 354 components — the case that exercises the
model's deliberate choice to run on the full graph rather than the giant component (§4). It is
not a better instance of the type the spec asks for; it is a useful instance of *low density
with high clustering*, which no generator supplies.

**(v) Both are static snapshots, and so is the model.** This is consistent rather than
convenient, but it means the empirical graph is doing no work a fixed synthetic graph could not
do. Real panics rewire the social world (§14.1); neither these data nor this model represent
that, and the appendix cannot speak to it.

---

## 4. What would make this an empirical test

Nothing in this appendix is a test of the model against the world; it is a robustness check
against a wider class of graphs than three generators supply. Three things would be needed to
change that, in ascending order of difficulty.

**A network of moral communication.** Ties that carry disagreement about a contested issue —
discussion networks, reply graphs on a specific controversy — rather than co-authorship or
friendship. These exist and are obtainable.

**Observed positions on the contested issue**, so that $b_i(0)$ is measured rather than drawn
from §8's Uniform$[-0.2,0.2]$. Panel survey data attached to a discussion network would do it.
This is where an empirical version of the model would begin, and note what it costs: the
consensual initial regime is what makes the interaction term interpretable (§10.1), so a
measured $b_i(0)$ would put most real populations into the *attenuated* polarized case rather
than the clean consensual one.

**An external threat referent.** This is the one that cannot be bought with better data.
$\Pi$ measures excess over the model's own counterfactual, not over real danger (§14.1). Even
with a real network, real positions and a real campaign, the model would say how much alarm
exceeded what the same population would have felt without the claims-making — not how much
exceeded what the situation warranted. The disproportionality criterion is made *computable*
here, not *decidable*.
