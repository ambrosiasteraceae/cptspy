
import numpy as np

# BEARING CAPACITY -> Refer to "Foundation Analysis & Design (Bowles 5ed) pg. 246

# Friction angles ->
phis = np.array([0, 5, 10, 15, 20, 25, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50])
# N_c term
n_c_test = np.array(
    [5.14, 6.49, 8.34, 10.97, 14.83, 20.71, 22.25, 25.79, 30.13, 35.47, 42.14, 50.55, 61.31, 75.25, 133.73, 266.5, ])
# N_q term
n_q_test = np.array([1, 1.6, 2.5, 3.9, 6.4, 10.7, 11.8, 14.7, 18.4, 23.2, 29.4, 37.7, 48.9, 64.1, 134.7, 318.5])

# HANSEN VEZIC & MEYERHOF
n_y_hansen_test = np.array([0, 0.1, 0.4, 1.2, 2.9, 6.8, 7.9, 10.9, 15.1, 20.8, 28.7, 40.0, 56.1, 79.4, 200.5, 567.4])
n_y_vezic_test = np.array([0, 0.4, 1.2, 2.6, 5.4, 10.9, 12.5, 16.7, 22.4, 30.2, 41, 56.2, 77.9, 109.3, 271.3, 761.3, ])
n_y_meyerhof_test = np.array([0, 0.1, 0.4, 1.1, 2.9, 6.8, 8, 11.2, 15.7, 22, 31.1, 44.4, 64, 93.6, 262.3, 871.7])

#from numpy import testing
# from tests import values
#
# n_y_hansen_test = np.array([0, 0.1, 0.4, 1.2, 2.9, 6.8, 7.9, 10.9, 15.1, 20.8, 28.7, 40.0, 56.1, 79.4, 200.5, 567.4])
#
# testing.assert_allclose(nc, values.n_c_test, rtol=0.1)
# # testing.assert_allclose(nq, values.n_q_test, rtol=0.1)
# # testing.assert_allclose(ny, n_y_hansen_test, rtol=0.1)
# #

# for phi, _, __, ___ in zip(phiss, nc, nq, ny, ):
#     print(f"{phi},{_:.2f},{__:.2f},{___:.2f}")