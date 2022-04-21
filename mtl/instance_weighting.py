"""Implements instance weighting via convex optimization"""

import logging
import logging.config
import time

import cvxpy as cp
import numpy as np
import scipy
import os

import tensorflow as tf
import tensorflow_constrained_optimization as tfco

## this currently works for all number of tasks
def quadratic_programming(Y, verbose=False, grouping_name=''):
    """
    Solves the constrained least-squares / quadratic program objective:

        \min_w 0.5 * ||Yw - c||_2^2 \\
        s.t. \begin{cases}
            \sum_i w_i = 1 \\
            w_i \ge 0
        \end{cases}

    where c is a w-sized constant vector of values 1/2.

    Reference: https://www.cvxpy.org/examples/basic/quadratic_program.html
    """
    grouping_name = grouping_name + 'quadratic_programming'
    file_name = grouping_name + '.npy'
    if os.path.exists(os.path.join('./mtl_suby_w', file_name)):
        w = np.load(os.path.join('./mtl_suby_w', file_name))
        return w, grouping_name


    k, n = Y.shape  # k = number of tasks, n = number of instances
    c = 0.5 * np.ones((k,), dtype=np.float32)
    print("Solving for w over %d examples. Input array of labels: (%d tasks, %d examples).", n, k, n)

    # Solve
    w = cp.Variable(n, nonneg=True)
    prob = cp.Problem(
        cp.Minimize(cp.norm(Y @ w - c)),
        [
            cp.sum(w) == 1,  # w as a distribution constraint
        ]
    )

    start = time.time()
    prob.solve(solver=cp.ECOS, verbose=verbose)
    end = time.time()
    print("Took %.2f seconds to solve the quadratic program.", (end - start))

    return w.value, grouping_name

## this currently works for a small number of tasks
def entropy_maximization(Y, verbose=False, grouping_name=''):
    """
    Solves the linearly inequality constrained entropy maximization problem:

        \min_w -\sum_i w_i \log(w_i) \\
        s.t. \begin{cases}
            Yw = c \\
            \sum_i w_i = 1 \\
            s_i \ge 0
        \end{cases}

    where c is a w-sized constant vector of values 1/2.

    Reference: https://www.cvxpy.org/examples/applications/max_entropy.html
    """

    grouping_name = grouping_name + 'entropy_maximization'
    file_name = grouping_name + '.npy'
    if os.path.exists(os.path.join('./mtl_suby_w', file_name)):
        w = np.load(os.path.join('./mtl_suby_w', file_name))
        return w, grouping_name


    Y = Y.astype(np.float32)
    k, n = Y.shape  # k = number of tasks, n = number of instances
    c = 0.5 * np.ones((k,), dtype=np.float32)
    print(f"Solving for w over {n} examples. Input array of labels: ({k} tasks, {n} examples).")

    # Solve
    w = cp.Variable(n, nonneg=True)
    prob = cp.Problem(
        cp.Maximize(cp.sum(cp.entr(w))),
        [
            Y @ w == c,
            cp.sum(w) == 1,
        ]
    )

    start = time.time()
    prob.solve(solver=cp.ECOS, verbose=verbose, qcp=True)
    print("Caught ECOS error, probably due to unconverged tolerance")
    end = time.time()

    print(f"Took {end - start:.2f} seconds to solve the entropy minimization problem.")
    print(w.value)
    return w.value, grouping_name

def entropy_maximization_pgd(Y, verbose=False, grouping_name=''):
    """
    Solves the linearly inequality constrained entropy maximization problem:

        \min_w -\sum_i w_i \log(w_i) \\
        s.t. \begin{cases}
            Yw = c \\
            \sum_i w_i = 1 \\
            s_i \ge 0
        \end{cases}

    where c is a w-sized constant vector of values 1/2.

    where we utilize pgd
    """

    grouping_name = grouping_name + 'entropy_maximization'
    file_name = grouping_name + '.npy'
    if os.path.exists(os.path.join('./mtl_suby_w', file_name)):
        w = np.load(os.path.join('./mtl_suby_w', file_name))
        return w, grouping_name


    Y = Y.astype(np.float32)
    k, n = Y.shape  # k = number of tasks, n = number of instances
    c = 0.5 * np.ones((k,), dtype=np.float32)
    print(f"Solving for w over {n} examples. Input array of labels: ({k} tasks, {n} examples).")

    # Solve
    w = cp.Variable(n, nonneg=True)
    prob = cp.Problem(
        cp.Maximize(cp.sum(cp.entr(w))),
        [
            Y @ w == c,
            cp.sum(w) == 1,
        ]
    )

    start = time.time()
    prob.solve(solver=cp.ECOS, verbose=verbose, qcp=True)
    print("Caught ECOS error, probably due to unconverged tolerance")
    end = time.time()

    print(f"Took {end - start:.2f} seconds to solve the entropy minimization problem.")
    print(w.value)
    return w.value, grouping_name



if __name__ == "__main__":
    # This is just a code block to test out the optimization functions independent of the train scripts.
    from omegaconf import OmegaConf
    config = OmegaConf.load("./configs/exp/erm.yaml")
    config.dataset.groupings = [
        "Big_Lips:Chubby",
        "Bushy_Eyebrows:Blond_Hair",
        "Wearing_Lipstick:Male",
        #"Gray_Hair:Young",
        #"High_Cheekbones:Smiling",
        #"Goatee:No_Beard",
        #"Wavy_Hair:Straight_Hair",
    ]
    config.dataset.task_weights = [1, 1, 1]

    grouping_name = (";").join(config.dataset.groupings)

    # Initialize train dataset
    from datasets.celeba import CelebA
    dataset = CelebA(config, split="train")
    Y = dataset.attr[:, dataset.task_label_indices].T.numpy()  # (7, 162770)
    Y = scipy.sparse.csr_matrix(Y)
    w, grouping_name = entropy_maximization(Y, verbose=True, grouping_name = grouping_name)
    print(f"verify that the weights multiply against the multi-class labels to 1/2: {Y@w}")
    print(f"verify that weights sum to one: {np.sum(w)}")
    print(f'minimum value of weight: {np.amin(w)}')
    print(f'maximum value of weight: {np.amax(w)}')

    ### save to cache the with groupings this is for
    os.makedirs('./mtl_suby_w', exist_ok=True)
    np.save(os.path.join('./mtl_suby_w',grouping_name),w)
    #w = entropy_maximization(Y, verbose=True)
