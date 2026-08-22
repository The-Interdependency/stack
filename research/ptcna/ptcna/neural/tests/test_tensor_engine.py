import numpy as np
from ptcna.neural.tensor_engine import TensorState, MarkovRecursion


def test_markov_recursion_mass_conserved():
    actor = np.array([0])
    time = np.array([0])
    context = np.array([0])
    metric = np.ones((4,))  # metric with total mass 4
    state = TensorState(actor=actor, time=time, metric=metric.copy(), context=context)

    # injected and resolved have slight imbalance
    injected = np.array([0.1, 0.2, 0.3, 0.4])
    resolved = np.array([0.11, 0.19, 0.31, 0.39])  # net imbalance = 0.0 actually
    updater = MarkovRecursion(learning_rate=0.5)

    new_state = updater.update(state, injected, resolved)
    # after update we expect mass to be conserved (sum(metric) unchanged)
    assert abs(new_state.mass - state.mass) < 1e-9

    # test with a non-zero imbalance
    injected2 = np.array([0.1, 0.1, 0.1, 0.1])
    resolved2 = np.array([0.2, 0.1, 0.1, 0.1])  # imbalance = -0.1
    new_state2 = updater.update(state, injected2, resolved2)
    assert abs(new_state2.mass - state.mass) < 1e-9
