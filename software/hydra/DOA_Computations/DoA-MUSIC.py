# Implement the MUSIC Algorithm as a function to be used in demo software
'''
MUSIC will take the inputs: 
    - R                : Covariance Matrix 
    - Signal Dimension : Number of incoming signals
    - Scanning Vectors : Array Response Vector (ideal for now)

Parameters that need to be characterized: 
    - Number of elements
    - Interelement Spacing
    - UCA vs ULA (have two seperate functions)
    - Covariance Matrix Calculation (make a function)
    - **Stretch Goal** implement spatial smoothing for multiple incoming signals
'''

# Start by just writing out the code, then we will make functions of things

# Import Libraries
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------------------------------------------------------
# DEFINE ANTENNA PARAMETERS
d = 0.5     # element spacing
M = 4       # number of elements in antenna array
N = 2**5    # number of samples
# --------------------------------------------------------------------------------------------------------------
# SET WHAT THE INPUT WOULD BE TO THE MUSIC FUNCTION INPUT
scan_volume = np.arange(0,181,1) # set scan volume from 0 to 180 degrees
array_manifold = np.arange(0,M,1)*d # define the array manifold physical structure (used to calculate array response vector)

# preallocate the array repsonse vector matrix; it will have M (num elements in array) rows of 180 
# empty indices to be filled
'''
"a_theta_vec" we will rewrite to be characterized by the manifold radiation pattern
'''
a_theta_vec = np.zeros((M, np.size(scan_volume)), dtype=complex) 
# compute the a(theta) matrix
for i in range(np.size(scan_volume)):    
    a_theta_vec[:, i] = np.exp(array_manifold*1j*2*np.pi*np.cos(np.radians(scan_volume[i]))) # Scanning vector 
# --------------------------------------------------------------------------------------------------------------
# GENERATE A TEST SIGNAL
theta = 67  # chosen arbitrarily in the above example
a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.cos(np.deg2rad(theta))) # array response vector
soi = np.random.normal(0,1,N)  # Signal of Interest (using Normal Gaussian Dist)
n = np.random.normal(0,np.sqrt(10**-1),(M,N)) # generate noise
As = np.outer(soi, a).T
rec_sig = As + n
# --------------------------------------------------------------------------------------------------------------
# COMPUTATION OF THE COVARIANCE MATRIX AND EIGENDECOMPOSITION
# Using the received signal, we can first define x^H (hermitian of x)
rec_sigH = (np.conjugate(rec_sig)).T # complex conjugate transpose
# Next, we can compute the summation of x*x^H via the dot product numpy function
R = np.dot(rec_sig, rec_sigH)
# Finally, we will finish computing the covariance matrix by diving each term by the number of samples (N)
R = np.divide(R,N)

eigval, eigvec = np.linalg.eig(R)
eig_array = []
for i in range(np.size(R,0)):
    eig_array.append([np.abs(eigval[i]),eigvec[:,i]])

eig_array = sorted(eig_array, key=lambda eig_array: eig_array[0], reverse=False) # sort in numeric order by the eigenvalue

signal_dimension = 1 # Single incoming signal of interest
noise_dimension = M - signal_dimension # signal subspace contains 1 eigenvector, noise subspace contains other three

# preallocate the noise subspace array 
E_n = np.zeros((M,noise_dimension),dtype=complex)

# obtain the noise subspace array 
for i in range(noise_dimension):     
    E_n[:,i] = eig_array[i][1]

E_n = np.matrix(E_n)
E_nH = (np.conjugate(E_n)).T
# --------------------------------------------------------------------------------------------------------------
# COMPUTE MUSIC ALGORITHM
P_MUSIC = np.zeros(np.size(a_theta_vec, 1),dtype=complex) # preallocate
for i in range(np.size(a_theta_vec, 1)):
    a_theta = np.reshape(a_theta_vec[:,i], (-1,1))
    a_thetaH = (np.conjugate(a_theta)).T
    P_MUSIC[i] = 1/np.abs(a_thetaH *(E_n*E_nH)* a_theta)





### PLOTTING
DOA_data = P_MUSIC
DOA_data = np.divide(np.abs(DOA_data),np.max(np.abs(DOA_data))) # normalization
DOA_data = 10*np.log10(DOA_data)                   

#Plot DOA results  
plt.plot(scan_volume,DOA_data, color='blue')    
plt.title('Direction of Arrival estimation ',fontsize = 16)
plt.xlabel('Incident angle [deg]')
plt.ylabel('Amplitude [dB]')
plt.grid()
plt.show()





