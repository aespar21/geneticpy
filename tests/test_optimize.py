from geneticpy import optimize
from geneticpy.distributions import *


def test_optimize_simple():
    def fn(params):
        loss = params['x'] + params['y']
        return loss

    param_space = {'x': UniformDistribution(0, 1),
                   'y': UniformDistribution(0, 1000000, 1000)}

    best_params, score = optimize(fn, param_space, size=200, generation_count=500, verbose=False)
    assert ['x', 'y'] == list(best_params.keys())
    assert best_params['x'] < 0.01
    assert best_params['y'] == 0
    assert score < 0.01


def test_optimize_complicated():
    def fn(params):
        loss_x = params['x']
        loss_y = 1 if 18 < params['y'] < 20 else 1000001
        loss_xq = params['xq']
        loss_c = params['c']
        loss = loss_x + loss_y + loss_xq + loss_c
        return loss

    param_space = {'x': UniformDistribution(0, 1),
                   'y': GaussianDistribution(100, 50, low=0),
                   'xq': UniformDistribution(0, 100, q=5),
                   'c': ChoiceDistribution([1000, 3000, 5000], [0.1, 0.7, 0.2])}

    best_params, score = optimize(fn, param_space, size=200, generation_count=500, verbose=False)
    print(best_params)
    print(score)
    assert ['x', 'y', 'xq', 'c'] == list(best_params.keys())
    assert best_params['x'] < 0.01
    assert 18 < best_params['y'] < 20
    assert 1000 == best_params['c']