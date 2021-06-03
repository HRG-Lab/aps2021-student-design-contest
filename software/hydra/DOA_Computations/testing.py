
import numpy as np
import matplotlib.pyplot as plt

from DOA_comp import DOA_functions as doa

# DEFINE ANTENNA PARAMETERS

d = 0.5     # element spacing                       #***INIT METHOD*** self.DOA_inter_elem_spacing
M = 4       # number of elements in antenna array # #***INIT METHOD*** self.channel_number
N = 2**5    # number of samples                     #***INIT METHOD*** self.DOA_sample_size
alignment = "ULA"                                   #***INIT METHOD*** self.DOA_ant_alignment
 
scan_volume = np.arange(0,181,1) # set scan volume from 0 to 180 degrees                                                           #***INIT METHOD*** self.DOA_theta
array_manifold = np.arange(0,M,1)*d # define the array manifold physical structure (used to calculate array response vector)       #***estimate_DOA METHOD*** 

'''
array_manifold is what we will characterize with our radiation patterns?
'''

# --------------------------------------------------------------------------------------------------------------
# GENERATE A TEST SIGNAL

theta = 67  # chosen arbitrarily in the above example
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.cos(np.deg2rad(theta))) # array response vector
soi = np.random.normal(0,1,N)  # Signal of Interest (using Normal Gaussian Dist)
n = np.random.normal(0,np.sqrt(10**-1),(M,N)) # generate noise
As = np.outer(soi, a).T
rec_sig = As + n


# TEST THE FUNCTIONS
# compute the covariance matrix
R = doa.cov_mat_test(rec_sig, N)

# compute eigendecomposition
E_n = doa.eigendecomp(R, M)

# characterize manifold
a_theta_vec = doa.ULA(scan_volume, array_manifold, M)

# compute MUSIC
P_MUSIC = doa.MUSIC(E_n, a_theta_vec)

# plot
doa.plot_MUSIC(P_MUSIC, scan_volume)

