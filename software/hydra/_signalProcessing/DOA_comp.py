import matplotlib.pyplot as plt
import numpy as np
### DOES THIS APPEAR?
# TEMPORARY STUFF USED FOR TESTING
'''
In the demo software, the receive signal is set by: 
    self.DOA_sample_size = self.module_receiver.iq_samples[0,:].size
    ...
    iq_samples = self.module_receiver.iq_samples[:, 0:self.DOA_sample_size]
'''
# --------------------------------------------------------------------------------------------------------------
# DEFINE ANTENNA PARAMETERS
'''
d = 0.5     # element spacing                       #***INIT METHOD*** self.DOA_inter_elem_spacing
M = 4       # number of elements in antenna array # #***INIT METHOD*** self.channel_number
N = 2**5    # number of samples                     #***INIT METHOD*** self.DOA_sample_size
alignment = "UCA"                                   #***INIT METHOD*** self.DOA_ant_alignment
freq = 447
radius = .5
 
scan_volume = np.arange(0,360,1) # set scan volume from 0 to 180 degrees                                                           #***INIT METHOD*** self.DOA_theta
array_manifold = np.arange(0,M,1)*d # define the array manifold physical structure (used to calculate array response vector)       #***estimate_DOA METHOD*** 
'''
'''
array_manifold is what we will characterize with our radiation patterns?
'''

# --------------------------------------------------------------------------------------------------------------
# GENERATE A TEST SIGNAL
'''
theta = 73  # chosen arbitrarily in the above example

if alignment=="ULA":
    a = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.cos(np.deg2rad(theta))) # array response vector
else:
    a = np.exp(2*np.pi*1j*radius*np.cos((np.deg2rad(theta)-(np.arange(0,M,1)/M)*(2*np.pi)))) # array response vector
    a = a.T

soi = np.random.normal(0,1,N)  # Signal of Interest (using Normal Gaussian Dist)
n = np.random.normal(0,np.sqrt(10**-1),(M,N)) # generate noise
As = np.outer(soi, a).T
rec_sig = As + n
'''
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class DOA_functions():
    def cov_mat_est(rec_sig, N): #***estimate_DOA METHOD***
        rec_sigH = (np.conjugate(rec_sig)).T # complex conjugate transpose
        # Compute the summation of x*x^H via the dot product numpy function and then divide each term by N
        R = np.divide(np.dot(rec_sig, rec_sigH),N)
        return R

    def eigendecomp(R, M):
        # eigendecomposition computation and sorting
        eigval, eigvec = np.linalg.eig(R) 

        eig_array = []
        for i in range(np.size(R,0)):
            eig_array.append([np.abs(eigval[i]),eigvec[:,i]])

        eig_array = sorted(eig_array, key=lambda eig_array: eig_array[0], reverse=False) # sort in numeric order by the eigenvalue

        # isolate noise subspace
        signal_dimension = 1 # Single incoming signal of interest
        noise_dimension = M - signal_dimension # signal subspace contains 1 eigenvector, noise subspace contains other three

        E_n = np.zeros((M,noise_dimension),dtype=complex) # preallocate the noise subspace array 
        
        # obtain the noise subspace array 
        for i in range(noise_dimension):     
            E_n[:,i] = eig_array[i][1]

        E_n = np.matrix(E_n) # noise subspace
        
        return E_n

    def ULA(scan_volume, array_manifold, M): #***estimate_DOA METHOD*** Takes place as an if statment (can have an option for UCA)
        a_theta_vec = np.zeros((M, np.size(scan_volume)), dtype=complex) 
        # compute the a(theta) matrix
        for i in range(np.size(scan_volume)):    
            a_theta_vec[:, i] = np.exp(array_manifold*1j*2*np.pi*np.cos(np.radians(scan_volume[i]))) # Scanning vector 

        return a_theta_vec

    def UCA(scan_volume, M, radius):
        a_theta_vec = np.zeros((M, np.size(scan_volume)), dtype=complex) 
        # compute the a(theta) matrix
        for i in range(np.size(scan_volume)):
            for j in range(M):    
                a_theta_vec[j, i] = np.exp(2*np.pi*1j*radius*np.cos(np.radians(scan_volume[i]-j*(360)/M))) # Scanning vector 

        return a_theta_vec

    def MUSIC(E_n, a_theta_vec): #***estimate_DOA METHOD*** gets called in the ULA if statement section 
        # preallocate
        P_MUSIC = np.zeros(np.size(a_theta_vec, 1),dtype=complex)    #***INIT METHOD*** self.DOA_MUSIC_res

        E_nH = (np.conjugate(E_n)).T # noise subspace hermitian

        for i in range(np.size(a_theta_vec, 1)):
            a_theta = np.reshape(a_theta_vec[:,i], (-1,1))
            a_thetaH = (np.conjugate(a_theta)).T
            P_MUSIC[i] = 1/np.abs(a_thetaH *(E_n*E_nH)* a_theta)

        return P_MUSIC

    # PHASE SHIFT VALUE CALCULATIONS 

    def peak_find(P_MUSIC, scan_volume, DOA_ant_alignment): # used to calcualte the angle of incoming signal
        peak_index = np.argmax(P_MUSIC)
        #print(peak_index)
        DOA_angle = scan_volume[peak_index]
        if (DOA_angle > 180) & (DOA_ant_alignment == "ULA"):
            DOA_angle = 360-DOA_angle
        print(DOA_angle)
        return DOA_angle

    def phase_shift_calc(DOA_angle, freq, DOA_ant_alignment,radius,channel_number): # used to calculate the phase shift value (delta)
        wavelength = (299.79/(freq))
        k = (2*np.pi) / wavelength
        phi = np.deg2rad(DOA_angle)
        delta_list = np.arange(0,channel_number,1, dtype="float")
        #print(delta_list)

        if (DOA_ant_alignment == "ULA"):
            d_physical_dist = 0.45 * wavelength/2
            delta = -k * d_physical_dist * np.sin(phi)
            print(delta)

            for elem in range(channel_number):
                delta_list[elem] = delta*elem

            print("Delta List: ",delta_list)
            return delta

        if (DOA_ant_alignment == "UCA"):
            for elem in range(channel_number):
                delta_list[elem] = -k * radius * np.cos(phi - 2*np.pi*(elem/channel_number))
            
            print(delta_list)
            return delta

    # Account for multiple transmitters via forward-backward averaging algorithm
    def fb_avg(R, M):
        J = np.eye(M)
        J = np.fliplr(J) 
        J = np.matrix(J)
        
        R_fb = 0.5 * (R + J*np.conjugate(R)*J)

        return np.array(R_fb)
    
    def app_PhaseShift(delta_list,arduino,side): # EDT-PS
        # TODO: Map deltaVal (degrees) to corresponding dacVal (0 to 4095)
        '''
        dacVal = 128 * deltaVal

        if side == "l":
            # Write value to serial port
            arduino.write((str(dacVal) + 'l' + '\n').encode())
            
        elif side == "r":
            # Write value to serial port
            arduino.write((str(dacVal) + 'r' + '\n').encode())
        '''
        print("Phase Shifters not implemented")

    def plot_MUSIC(P_MUSIC, scan_volume):
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

# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
'''
# TEST THE FUNCTIONS
# compute the covariance matrix
R = cov_mat_est(rec_sig,N)

# compute eigendecomposition
E_n = eigendecomp(R,M)

# characterize manifold
#a_theta_vec = ULA(scan_volume, array_manifold,M)
a_theta_vec = UCA(scan_volume, M, radius)

# compute MUSIC
P_MUSIC_UCA = MUSIC(E_n, a_theta_vec)

#a_theta_vec = ULA(scan_volume, array_manifold,M)
#P_MUSIC_ULA = MUSIC(E_n, a_theta_vec)

#DOA_angle = peak_find(P_MUSIC, scan_volume)
#delta = phase_shift_calc(DOA_angle, d, freq)

# plot
plot_MUSIC(P_MUSIC_UCA, scan_volume)
#plot_MUSIC(P_MUSIC_ULA, scan_volume)

'''