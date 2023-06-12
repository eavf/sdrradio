#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AM TX
# Author: EaVF
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import osmosdr
import time



from gnuradio import qtgui

class amtx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AM TX", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AM TX")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "amtx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.tx_freq = tx_freq = 435
        self.sig_amp = sig_amp = 0.1
        self.samp_rate_sdr = samp_rate_sdr = 3e6
        self.samp_rate = samp_rate = 48000
        self.rf_gain = rf_gain = 12
        self.if_gain = if_gain = 20
        self.bb_gain = bb_gain = 2
        self.audio_freq = audio_freq = 250

        ##################################################
        # Blocks
        ##################################################

        self._tx_freq_tool_bar = Qt.QToolBar(self)
        self._tx_freq_tool_bar.addWidget(Qt.QLabel("TX Frequency (MHz)" + ": "))
        self._tx_freq_line_edit = Qt.QLineEdit(str(self.tx_freq))
        self._tx_freq_tool_bar.addWidget(self._tx_freq_line_edit)
        self._tx_freq_line_edit.returnPressed.connect(
            lambda: self.set_tx_freq(eng_notation.str_to_num(str(self._tx_freq_line_edit.text()))))
        self.top_layout.addWidget(self._tx_freq_tool_bar)
        self._sig_amp_range = Range(0, 2, 0.1, 0.1, 200)
        self._sig_amp_win = RangeWidget(self._sig_amp_range, self.set_sig_amp, "Signal Source level", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sig_amp_win)
        self._rf_gain_range = Range(0, 25, 1, 12, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_win)
        self._if_gain_range = Range(0, 25, 1, 20, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "IF Gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._if_gain_win)
        self._bb_gain_range = Range(0, 25, 1, 2, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "Baseband Gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bb_gain_win)
        self._audio_freq_range = Range(100, 3000, 50, 250, 200)
        self._audio_freq_win = RangeWidget(self._audio_freq_range, self.set_audio_freq, "Audio Frequency", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._audio_freq_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + 'hackrf=708061dc211a5a4b'
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate_sdr)
        self.osmosdr_sink_0.set_center_freq((tx_freq*1e6), 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, (samp_rate/samp_rate_sdr))
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(1)
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                20,
                samp_rate,
                100,
                3000,
                500,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 48e3, 0.5, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, audio_freq, sig_amp, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.osmosdr_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "amtx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        Qt.QMetaObject.invokeMethod(self._tx_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.tx_freq)))
        self.osmosdr_sink_0.set_center_freq((self.tx_freq*1e6), 0)

    def get_sig_amp(self):
        return self.sig_amp

    def set_sig_amp(self, sig_amp):
        self.sig_amp = sig_amp
        self.analog_sig_source_x_0.set_amplitude(self.sig_amp)

    def get_samp_rate_sdr(self):
        return self.samp_rate_sdr

    def set_samp_rate_sdr(self, samp_rate_sdr):
        self.samp_rate_sdr = samp_rate_sdr
        self.mmse_resampler_xx_0.set_resamp_ratio((self.samp_rate/self.samp_rate_sdr))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate_sdr)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(20, self.samp_rate, 100, 3000, 500, window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio((self.samp_rate/self.samp_rate_sdr))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0.set_if_gain(self.if_gain, 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_sink_0.set_bb_gain(self.bb_gain, 0)

    def get_audio_freq(self):
        return self.audio_freq

    def set_audio_freq(self, audio_freq):
        self.audio_freq = audio_freq
        self.analog_sig_source_x_0.set_frequency(self.audio_freq)




def main(top_block_cls=amtx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
