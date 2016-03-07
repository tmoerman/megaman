from __future__ import division ## removes integer division

import numpy as np
from nose import SkipTest
from numpy.testing import assert_array_almost_equal
from scipy.spatial.distance import pdist, squareform
from megaman.utils.testing import assert_raise_message
from megaman.geometry.adjacency import compute_adjacency_matrix
from megaman.geometry.laplacian import compute_laplacian_matrix
from megaman.geometry.affinity import compute_affinity_matrix
from megaman.geometry.geometry import *

def test_compare_adjacency_methods(almost_equal_decimals=5):
    """ compare the different adjacency methods """
    X = np.random.uniform(size=(20,2))
    D = squareform(pdist(X))
    radius = 1.
    D[D>radius]=0
    for adjacency_method in adjacency_methods:
        G = Geometry(adjacency_method = 'brute')
        G.set_data_matrix(X)
        d = G.compute_adjacency_matrix(radius=radius)
        assert_array_almost_equal(D, d.todense(), almost_equal_decimals)

def test_compute_adjacency_matrix_args(almost_equal_decimals=5):
    """ test the compute_adjacency_matrix parameter arguments """
    input_types = ['data', 'adjacency', 'affinity']
    params = [{'radius':1}, {'radius':2}]
    for adjacency_method in adjacency_methods:
        if adjacency_method == 'pyflann':
            try:
                import pyflann as pyf
            except ImportError:
                raise SkipTest("pyflann not installed.")
        X = np.random.uniform(size=(10, 2))
        D = compute_adjacency_matrix(X, adjacency_method, **params[1])
        A = compute_affinity_matrix(D, radius=1)
        for init_params in params:
            for kwarg_params in params:
                true_params = init_params.copy()
                true_params.update(kwarg_params)
                adjacency_true = compute_adjacency_matrix(X, adjacency_method, **true_params)
                G = Geometry(adjacency_method = adjacency_method, adjacency_kwds = init_params)
                for input in input_types:
                    G = Geometry(adjacency_kwds = init_params)
                    if input in ['data']:
                        G.set_data_matrix(X)
                        adjacency_queried = G.compute_adjacency_matrix(**kwarg_params)
                        assert_array_almost_equal(adjacency_true.todense(), adjacency_queried.todense(),
                                                  almost_equal_decimals)
                    else:
                        if input in ['adjacency']:
                            G.set_adjacency_matrix(D)
                        else:
                            G.set_affinity_matrix(A)
                        msg = distance_error_msg
                        assert_raise_message(ValueError, msg, G.compute_adjacency_matrix)

def test_compute_affinity_matrix_args(almost_equal_decimals=5):
    """ test the compute_affinity_matrix parameter arguments """
    input_types = ['data', 'adjacency', 'affinity']
    params = [{'radius':4}, {'radius':5}]
    adjacency_method = 'auto'
    for affinity_method in affinity_methods:
        X = np.random.uniform(size=(10, 2))
        D = compute_adjacency_matrix(X, adjacency_method, **params[1])
        A = compute_affinity_matrix(D, affinity_method, **params[1])
        for init_params in params:
            for kwarg_params in params:
                true_params = init_params.copy()
                true_params.update(kwarg_params)
                affinity_true = compute_affinity_matrix(D, adjacency_method,
                                                        **true_params)
                for input in input_types:
                    G = Geometry(adjacency_method = adjacency_method,
                                 adjacency_kwds = params[1],
                                 affinity_method = affinity_method,
                                 affinity_kwds = init_params)
                    if input in ['data', 'adjacency']:
                        if input in ['data']:
                            G.set_data_matrix(X)
                        else:
                            G.set_adjacency_matrix(D)
                        affinity_queried = G.compute_affinity_matrix(**kwarg_params)
                        assert_array_almost_equal(affinity_true.todense(), affinity_queried.todense(), almost_equal_decimals)
                    else:
                        G.set_affinity_matrix(A)
                        msg = affinity_error_msg
                        assert_raise_message(ValueError, msg, G.compute_affinity_matrix)

def test_compute_laplacian_matrix_args(almost_equal_decimals=5):
    input_types = ['data', 'adjacency', 'affinity']
    params = [{}, {'radius':4}, {'radius':5}]
    lapl_params = [{}, {'scaling_epps':4}, {'scaling_epps':10}]
    adjacency_method = 'auto'
    affinity_method = 'auto'

    for laplacian_method in laplacian_types:
        X = np.random.uniform(size=(10, 2))
        D = compute_adjacency_matrix(X, adjacency_method, **params[1])
        A = compute_affinity_matrix(D, affinity_method, **params[1])
        for init_params in lapl_params:
            for kwarg_params in lapl_params:
                    true_params = init_params.copy()
                    true_params.update(kwarg_params)
                    laplacian_true = compute_laplacian_matrix(A, laplacian_method, **true_params)
            for input in input_types:
                G = Geometry(adjacency_method = adjacency_method,
                             adjacency_kwds = params[1],
                             affinity_method = affinity_method,
                             affinity_kwds = params[1],
                             laplacian_method = laplacian_method,
                             laplacian_kwds = lapl_params[0])
                if input in ['data']:
                    G.set_data_matrix(X)
                if input in ['adjacency']:
                    G.set_adjacency_matrix(D)
                else:
                    G.set_affinity_matrix(A)
                laplacian_queried = G.compute_laplacian_matrix(**kwarg_params)
                assert_array_almost_equal(laplacian_true.todense(), laplacian_queried.todense(), almost_equal_decimals)
