# KerberosSDR Signal Processor
#
# Copyright (C) 2018-2019  Carl Laufer, Tamás Pető
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# -*
# - coding: utf-8 -*-

import sys
import os
import time
# Math support
import numpy as np
# Arduino/serial comm support
import serial
#from PhaseShiftControl import phaseShift

# Signal processing support
from scipy import fft,ifft
from scipy import signal
from scipy.signal import correlate

# GUI support
from PyQt5 import QtGui, QtCore

# import DoA Computation Functions
from DOA_comp import DOA_functions as doa


class SignalProcessor(QtCore.QThread):

    signal_spectrum_ready = QtCore.pyqtSignal()
    signal_sync_ready = QtCore.pyqtSignal()
    signal_DOA_ready = QtCore.pyqtSignal()
    signal_overdrive = QtCore.pyqtSignal(int)
    signal_period    = QtCore.pyqtSignal(float)
    
    #delta value to signal -EDT
    signal_delta = QtCore.pyqtSignal(float)
    signal_DOA_angle = QtCore.pyqtSignal(float)

    def __init__(self, parent=None, module_receiver=None):
        """
            Description:
            ------------

            Parameters:
            -----------

            Return values:
            --------------

        """
        super(SignalProcessor, self).__init__(parent) # super() allows for inheritance

        self.module_receiver = module_receiver
        self.en_spectrum = True
        self.en_sync = True
        self.en_sample_offset_sync = False
        self.en_record = False
        self.en_calib_iq = False
        self.en_DOA_estimation = False #DOA ADDED
        
        # DOA processing options
        self.en_DOA_MUSIC = False # set DOA method
        self.DOA_inter_elem_space = 0.5 # element spacing
        self.DOA_ant_alignment = "ULA" # antenna configuration
        self.en_DOA_FB_avg = False
        
        self.center_freq = 0  # TODO: Initialize this [Hz] - USED IN PHASE SHIFT CALCULATION
        self.fs = 1.024 * 10**6  # Decimated sampling frequency - Update from GUI
        #self.sample_size = 2**15
        self.channel_number = 4

        # PHASE SHIFT CALCULATION - INITIALIZING PARAMETERS
        self.delta_list = np.arange(0,self.channel_number,1)
        self.DOA_angle = 90
        #self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.arduino = 1
        self.side_LR = 'l'

        # PHASE SHIFTER configuration
        self.en_PhaseShifter = False # set phase shifters to be on or off
        
        # Processing parameters        
        self.test = None
        self.spectrum_sample_size = 2**14 #2**14
        self.DOA_sample_size = 2**15 # Connect to GUI value??
        self.xcorr_sample_size = 2**18 #2**18
        self.spectrum = np.ones((self.channel_number+1,self.spectrum_sample_size), dtype=np.float32)
        self.iq_data = np.ones((self.channel_number+1,self.spectrum_sample_size), dtype=np.float32)
        self.xcorr = np.ones((self.channel_number-1,self.xcorr_sample_size*2), dtype=np.complex64)        
        self.phasor_win = 2**10 # Phasor plot window
        self.phasors = np.ones((self.channel_number-1, self.phasor_win), dtype=np.complex64)
        self.run_processing = False
        
        # Result vectors
        self.delay_log= np.array([[0],[0],[0]])
        self.phase_log= np.array([[0],[0],[0]])
        self.DOA_MUSIC_res = np.ones(361)
        self.scan_vol = np.arange(0,361,1) # DOA ADDED
        ## self.DOA_theta = np.arange(0,181,1) not being used

        # Auto resync params
        self.lastTime = 0
        self.runningSync = 0
        self.timed_sync = False
        self.noise_checked = False
        self.resync_time = -1

    def run(self):
        
        self.run_processing = True
        
        while self.run_processing:
            start_time = time.time()

            self.module_receiver.download_iq_samples()

            self.DOA_sample_size = self.module_receiver.iq_samples[0,:].size # value of N in my code
            self.xcorr_sample_size = self.module_receiver.iq_samples[0,:].size
            self.xcorr = np.ones((self.channel_number-1,self.xcorr_sample_size*2), dtype=np.complex64) 
            
            # Check overdrive
            if self.module_receiver.overdrive_detect_flag:
                self.signal_overdrive.emit(1)
            else:
                self.signal_overdrive.emit(0)
            
            # Display spectrum
            if self.en_spectrum:
                self.spectrum[0, :] = np.fft.fftshift(np.fft.fftfreq(self.spectrum_sample_size, 1/self.fs))/10**6

                m = self.channel_number
                #self.spectrum[1:m+1,:] = 10*np.log10(np.fft.fftshift(np.abs(np.fft.fft(self.module_receiver.iq_samples[0:m, 0:self.spectrum_sample_size]))))

                for m in range(self.channel_number):
                    self.spectrum[m+1,:] = 10*np.log10(np.fft.fftshift(np.abs(np.fft.fft(self.module_receiver.iq_samples[m, 0:self.spectrum_sample_size]))))
                    self.iq_data[m+1,:] = self.module_receiver.iq_samples[m, 0:self.spectrum_sample_size]
                self.signal_spectrum_ready.emit()
            
            # Synchronization
            if self.en_sync or self.timed_sync:
                #print("Sync graph enabled")
                self.sample_delay()
                self.signal_sync_ready.emit()
            
            # Sample offset compensation request
            if self.en_sample_offset_sync:
                self.module_receiver.set_sample_offsets(self.delay_log[:,-1])
                self.en_sample_offset_sync = False    
            
            # IQ calibration request
            if self.en_calib_iq:
                # IQ correction
                for m in range(self.channel_number):
                    self.module_receiver.iq_corrections[m] *= np.size(self.module_receiver.iq_samples[0, :])/(np.dot(self.module_receiver.iq_samples[m, :],self.module_receiver.iq_samples[0, :].conj()))
                c = np.sqrt(np.sum(np.abs(self.module_receiver.iq_corrections)**2))
                self.module_receiver.iq_corrections = np.divide(self.module_receiver.iq_corrections, c)
                #print("Corrections: ",self.module_receiver.iq_corrections)
                self.en_calib_iq = False            

            # Record IQ samples
            if self.en_record:
                np.save('hydra_samples.npy', self.module_receiver.iq_samples)

            # Direction of Arrival Estimation
            if self.en_DOA_estimation:
                # Get FFT for squelch
                self.spectrum[1,:] = 10*np.log10(np.fft.fftshift(np.abs(np.fft.fft(self.module_receiver.iq_samples[0, 0:self.spectrum_sample_size]))))
                self.estimate_DOA()
                self.signal_DOA_ready.emit()

            if self.en_PhaseShifter:
                self.call_PhaseShifters()


            # Code to maintain sync
            stop_time = time.time()
            self.signal_period.emit(stop_time - start_time)


    def sample_delay(self):
        #print("Entered sample delay func")
        N = self.xcorr_sample_size
        iq_samples = self.module_receiver.iq_samples[:, 0:N]
       
        delays = np.array([[0],[0],[0]])
        phases = np.array([[0],[0],[0]])
        # Channel matching
        np_zeros = np.zeros(N, dtype=np.complex64)
        x_padd = np.concatenate([iq_samples[0, :], np_zeros])
        x_fft = np.fft.fft(x_padd)
        for m in np.arange(1, self.channel_number):
            y_padd = np.concatenate([np_zeros, iq_samples[m, :]])
            y_fft = np.fft.fft(y_padd)
            self.xcorr[m-1] = np.fft.ifft(x_fft.conj() * y_fft)
            delay = np.argmax(np.abs(self.xcorr[m-1])) - N
            #phase = np.rad2deg(np.angle(self.xcorr[m-1, delay + N]))
            phase = np.rad2deg(np.angle(self.xcorr[m-1, N]))
            
            #msg = "[ INFO ] delay: " + str(delay)
            #print(msg)
            delays[m-1,0] = delay
            phases[m-1,0] = phase

        self.delay_log = np.concatenate((self.delay_log, delays),axis=1)
        self.phase_log = np.concatenate((self.phase_log, phases),axis=1)
    
    def delete_sync_history(self):
        self.delay_log= np.array([[0],[0],[0]])
        self.phase_log= np.array([[0],[0],[0]])


    # DoA Computation
    def estimate_DOA(self):
        iq_samples = self.module_receiver.iq_samples[:, 0:self.DOA_sample_size]
        N = self.DOA_sample_size
        M = self.channel_number
        d = self.DOA_inter_elem_space # USED IN PHASE SHIFT CALCULATION
        self.radius = self.DOA_inter_elem_space/(np.sqrt(2))
        array_manifold = np.arange(0,M,1) * d

        R = doa.cov_mat_est(iq_samples, N)


        # compute forward-backward (fb-alg) average is enabled
        if self.en_DOA_FB_avg:
            R = doa.fb_avg(R,M)
            print("Forward-Backward Averaging Enabled")
            print("FB Avg, R: ", R)
        else:
            print("No FB Avg, R: ", R)


        En = doa.eigendecomp(R, M)

        if self.DOA_ant_alignment == "ULA":
            self.scan_vol = np.linspace(0,360,361) # impacts axis? - currently set to [0-->180]
            array_response_vec = doa.ULA(self.scan_vol,array_manifold, M)

            if self.en_DOA_MUSIC:
                self.DOA_MUSIC_res = doa.MUSIC(En, array_response_vec)

            # PHASE SHIFT CALCULATIONS
            self.DOA_angle = doa.peak_find(self.DOA_MUSIC_res, self.scan_vol, self.DOA_ant_alignment)
            self.delta_list = doa.phase_shift_calc(self.DOA_angle, self.center_freq, self.DOA_ant_alignment, self.radius, self.channel_number)
            #-EDT
            self.signal_delta.emit(self.delta_list[1])
            self.signal_DOA_angle.emit(self.DOA_angle)

            if self.DOA_angle <= 90:
                self.side_LR = 'l'
            if self.DOA_angle > 90:
                self.side_LR = 'r'
            
            doa.app_PhaseShift(self.delta,self.arduino,self.side_LR)
            
        if self.DOA_ant_alignment == "UCA":
            self.scan_vol = np.linspace(0,360,361) # impacts axis? - currently set to [0-->180]
            array_response_vec = doa.UCA(self.scan_vol, M, self.radius)
            
            if self.en_DOA_MUSIC:
                self.DOA_MUSIC_res = doa.MUSIC(En, array_response_vec)

            # PHASE SHIFT CALCULATIONS
            self.DOA_angle = doa.peak_find(self.DOA_MUSIC_res, self.scan_vol, self.DOA_ant_alignment)
            self.delta_list = doa.phase_shift_calc(self.DOA_angle, self.center_freq, self.DOA_ant_alignment,self.radius, self.channel_number)
            #-EDT
            self.signal_delta.emit(self.delta_list[1])
            self.signal_DOA_angle.emit(self.DOA_angle)
            
    def call_PhaseShifters(self):
        if self.DOA_ant_alignment == "UCA":
            print("Phase Shifters Enabled UCA")
            if (self.DOA_angle <= 90) & (self.DOA_angle >= 270):
                self.side_LR = 'l'
            if (self.DOA_angle > 90) & (self.DOA_angle < 270):
                self.side_LR = 'r'
            
<<<<<<< HEAD
            doa.app_PhaseShift(self.delta,self.arduino,self.side_LR)
=======
            doa.app_PhaseShift(self.delta_list,self.arduino,self.side_LR)
            
        if self.DOA_ant_alignment == "ULA":
            print("Phase Shifters Enabled ULA")
            if self.DOA_angle <= 90:
                self.side_LR = 'l'
            if self.DOA_angle > 90:
                self.side_LR = 'r'
            
            doa.app_PhaseShift(self.delta_list,self.arduino,self.side_LR)

>>>>>>> 527e56952e5ce21979be20c7a291d2208156045d


    def stop(self):
        self.run_processing = False


def busy_wait(dt):
    current_time = time.time()
    while (time.time() < current_time+dt):
        pass
