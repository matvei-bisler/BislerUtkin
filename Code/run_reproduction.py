#!/usr/bin/env python3
"""Reproduce the pilot results claimed in README.md from the specification alone.

    python run_reproduction.py [n_seeds]

Five exercises, each printing one table over `n_seeds` seeds (default 10), so
every number is a distribution over seeds and never a single run (spec §10.3):

  1. Amplification and containment (spec §1.4, patterns 1-2; H1).
     Pi at withdrawal vs reach rho, in both exposure modes. The reinforcing
     mode must amplify (Pi/rho > 1 somewhere) and the proportional mode must
     not, which is the reason the count denominator is load-bearing (§7.4).
  2. Broadcast is self-limiting (H1). The interaction term against rho: it
     must peak at intermediate reach and collapse toward zero at rho = 1.
  3. Alarm outlives its cause (spec §1.4, pattern 3; H2). Persistence after
     withdrawal against omega at fixed mu + delta: zero-floor decay at
     omega = 0, positive floor at omega > 0.
  4. Handover (H2): the step at which the interaction term overtakes
     claims-alone, at the headline setting.
  5. Conditioning: max_t of the null run's mean alarm (spec §10.2) and the
     C3 sub-criticality probe (spec §3.3) at the operating point.
  6. The anchor dissolves manufactured division (spec §3.2): persistence
     tracks the anchor's relaxation time -1/ln(1-sigma), not omega, which is
     why sigma = 0 at the operating point.

Settings follow the README pilot: small world, N = 600, mean degree 10,
epsilon = 0.5, mu = 0.30, delta = 0.25, alpha = 0.7, `base` repertoire,
withdrawal at t_off = 150, T = 400.
"""

from __future__ import annotations

import sys
from dataclasses import replace

import numpy as np

from moralpanic import (
    Constants,
    ExposureMode,
    NetworkSpec,
    Parameters,
    Repertoire,
    RunConfig,
    Topology,
    entrepreneur,
    run_counterfactual_set,
)
from moralpanic.counterfactual import is_subcritical

T_OFF = 150
N_STEPS = 400
NETWORK = NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=600, mean_degree=10.0)
OPERATING = dict(epsilon=0.5, mu=0.30, delta=0.25)
ALPHA = 0.7


def config(
    rho: float,
    omega: float = 0.35,
    exposure_mode: ExposureMode = ExposureMode.REINFORCING,
    seed: int = 11,
) -> RunConfig:
    return RunConfig(
        seed=seed,
        n_steps=N_STEPS,
        network=NETWORK,
        parameters=Parameters(omega=omega, **OPERATING),
        actor_d=entrepreneur(
            alpha=ALPHA, rho=rho, repertoire=Repertoire.BASE, active_until=T_OFF
        ),
        exposure_mode=exposure_mode,
    )


def over_seeds(seeds, make_config):
    return [run_counterfactual_set(make_config(seed)) for seed in seeds]


def mean_sd(values) -> str:
    values = np.asarray(values, dtype=float)
    return f"{values.mean():6.3f} +/- {values.std(ddof=1):5.3f}"


def persistence_summary(results, t_off: int = T_OFF) -> str:
    entries = [r.persistence(t_off) for r in results]
    censored = sum(e["censored"] for e in entries)
    durations = [e["duration"] for e in entries]
    if censored == len(entries):
        return f"all censored at {int(np.min(durations))}+"
    shown = np.median([e["duration"] for e in entries if not e["censored"]])
    return f"median {shown:.0f} ({censored}/{len(entries)} censored)"


def main() -> int:
    n_seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seeds = list(range(11, 11 + n_seeds))
    at = T_OFF - 1  # the last step with the entrepreneur still active

    print(f"Reproduction over {n_seeds} seeds; four runs per seed (spec §10.1).")
    print(f"Operating point {OPERATING}, alpha={ALPHA}, base repertoire, "
          f"t_off={T_OFF}, T={N_STEPS}.\n")

    # -- 1. Amplification and containment ---------------------------------- #
    print("1. Amplification (Pi at withdrawal vs rho; spec §1.4 patterns 1-2)")
    print(f"   {'rho':>5} | {'Pi(149) reinforcing':>22} | {'Pi/rho':>6} | "
          f"{'Pi(149) proportional':>22} | {'Pi/rho':>6}")
    for rho in (0.05, 0.10, 0.20, 0.40):
        reinf = over_seeds(seeds, lambda s, r=rho: config(r, seed=s))
        prop = over_seeds(
            seeds,
            lambda s, r=rho: config(r, exposure_mode=ExposureMode.PROPORTIONAL, seed=s),
        )
        pi_r = [r.decomposition.panic_index[at] for r in reinf]
        pi_p = [r.decomposition.panic_index[at] for r in prop]
        print(f"   {rho:5.2f} | {mean_sd(pi_r):>22} | {np.mean(pi_r)/rho:6.2f} | "
              f"{mean_sd(pi_p):>22} | {np.mean(pi_p)/rho:6.2f}")
    print()

    # -- 2. Broadcast is self-limiting -------------------------------------- #
    print("2. Interaction vs reach (broadcast self-limiting; H1)")
    print(f"   {'rho':>5} | {'interaction(149)':>18} | persistence after t_off")
    for rho in (0.05, 0.10, 0.25, 0.40, 0.70, 1.00):
        results = over_seeds(seeds, lambda s, r=rho: config(r, seed=s))
        inter = [r.decomposition.interaction[at] for r in results]
        print(f"   {rho:5.2f} | {mean_sd(inter):>18} | {persistence_summary(results)}")
    print()

    # -- 3. Persistence is governed by omega -------------------------------- #
    print("3. Persistence vs omega at fixed mu + delta (H2; spec §1.4 pattern 3)")
    print(f"   {'omega':>5} | {'Pi(149)':>16} | {'Pi(299)':>16} | persistence")
    omega_results = {}
    for omega in (0.00, 0.20, 0.35, 0.45):
        results = over_seeds(seeds, lambda s, w=omega: config(0.25, omega=w, seed=s))
        omega_results[omega] = results
        pi = np.array([r.decomposition.panic_index for r in results])
        print(f"   {omega:5.2f} | {mean_sd(pi[:, at]):>16} | "
              f"{mean_sd(pi[:, 299]):>16} | {persistence_summary(results)}")
    print()

    # -- 4. Handover --------------------------------------------------------- #
    print("4. Handover: interaction overtakes claims-alone (H2; spec §10.3)")
    handovers = [r.handover_step() for r in omega_results[0.35]]
    reached = [h for h in handovers if h is not None]
    print(f"   at omega=0.35, rho=0.25: handover in {len(reached)}/{n_seeds} seeds"
          + (f", median step {np.median(reached):.0f}" if reached else ""))
    print()

    # -- 5. Conditioning ------------------------------------------------------ #
    print("5. Conditioning of the operating point")
    peaks = [r.null_peak() for r in omega_results[0.35]]
    print(f"   max_t null-run mean alarm (spec §10.2): "
          f"{max(peaks):.4f} over all seeds (must stay below 0.1)")
    probe = is_subcritical(config(0.25, seed=seeds[0]))
    print(f"   C3 probe (spec §3.3): subcritical={probe['subcritical']}, "
          f"resting mean alarm {probe['resting_mean_alarm']:.4f} "
          f"at mu+delta={probe['mu_plus_delta']:.2f}")
    print()

    # -- 6. The anchor dissolves manufactured division ----------------------- #
    print("6. Persistence vs sigma (the anchor caution of spec §3.2)")
    print(f"   {'sigma':>5} | {'-1/ln(1-sigma)':>14} | persistence")
    sigma_seeds = seeds[: min(3, n_seeds)]
    for sigma in (0.00, 0.05, 0.10, 0.20):
        results = over_seeds(
            sigma_seeds,
            lambda s, g=sigma: replace(
                config(0.25, seed=s), constants=Constants(sigma=g, gamma=3.0, zeta=0.01)
            ),
        )
        predicted = "inf" if sigma == 0.0 else f"{-1.0 / np.log(1.0 - sigma):.1f}"
        print(f"   {sigma:5.2f} | {predicted:>14} | "
              f"{persistence_summary(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
