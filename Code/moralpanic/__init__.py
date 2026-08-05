"""An agent-based model of moral entrepreneurship and moral panic.

A faithful implementation of `model_simplified.md`. Every module names the
specification sections it implements.

    config         parameters, constants, actor specs, initialization regimes (§3, §5, §8)
    rng            the three seeded streams (§8, §15)
    network        the three generators, matched on mean degree (§4)
    actors         the three claims-making repertoires (§7.1)
    model          the four update rules, synchronous (§6, §7)
    measures       per-step measurements (§10.3)
    counterfactual the 2x2 design, decomposition and panic index (§10.1, §10.2)
    sensitivity    simplex reparameterisation for Sobol (§12.2)
    verification   the five limiting cases and three property checks (§12.3)

Minimal use::

    from moralpanic import (
        Parameters, NetworkSpec, RunConfig, entrepreneur, run_counterfactual_set,
    )

    config = RunConfig(
        seed=1,
        n_steps=200,
        network=NetworkSpec(n_agents=1000, mean_degree=10.0),
        parameters=Parameters(epsilon=0.6, mu=0.3, delta=0.3, omega=0.3),
        actor_d=entrepreneur(alpha=0.6, rho=0.3),
    )
    result = run_counterfactual_set(config)
    print(result.decomposition.panic_index[-1])
"""

from .config import (
    ActorSpec,
    BoundMode,
    Constants,
    ExposureMode,
    NetworkSpec,
    Parameters,
    PositionRegime,
    Repertoire,
    RunConfig,
    SILENT_C,
    ThresholdRegime,
    Topology,
    UpdateOrder,
    counter_entrepreneur,
    entrepreneur,
)
from .counterfactual import (
    CounterfactualResult,
    Decomposition,
    counterfactual_validity,
    is_subcritical,
    run_counterfactual_set,
)
from .measures import (
    StepRecord,
    bimodality_coefficient,
    boundary_fraction,
    exposure_concentration,
    interior_bimodality_coefficient,
)
from .model import Model, RunResult, initialise
from .network import build_graph, load_edge_list, structural_summary
from .rng import Streams
from .sensitivity import (
    alarm_parameters,
    salib_problem,
    simplex_grid,
    sobol_design,
    sobol_indices,
    split_from_uniforms,
    validate_sobol_estimator,
)
from .verification import run_all as run_verification

__all__ = [
    "ActorSpec", "BoundMode", "Constants", "ExposureMode", "NetworkSpec", "Parameters",
    "PositionRegime", "Repertoire", "RunConfig", "SILENT_C", "ThresholdRegime", "Topology",
    "UpdateOrder", "counter_entrepreneur", "entrepreneur",
    "CounterfactualResult", "Decomposition", "counterfactual_validity", "is_subcritical",
    "run_counterfactual_set",
    "StepRecord", "bimodality_coefficient", "boundary_fraction", "exposure_concentration",
    "interior_bimodality_coefficient",
    "Model", "RunResult", "initialise",
    "build_graph", "load_edge_list", "structural_summary", "Streams",
    "alarm_parameters", "salib_problem", "simplex_grid", "sobol_design", "sobol_indices",
    "split_from_uniforms", "validate_sobol_estimator",
    "run_verification",
]

__version__ = "1.0.0"
