# KerberosSDR Python GUI

# Copyright (C) 2018-2019  Carl Laufer, Tamás Pető
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# -*- coding: utf-8 -*

import sys
import os
import time
import math
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
import scipy
from bottle import route, run, request, get, post, redirect, template, static_file
import threading
import subprocess
import save_settings as settings

np.seterr(divide='ignore')

# Import Kerberos modules
currentPath = os.path.dirname(os.path.realpath(__file__))
rootPath = os.path.dirname(currentPath)

receiverPath        = os.path.join(rootPath, "_receiver")
signalProcessorPath = os.path.join(rootPath, "_signalProcessing")

sys.path.insert(0, receiverPath)
sys.path.insert(0, signalProcessorPath)

from hydra_receiver import ReceiverRTLSDR

# Import graphical user interface packages
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

# Import packages for plotting
import matplotlib
matplotlib.use('Agg') # For Raspberry Pi compatiblity
from matplotlib import cm
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches


from hydra_main_window_layout import Ui_MainWindow
from hydra_signal_processor import SignalProcessor

# Import the pyArgus module
#root_path = os.getcwd()
#pyargus_path = os.path.join(os.path.join(root_path, "pyArgus"), "pyArgus")
#sys.path.insert(0, pyargus_path)
#import directionEstimation as de

#from pyargus import directionEstimation as de

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__ (self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #f = open('/dev/null', 'w')
        #sys.stdout = f

        self.tabWidget.setCurrentIndex(0)

        # Set pyqtgraph to use white background, black foreground
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('imageAxisOrder', 'row-major')
        #pg.setConfigOption('useOpenGL', True)
        #pg.setConfigOption('useWeave', True)

        # Spectrum display

        self.win_spectrum = pg.GraphicsWindow(title="Quad Channel Spectrum")
        

        self.export_spectrum = pg.exporters.ImageExporter(self.win_spectrum.scene())

        self.plotWidget_spectrum_ch1 = self.win_spectrum.addPlot(title="Channel 1")
        self.plotWidget_spectrum_ch2 = self.win_spectrum.addPlot(title="Channel 2")
        self.win_spectrum.nextRow()
        self.plotWidget_spectrum_ch3 = self.win_spectrum.addPlot(title="Channel 3")
        #self.plotWidget_spectrum_ch4 = self.win_spectrum.addPlot(title="Channel 4")
        self.plotWidget_spectrum_ch4 = self.win_spectrum.addPlot(title="Beamforming Plot")

        self.plotWidget_spectrum_ch1.setYRange(-20,40, padding=0)
        self.plotWidget_spectrum_ch2.setYRange(-20,40, padding=0)
        self.plotWidget_spectrum_ch3.setYRange(-20,40, padding=0)
        self.plotWidget_spectrum_ch4.setYRange(-20,40, padding=0)

        self.gridLayout_spectrum.addWidget(self.win_spectrum, 1, 1, 1, 1)

        x = np.arange(1000)
        y = np.random.normal(size=(4,1000))

        self.spectrum_ch1_curve = self.plotWidget_spectrum_ch1.plot(x, y[0], clear=True, pen=(153, 0, 76))
        self.spectrum_ch2_curve = self.plotWidget_spectrum_ch2.plot(x, y[1], clear=True, pen=(76,0,153))
        self.spectrum_ch3_curve = self.plotWidget_spectrum_ch3.plot(x, y[2], clear=True, pen=(0,102,51))
        #self.spectrum_ch4_curve = self.plotWidget_spectrum_ch4.plot(x, y[3], clear=True, pen=(153, 153, 0))
        # HRG - Digital BF Test
        self.spectrum_ch4_curve = self.plotWidget_spectrum_ch4.plot(x, y[0] + y[1] + y[2] + y[3], clear=True, pen=(153, 153, 0))
        

        self.plotWidget_spectrum_ch1.setLabel("bottom", "Frequency [MHz]")
        self.plotWidget_spectrum_ch1.setLabel("left", "Amplitude [dBm]")
        self.plotWidget_spectrum_ch2.setLabel("bottom", "Frequency [MHz]")
        self.plotWidget_spectrum_ch2.setLabel("left", "Amplitude [dBm]")
        self.plotWidget_spectrum_ch3.setLabel("bottom", "Frequency [MHz]")
        self.plotWidget_spectrum_ch3.setLabel("left", "Amplitude [dBm]")
        #self.plotWidget_spectrum_ch4.setLabel("bottom", "Frequency [MHz]")
        #self.plotWidget_spectrum_ch4.setLabel("left", "Amplitude [dBm]")

        # HRG - Digital BF Test
        self.plotWidget_spectrum_ch4.setLabel("bottom", "Frequency [MHz]")
        self.plotWidget_spectrum_ch4.setLabel("left", "Amplitude [dBm]")

        #---> Sync display <---
        # --> Delay

        self.win_sync = pg.GraphicsWindow(title="Receiver Sync")

        self.export_sync = pg.exporters.ImageExporter(self.win_sync.scene())

        self.plotWidget_sync_absx = self.win_sync.addPlot(title="ABS X Corr")
        #self.plotWidget_sync_absx.setDownsampling(ds=4, mode='subsample')
        #self.plotWidget_sync_normph = self.win_sync.addPlot(title="Normalized Phasors")
        self.win_sync.nextRow()
        self.plotWidget_sync_sampd = self.win_sync.addPlot(title="Sample Delay History")
        self.plotWidget_sync_phasediff = self.win_sync.addPlot(title="Phase Diff History")

        self.gridLayout_sync.addWidget(self.win_sync, 1, 1, 1, 1)

        x = np.arange(1000)
        y = np.random.normal(size=(4,1000))

        # ------------- DOA results display setup ---------------
        self.win_DOA = pg.GraphicsWindow(title="DOA Plot")
        #Set up image exporter for web display
        #self.export_DOA = pg.exporters.ImageExporter(self.win_DOA.scene())

        self.plotWidget_DOA = self.win_DOA.addPlot(title="Direction of Arrival Estimation")
        self.plotWidget_DOA.setLabel("bottom", "Incident Angle [deg]")
        self.plotWidget_DOA.setLabel("left", "Amplitude [dB]")
        self.plotWidget_DOA.showGrid(x=True, alpha=0.25)
        self.gridLayout_DOA.addWidget(self.win_DOA, 1, 1, 1, 1)

        self.DOA_res_fd = open("/ram/DOA_value.html","w") # DOA estimation result file descriptor

        # Junk data to just init plot legends
        x = np.arange(1000)
        y = np.random.normal(size=(4,1000))

        self.plotWidget_DOA.addLegend()
        self.plotWidget_DOA.plot(x, y[0], pen=pg.mkPen((0, 45, 98), width=2), name="MUSIC")

        # Connect pushbutton signals
        self.pushButton_close.clicked.connect(self.pb_close_clicked)
        self.pushButton_proc_control.clicked.connect(self.pb_proc_control_clicked)
        self.pushButton_sync.clicked.connect(self.pb_sync_clicked)
        self.pushButton_iq_calib.clicked.connect(self.pb_calibrate_iq_clicked)
        self.pushButton_del_sync_history.clicked.connect(self.pb_del_sync_history_clicked)
        self.pushButton_set_receiver_config.clicked.connect(self.pb_rec_reconfig_clicked)
        self.stream_state = False

        # Status and configuration tab control
        self.tabWidget.currentChanged.connect(self.tab_changed)

        # Connect checkbox signals
        self.checkBox_en_uniform_gain.stateChanged.connect(self.pb_rec_reconfig_clicked)
        self.checkBox_en_sync_display.stateChanged.connect(self.set_sync_params)
        self.checkBox_en_spectrum.stateChanged.connect(self.set_spectrum_params)
        self.checkBox_en_dc_compensation.stateChanged.connect(self.set_iq_preprocessing_params)
        self.checkBox_en_noise_source.stateChanged.connect(self.switch_noise_source)
        # ---------- DOA STUFF
        self.checkBox_en_DOA.stateChanged.connect(self.set_DOA_params)
        self.checkBox_en_DOA_MUSIC.stateChanged.connect(self.set_DOA_params)

        # Phase Shifter Configuation - RED
        self.checkBox_en_PhaseShifter.stateChanged.connect(self.set_PhaseShifter_params)

        # Connect spinbox signals
        self.doubleSpinBox_filterbw.valueChanged.connect(self.set_iq_preprocessing_params)
        self.spinBox_fir_tap_size.valueChanged.connect(self.set_iq_preprocessing_params)
        self.spinBox_decimation.valueChanged.connect(self.set_iq_preprocessing_params)

        self.doubleSpinBox_DOA_d.valueChanged.connect(self.set_DOA_params)
        self.spinBox_DOA_sample_size.valueChanged.connect(self.set_DOA_params)

        self.doubleSpinBox_center_freq.valueChanged.connect(self.set_DOA_params)

        self.spinBox_resync_time.valueChanged.connect(self.set_resync_time)

        self.comboBox_antenna_alignment.currentIndexChanged.connect(self.set_DOA_params)

        # Instantiate and configure Hydra modules
        self.module_receiver = ReceiverRTLSDR()

        self.module_receiver.block_size = int(sys.argv[1]) * 1024

        self.module_signal_processor = SignalProcessor(module_receiver=self.module_receiver)

        self.module_signal_processor.signal_overdrive.connect(self.power_level_update)
        self.module_signal_processor.signal_period.connect(self.period_time_update)
        self.module_signal_processor.signal_spectrum_ready.connect(self.spectrum_plot)
        self.module_signal_processor.signal_sync_ready.connect(self.delay_plot)
        self.module_signal_processor.signal_DOA_ready.connect(self.DOA_plot)

        #connect delta/DOA values -EDT
        self.module_signal_processor.signal_delta.connect(self.delta_update)
        self.module_signal_processor.signal_DOA_angle.connect(self.DOA_angle_update)
                
        # -> Set default configuration for the signal processing module
        self.set_spectrum_params()
        self.set_sync_params()
        self.set_DOA_params()

        self.DOA_time = time.time()
        self.sync_time = time.time()
        self.spectrum_time = time.time()

        # Set default configuration for the GUI components
        self.set_default_configuration()

        self.ip_addr = sys.argv[2]
        threading.Thread(target=run, kwargs=dict(host=self.ip_addr, port=8080, quiet=True, debug=False, server='paste')).start()

        ### USED FOR PHASE SHIFT CALCULATION - NEEDED TO CONNECT THE CENTER FREQ 
        self.module_signal_processor.center_freq = self.doubleSpinBox_center_freq.value()


    def set_default_configuration(self):

        self.power_level_update(0)
        self.checkBox_en_spectrum.setChecked(False)
        self.checkBox_en_DOA.setChecked(False)

    def calculate_spacing(self):
        ant_arrangement_index = self.comboBox_antenna_alignment.currentText()
        ant_meters = self.doubleSpinBox_DOA_d.value()
        freq = self.doubleSpinBox_center_freq.value()
        wave_length = (299.79/freq)
        if ant_arrangement_index == "ULA":
            ant_spacing = (ant_meters/wave_length)

        elif ant_arrangement_index == "UCA": ##RD COMMENT
            ant_spacing = ((ant_meters/wave_length)/math.sqrt(2)) ##RD COMMENT

        return ant_spacing

    def tab_changed(self):
        tab_index = self.tabWidget.currentIndex()

        if tab_index == 0:  # Spectrum tab
            self.stackedWidget_config.setCurrentIndex(0)
        elif tab_index == 1:  # Sync tab
            self.stackedWidget_config.setCurrentIndex(1)
        elif tab_index == 2:  # DOA tab
            self.stackedWidget_config.setCurrentIndex(2)

    def set_sync_params(self):
        if self.checkBox_en_sync_display.checkState():
            self.module_signal_processor.en_sync = True
        else:
            self.module_signal_processor.en_sync = False
    def set_spectrum_params(self):
        if self.checkBox_en_spectrum.checkState():
            self.module_signal_processor.en_spectrum = True
        else:
            self.module_signal_processor.en_spectrum = False


    def pb_rec_reconfig_clicked(self):
        center_freq = self.doubleSpinBox_center_freq.value() *10**6
        sample_rate = float(self.comboBox_sampling_freq.currentText()) *10**6 #self.doubleSpinBox_sampling_freq.value()*10**6
        gain = [0,0,0,0]
        if self.checkBox_en_uniform_gain.checkState():
            gain[0] = 10*float(self.comboBox_gain.currentText())
            gain[1] = 10*float(self.comboBox_gain.currentText())
            gain[2] = 10*float(self.comboBox_gain.currentText())
            gain[3] = 10*float(self.comboBox_gain.currentText())
            gain_index = self.comboBox_gain.currentIndex()
            self.module_receiver.receiver_gain = 10*float(self.comboBox_gain.currentText())
            form.comboBox_gain_2.setCurrentIndex(int(gain_index))
            form.comboBox_gain_2.setEnabled(False)
            self.module_receiver.receiver_gain_2 = 10*float(self.comboBox_gain.currentText())
            form.comboBox_gain_3.setCurrentIndex(int(gain_index))
            form.comboBox_gain_3.setEnabled(False)
            self.module_receiver.receiver_gain_3 = 10*float(self.comboBox_gain.currentText())
            form.comboBox_gain_4.setCurrentIndex(int(gain_index))
            form.comboBox_gain_4.setEnabled(False)
            self.module_receiver.receiver_gain_4 = 10*float(self.comboBox_gain.currentText())
        else:
            gain[0] = 10*float(self.comboBox_gain.currentText())
            gain[1] = 10*float(self.comboBox_gain_2.currentText())
            gain[2] = 10*float(self.comboBox_gain_3.currentText())
            gain[3] = 10*float(self.comboBox_gain_4.currentText())
            self.module_receiver.receiver_gain = 10*float(self.comboBox_gain.currentText())
            form.comboBox_gain_2.setEnabled(True)
            self.module_receiver.receiver_gain_2 = 10*float(self.comboBox_gain_2.currentText())
            form.comboBox_gain_3.setEnabled(True)
            self.module_receiver.receiver_gain_3 = 10*float(self.comboBox_gain_3.currentText())
            form.comboBox_gain_4.setEnabled(True)
            self.module_receiver.receiver_gain_4 = 10*float(self.comboBox_gain_4.currentText())

        self.module_receiver.fs = float(self.comboBox_sampling_freq.currentText())*10**6 #self.doubleSpinBox_sampling_freq.value()*10**6
        self.module_signal_processor.fs = self.module_receiver.fs/self.module_receiver.decimation_ratio

        self.module_signal_processor.center_freq=self.doubleSpinBox_center_freq.value() *10**6
        self.module_receiver.reconfigure_tuner(center_freq, sample_rate, gain)

    def switch_noise_source(self):
        if self.checkBox_en_noise_source.checkState():
            self.module_signal_processor.noise_checked = True
            self.module_receiver.switch_noise_source(1)
        else:
            self.module_signal_processor.noise_checked = False
            self.module_receiver.switch_noise_source(0)
    def set_iq_preprocessing_params(self):
        """
            Update IQ preprocessing parameters
            Callback function of:
                -
        """
        # Set DC compensations
        if self.checkBox_en_dc_compensation.checkState():
            self.module_receiver.en_dc_compensation = True
        else:
            self.module_receiver.en_dc_compensation = False

        # Set FIR filter parameters
        tap_size = self.spinBox_fir_tap_size.value()
        bw = self.doubleSpinBox_filterbw.value() * 10**3  # ->[kHz]
        self.module_receiver.set_fir_coeffs(tap_size, bw)

        # Set Decimation
        self.module_receiver.decimation_ratio = self.spinBox_decimation.value()
        self.module_signal_processor.fs = self.module_receiver.fs/self.module_receiver.decimation_ratio

    def set_DOA_params(self):
        """
            Update DOA processing parameters
            Callback function of:
                -
        """
        #  Set DOA processing option
        if self.checkBox_en_DOA.checkState():
            self.module_signal_processor.en_DOA_estimation = True
        else:
            self.module_signal_processor.en_DOA_estimation = False


        if self.checkBox_en_DOA_MUSIC.checkState():
            self.module_signal_processor.en_DOA_MUSIC = True
        else:
            self.module_signal_processor.en_DOA_MUSIC = False
        
        # used for forward-backward (fb-alg) computation
        if self.checkBox_en_DOA_FB_avg.checkState():
            self.module_signal_processor.en_DOA_FB_avg = True
        else:
            self.module_signal_processor.en_DOA_FB_avg = False
        

        #self.module_signal_processor.DOA_inter_elem_space = self.doubleSpinBox_DOA_d.value()
        self.module_signal_processor.DOA_inter_elem_space = self.calculate_spacing()
        self.module_signal_processor.DOA_ant_alignment = self.comboBox_antenna_alignment.currentText()
        
        
        if self.module_signal_processor.DOA_ant_alignment == "ULA": # check if this is actually needed for just ULA?
            self.checkBox_en_DOA_FB_avg.setEnabled(True)
        
        else: # UCA 
            self.checkBox_en_DOA_FB_avg.setEnabled(False)
            self.checkBox_en_DOA_FB_avg.setCheckState(False)
        
        
        self.module_signal_processor.DOA_sample_size = 2**self.spinBox_DOA_sample_size.value()

    # Phase Shifter Configuration - RED
    def set_PhaseShifter_params(self):
        if self.checkBox_en_PhaseShifter.checkState():
            self.module_signal_processor.en_PhaseShifter = True
        else:
            self.module_signal_processor.en_PhaseShifter = False

    def set_resync_time(self):
        self.module_signal_processor.resync_time = self.spinBox_resync_time.value()


    def pb_close_clicked(self):
        #self.stop_streaming()
        #self.module_receiver.module_state = "EXIT"
        self.module_receiver.close()
        self.DOA_res_fd.close()
        self.close()


    def pb_proc_control_clicked(self):
        if self.pushButton_proc_control.text() == "Start processing":
            self.pushButton_proc_control.setText("Stop processing")


            self.module_signal_processor.start()

        elif self.pushButton_proc_control.text() == "Stop processing":
            self.pushButton_proc_control.setText("Start processing")

            self.module_signal_processor.stop()

    def pb_sync_clicked(self):
        #print("[ INFO ] Sync requested")
        self.module_signal_processor.en_sample_offset_sync=True

    def pb_calibrate_iq_clicked(self):
        #print("[ INFO ] IQ calibration requested")
        self.module_signal_processor.en_calib_iq=True

    def pb_del_sync_history_clicked(self):
        self.module_signal_processor.delete_sync_history()

    def power_level_update(self, over_drive_flag):
        if over_drive_flag:
            red_text = "<span style=\" font-size:8pt; font-weight:600; color:#ff0000;\" >"
            red_text += "OVERDRIVE"
            red_text += ("</span>")
            self.label_power_level.setText(red_text)
        else:
            green_text = "<span style=\" font-size:8pt; font-weight:600; color:#01df01;\" >"
            green_text += "OK"
            green_text += ("</span>")
            self.label_power_level.setText(green_text)
    def period_time_update(self, update_period):
        if update_period > 1:
            self.label_update_rate.setText("%.1f s" %update_period)
        else:
            self.label_update_rate.setText("%.1f ms" %(update_period*1000))

    #call to update displayed delta value -EDT
    def delta_update(self, delta_list):
        self.label_delta_value.setText("%.2f " %delta_list)
    #call to update displayed DOA angle value
    def DOA_angle_update(self, DOA_angle):
        self.label_DOA_value.setText("%.2f " %DOA_angle)

    def spectrum_plot(self):
        xw1 = self.module_signal_processor.spectrum[1,:]
        xw2 = self.module_signal_processor.spectrum[2,:]
        xw3 = self.module_signal_processor.spectrum[3,:]
        xw4 = self.module_signal_processor.spectrum[4,:]
        freqs = self.module_signal_processor.spectrum[0,:]
        spectrum_dynamic_range = 10

        # HRG - BF Test
        iq1 = self.module_signal_processor.iq_data[1,:]
        iq2 = self.module_signal_processor.iq_data[2,:]
        iq3 = self.module_signal_processor.iq_data[3,:]
        iq4 = self.module_signal_processor.iq_data[4,:]
        summation_iq = iq1 + iq2 + iq3 + iq4

        psd_iq = 10*np.log10(np.fft.fftshift(np.abs(np.fft.fft(summation_iq))))

        self.spectrum_ch1_curve.setData(freqs, xw1)
        self.spectrum_ch2_curve.setData(freqs, xw2)
        self.spectrum_ch3_curve.setData(freqs, xw3)
        #self.spectrum_ch4_curve.setData(freqs, xw4)
        self.spectrum_ch4_curve.setData(freqs, psd_iq)

        currentTime = time.time()
        if((currentTime - self.spectrum_time) > 0.5):
            self.spectrum_time = currentTime
            self.export_spectrum.export('/ram/spectrum.jpg')

    def delay_plot(self):

        xcorr12 = 10*np.log10(np.abs(self.module_signal_processor.xcorr[0,:]))
        xcorr13 = 10*np.log10(np.abs(self.module_signal_processor.xcorr[1,:]))
        xcorr14 = 10*np.log10(np.abs(self.module_signal_processor.xcorr[2,:]))

        phasor12 =self.module_signal_processor.phasors[0,:]
        phasor13 =self.module_signal_processor.phasors[1,:]
        phasor14 =self.module_signal_processor.phasors[2,:]

        N = np.size(xcorr12)//2

        xcorr12 -= np.max(xcorr12)
        xcorr13 -= np.max(xcorr13)
        xcorr14 -= np.max(xcorr14)

        #phasor12 /= np.max(np.abs(phasor12))
        #phasor13 /= np.max(np.abs(phasor13))
        #phasor14 /= np.max(np.abs(phasor14))

        M = 500
        max_delay = np.max(np.abs(self.module_signal_processor.delay_log[:,-1]))
        if max_delay+50 > M:
            M=max_delay+50

        delay_label = np.arange(-M,M+1,1)

#        if(xcorr12[0] != 0 and xcorr13[0] != 0 and xcorr14[0] != 0):
        self.plotWidget_sync_absx.clear()

        self.plotWidget_sync_absx.plot(delay_label, xcorr12[N-M:N+M+1], pen='b')
        self.plotWidget_sync_absx.plot(delay_label, xcorr13[N-M:N+M+1], pen='r')
        self.plotWidget_sync_absx.plot(delay_label, xcorr14[N-M:N+M+1], pen='g')

        # Plot delay history

        self.plotWidget_sync_sampd.clear()

        self.plotWidget_sync_sampd.plot(self.module_signal_processor.delay_log[0,:], pen='b')
        self.plotWidget_sync_sampd.plot(self.module_signal_processor.delay_log[1,:], pen='r')
        self.plotWidget_sync_sampd.plot(self.module_signal_processor.delay_log[2,:], pen='g')


        # Plot phasors
        # For averaged phasors
        #self.plotWidget_sync_normph.clear()
        #self.plotWidget_sync_normph.plot(np.cos(np.deg2rad(self.module_signal_processor.phase_log[0,:])), np.sin(np.deg2rad(self.module_signal_processor.phase_log[0,:])), pen=None, symbol='o', symbolBrush=(100,100,255,50))
        #self.plotWidget_sync_normph.plot(np.cos(np.deg2rad(self.module_signal_processor.phase_log[0,:])), np.sin(np.deg2rad(self.module_signal_processor.phase_log[0,:])), pen=None, symbol='o', symbolBrush=(150,150,150,50))
        #self.plotWidget_sync_normph.plot(np.cos(np.deg2rad(self.module_signal_processor.phase_log[0,:])), np.sin(np.deg2rad(self.module_signal_processor.phase_log[0,:])), pen=None, symbol='o', symbolBrush=(50,50,50,50))

        # Plot phase history

        self.plotWidget_sync_phasediff.clear()

        self.plotWidget_sync_phasediff.plot(self.module_signal_processor.phase_log[0,:], pen='b')
        self.plotWidget_sync_phasediff.plot(self.module_signal_processor.phase_log[1,:], pen='r')
        self.plotWidget_sync_phasediff.plot(self.module_signal_processor.phase_log[2,:], pen='g')

        currentTime = time.time()
        if((currentTime - self.sync_time) > 0.5):
            self.sync_time = currentTime
            self.export_sync.export('/ram/sync.jpg')

    def DOA_plot_helper(self, DOA_data, incident_angles, log_scale_min=None, color=(0, 45, 98), legend=None):

        DOA_data = np.divide(np.abs(DOA_data), np.max(np.abs(DOA_data))) # normalization
        if(log_scale_min != None):
            DOA_data = 10*np.log10(DOA_data)
            theta_index = 0
            for theta in incident_angles:
                if DOA_data[theta_index] < log_scale_min:
                    DOA_data[theta_index] = log_scale_min
                theta_index += 1

        plot = self.plotWidget_DOA.plot(incident_angles, DOA_data, pen=pg.mkPen(color, width=2))
        return DOA_data
    
    def DOA_plot(self):

        thetas =  self.module_signal_processor.scan_vol
        MUSIC  = self.module_signal_processor.DOA_MUSIC_res

        DOA = 0
        DOA_results = []
        COMBINED = np.zeros_like(thetas, dtype=np.complex)

        self.plotWidget_DOA.clear()

        if self.module_signal_processor.en_DOA_MUSIC:

            self.DOA_plot_helper(MUSIC, thetas, log_scale_min = -50, color=(0, 45, 98))
            COMBINED += np.divide(np.abs(MUSIC),np.max(np.abs(MUSIC)))
            #de.DOA_plot(MUSIC, thetas, log_scale_min = -50, axes=self.axes_DOA)
            DOA_results.append(thetas[np.argmax(MUSIC)])

            # PHASE SHIFT CALCULATION
            DOA_angle = self.module_signal_processor.DOA_angle
            delta_list  = self.module_signal_processor.delta_list ####### -------------------------------- PHASE SHIFT Value!!!


        #COMBINED_LOG = 10*np.log10(COMBINED)

        if len(DOA_results) != 0:

            # Combined Graph (beta)
            COMBINED_LOG = self.DOA_plot_helper(COMBINED, thetas, log_scale_min = -50, color=(0, 45, 98))

            confidence = scipy.signal.find_peaks_cwt(COMBINED_LOG, np.arange(10,30), min_snr=1) #np.max(DOA_combined**2) / np.average(DOA_combined**2)
            maxIndex = confidence[np.argmax(COMBINED_LOG[confidence])]
            confidence_sum = 0

            #print("Peaks: " + str(confidence))
            for val in confidence:
               if(val != maxIndex and np.abs(COMBINED_LOG[val] - min(COMBINED_LOG)) > np.abs(min(COMBINED_LOG))*0.25):
                  #print("Doing other peaks: " + str(val) + "combined value: " + str(COMBINED_LOG[val]))
                  confidence_sum += 1/(np.abs(COMBINED_LOG[val]))
               elif val == maxIndex:
                  #print("Doing maxIndex peak: " + str(maxIndex) + "min combined: " + str(min(COMBINED_LOG)))
                  confidence_sum += 1/np.abs(min(COMBINED_LOG))
            # Get avg power level
            max_power_level = np.max(self.module_signal_processor.spectrum[1,:])
            #rms_power_level = np.sqrt(np.mean(self.module_signal_processor.spectrum[1,:]**2))

            confidence_sum = 10/confidence_sum

            #print("Max Power Level" + str(max_power_level))
            #print("Confidence Sum: " + str(confidence_sum))

            DOA_results = np.array(DOA_results)
            # Convert measured DOAs to complex numbers
            DOA_results_c = np.exp(1j*np.deg2rad(DOA_results))
            # Average measured DOA angles
            DOA_avg_c = np.average(DOA_results_c)
            # Convert back to degree
            DOA = np.rad2deg(np.angle(DOA_avg_c))


        currentTime = time.time()
        if((currentTime - self.DOA_time) > 0.5):
            self.DOA_time = currentTime
            self.export_DOA.export('/ram/doa.jpg')

app = QApplication(sys.argv)
form = MainWindow()
form.show()

def init_settings():

    # Receiver Configuration
    center_freq = settings.center_freq
    samp_index = settings.samp_index
    uniform_gain = settings.uniform_gain
    gain_index = settings.gain_index
    gain_index_2 = settings.gain_index_2
    gain_index_3 = settings.gain_index_3
    gain_index_4 = settings.gain_index_4

    form.doubleSpinBox_center_freq.setProperty("value", center_freq)
    form.comboBox_sampling_freq.setCurrentIndex(int(samp_index))
    form.checkBox_en_uniform_gain.setChecked(True if uniform_gain=="on" else False)
    form.comboBox_gain.setCurrentIndex(int(gain_index))
    form.comboBox_gain_2.setCurrentIndex(int(gain_index))
    form.comboBox_gain_3.setCurrentIndex(int(gain_index))
    form.comboBox_gain_4.setCurrentIndex(int(gain_index))

    # IQ Preprocessing
    dc_comp = settings.dc_comp
    filt_bw = settings.filt_bw
    fir_size = settings.fir_size
    decimation = settings.decimation

    form.checkBox_en_dc_compensation.setChecked(True if dc_comp=="on" else False)
    form.doubleSpinBox_filterbw.setProperty("value", filt_bw)
    form.spinBox_fir_tap_size.setProperty("value", fir_size)
    form.spinBox_decimation.setProperty("value", decimation)


    # Sync
    en_sync = "off" #settings.en_sync
    en_noise = "off" #settings.en_noise

    form.checkBox_en_sync_display.setChecked(True if en_sync=="on" else False)
    form.checkBox_en_noise_source.setChecked(True if en_noise=="on" else False)

    # DOA Estimation
    ant_arrangement_index = settings.ant_arrangement_index
    ant_spacing = settings.ant_spacing
    en_doa = "off" #settings.en_doa
    en_MUSIC = settings.en_MUSIC
    en_fbavg = settings.en_fbavg # fb-alg
    en_PhaseShifter = settings.en_PhaseShifter # RED

    form.comboBox_antenna_alignment.setCurrentIndex(int(ant_arrangement_index))
    form.doubleSpinBox_DOA_d.setProperty("value", ant_spacing)
    form.checkBox_en_DOA.setChecked(True if en_doa=="on" else False)
    form.checkBox_en_DOA_MUSIC.setChecked(True if en_MUSIC=="on" else False)
    form.checkBox_en_DOA_FB_avg.setChecked(True if en_fbavg=="on" else False) # fb-alg    
    form.checkBox_en_PhaseShifter.setChecked(True if en_PhaseShifter=="on" else False) # Phase Shifter Configuration - RED


def reboot_program():
    form.module_receiver.close()
    subprocess.call(['./run.sh'])

#@route('/static/:path#.+#', name='static')
#def static(path):
    #return static_file(path, root='static')

@route('/static/<filepath:path>', name='static')
def server_static(filepath):
    return static_file(filepath, root='./static')

## ADDED DOA
@get('/doa')
def doa():
    ant_arrangement_index = int(form.comboBox_antenna_alignment.currentIndex())
    ant_meters = form.doubleSpinBox_DOA_d.value()
    en_doa = form.checkBox_en_DOA.checkState()
    en_MUSIC = form.checkBox_en_DOA_MUSIC.checkState()
    en_fbavg = form.checkBox_en_DOA_FB_avg.checkState() # fb-alg
    en_PhaseShifter = form.checkBox_en_PhaseShifter.checkState() # RED
    ip_addr = form.ip_addr

    return template ('doa.tpl', {'ant_arrangement_index':ant_arrangement_index,
#				'ant_spacing':ant_spacing,
                'ant_meters' :ant_meters,
				'en_doa':en_doa,
				'en_MUSIC':en_MUSIC,
				'en_fbavg':en_fbavg,
                'en_PhaseShifter':en_PhaseShifter,
				'ip_addr':ip_addr})


@post('/doa')
def do_doa():
    ant_arrangement_index = request.forms.get('ant_arrangement')
    form.comboBox_antenna_alignment.setCurrentIndex(int(ant_arrangement_index))

    ant_spacing = request.forms.get('ant_spacing')
    form.doubleSpinBox_DOA_d.setProperty("value", ant_spacing)

    en_doa = request.forms.get('en_doa')
    form.checkBox_en_DOA.setChecked(True if en_doa=="on" else False)

    en_MUSIC = request.forms.get('en_MUSIC')
    form.checkBox_en_DOA_MUSIC.setChecked(True if en_MUSIC=="on" else False)

    # fb-alg
    en_fbavg = request.forms.get('en_fbavg')
    form.checkBox_en_DOA_FB_avg.setChecked(True if en_fbavg=="on" else False)

    # phase shifter configuration - REDOLD
    en_PhaseShifter = request.forms.get('en_PhaseShifter')
    form.checkBox_en_PhaseShifter.setChecked(True if en_PhaseShifter=="on" else False)

    # Phase Shifter Configuration - RED
    if en_PhaseShifter == "on":
        print("in progress")
        # do something
    else: 
        # do something else
        print("in progress")

    settings.ant_arrangement_index = ant_arrangement_index
    settings.ant_spacing = ant_spacing
    settings.en_doa = en_doa
    settings.en_MUSIC = en_MUSIC
    settings.en_fbavg = en_fbavg # fb-alg
    settings.en_PhaseShifter = en_PhaseShifter # RED
    form.set_DOA_params()

    settings.write()
    return redirect('doa')
# END ADDED

@get('/sync')
def sync():
    en_sync = form.checkBox_en_sync_display.checkState()
    en_noise = form.checkBox_en_noise_source.checkState()
    ip_addr = form.ip_addr
    return template ('sync.tpl', {'en_sync':en_sync,
				'en_noise':en_noise,
				'ip_addr':ip_addr})


@post('/sync')
def do_sync():

    if (request.POST.get('enable_all_sync') == 'enable_all_sync'):
        current_sync = form.checkBox_en_sync_display.checkState()
        current_noise = form.checkBox_en_noise_source.checkState()
        if (current_sync == False) and (current_noise == False):
            form.checkBox_en_sync_display.setChecked(True)
            form.checkBox_en_noise_source.setChecked(True)
        else:
            form.checkBox_en_sync_display.setChecked(False)
            form.checkBox_en_noise_source.setChecked(False)

        form.switch_noise_source()
        form.set_sync_params()

    if (request.POST.get('update_sync') == 'update_sync'):
        en_sync = request.forms.get('en_sync')
        form.checkBox_en_sync_display.setChecked(True if en_sync=="on" else False)

        en_noise = request.forms.get('en_noise')
        form.checkBox_en_noise_source.setChecked(True if en_noise=="on" else False)

        settings.en_sync = en_sync
        settings.en_noise = en_noise
        form.switch_noise_source()
        form.set_sync_params()

    if (request.POST.get('del_hist') == 'del_hist'):
        form.pb_del_sync_history_clicked()

    if (request.POST.get('samp_sync') == 'samp_sync'):
        form.pb_sync_clicked()

    if (request.POST.get('cal_iq') == 'cal_iq'):
        form.pb_calibrate_iq_clicked()

    settings.write()
    return redirect('sync')

@get('/')
@get('/init')
def init():
    center_freq = form.doubleSpinBox_center_freq.value()
    samp_index = int(form.comboBox_sampling_freq.currentIndex())
    uniform_gain = form.checkBox_en_uniform_gain.checkState()
    #en_PhaseShifter = form.checkBox_en_PhaseShifter.checkState() # REDOLD
    gain_index = int(form.comboBox_gain.currentIndex())
    gain_index_2 = int(form.comboBox_gain_2.currentIndex())
    gain_index_3 = int(form.comboBox_gain_3.currentIndex())
    gain_index_4 = int(form.comboBox_gain_4.currentIndex())
    dc_comp = form.checkBox_en_dc_compensation.checkState()
    filt_bw = form.doubleSpinBox_filterbw.value()
    fir_size = form.spinBox_fir_tap_size.value()
    decimation = form.spinBox_decimation.value()
    ip_addr = form.ip_addr

    return template ('init.tpl', {'center_freq':center_freq,
				'samp_index':samp_index,
                'uniform_gain':uniform_gain,
				'gain_index':gain_index,
				'gain_index_2':gain_index_2,
				'gain_index_3':gain_index_3,
				'gain_index_4':gain_index_4,
				'dc_comp':dc_comp,
				'filt_bw':filt_bw,
				'fir_size':fir_size,
				'decimation':decimation,
                #'en_PhaseShifter':en_PhaseShifter,
				'ip_addr':ip_addr})

@post('/init') # or @route('/login', method='POST')
def do_init():
    if (request.POST.get('rcv_params') == 'rcv_params'):
        center_freq = request.forms.get('center_freq')
        form.doubleSpinBox_center_freq.setProperty("value", center_freq)

        samp_index = request.forms.get('samp_freq')
        form.comboBox_sampling_freq.setCurrentIndex(int(samp_index))

        uniform_gain = request.forms.get('uniform_gain')
        form.checkBox_en_uniform_gain.setChecked(True if uniform_gain=="on" else False)

        # phase shifter configuration - REDOLD
        #en_PhaseShifter = request.forms.get('en_PhaseShifter')
        #form.checkBox_en_PhaseShifter.setChecked(True if en_PhaseShifter=="on" else False)

        if uniform_gain == "on":
            gain_index = request.forms.get('gain')
            form.comboBox_gain.setCurrentIndex(int(gain_index))
            gain_index_2 = request.forms.get('gain')
            form.comboBox_gain_2.setCurrentIndex(int(gain_index))
            gain_index_3 = request.forms.get('gain')
            form.comboBox_gain_3.setCurrentIndex(int(gain_index))
            gain_index_4 = request.forms.get('gain')
            form.comboBox_gain_4.setCurrentIndex(int(gain_index))
        else:
            gain_index = request.forms.get('gain')
            form.comboBox_gain.setCurrentIndex(int(gain_index))
            gain_index_2 = request.forms.get('gain_2')
            form.comboBox_gain_2.setCurrentIndex(int(gain_index_2))
            gain_index_3 = request.forms.get('gain_3')
            form.comboBox_gain_3.setCurrentIndex(int(gain_index_3))
            gain_index_4 = request.forms.get('gain_4')
            form.comboBox_gain_4.setCurrentIndex(int(gain_index_4))

        # Phase Shifter Configuration - REDOLD
        '''
        if en_PhaseShifter == "on":
            print("in progress")
            # do something
        else: 
            # do something else
            print("in progress")
        '''

        settings.center_freq = center_freq
        settings.samp_index = samp_index
        settings.uniform_gain = uniform_gain
        #settings.en_PhaseShifter = en_PhaseShifter # REDOLD
        settings.gain_index = gain_index
        settings.gain_index_2 = gain_index_2
        settings.gain_index_3 = gain_index_3
        settings.gain_index_4 = gain_index_4
        form.pb_rec_reconfig_clicked()


    if (request.POST.get('iq_params') == 'iq_params'):
        dc_comp = request.forms.get('dc_comp')
        form.checkBox_en_dc_compensation.setChecked(True if dc_comp=="on" else False)

        filt_bw = request.forms.get('filt_bw')
        form.doubleSpinBox_filterbw.setProperty("value", filt_bw)

        fir_size = request.forms.get('fir_size')
        form.spinBox_fir_tap_size.setProperty("value", fir_size)

        decimation = request.forms.get('decimation')
        form.spinBox_decimation.setProperty("value", decimation)

        settings.dc_comp = dc_comp
        settings.filt_bw = filt_bw
        settings.fir_size = fir_size
        settings.decimation = decimation
        form.set_iq_preprocessing_params()

    if (request.POST.get('start') == 'start'):
        form.module_signal_processor.start()
        form.pushButton_proc_control.setText("Stop processing")

    if (request.POST.get('stop') == 'stop'):
        form.module_signal_processor.stop()
        form.pushButton_proc_control.setText("Start processing")

    if (request.POST.get('start_spec') == 'start_spec'):
        form.checkBox_en_spectrum.setChecked(True)
        form.set_spectrum_params()

    if (request.POST.get('stop_spec') == 'stop_spec'):
        form.checkBox_en_spectrum.setChecked(False)
        form.set_spectrum_params()

    if (request.POST.get('reboot') == 'reboot'):
        reboot_program()

    settings.write()

    return redirect('init')

@get('/stats')
def stats():

    upd_rate = form.label_update_rate.text()

    if(form.module_receiver.overdrive_detect_flag):
       ovr_drv = "YES"
    else:
       ovr_drv = "NO"

    return template ('stats.tpl', {'upd_rate':upd_rate,
				'ovr_drv':ovr_drv})

init_settings()
app.exec_()
