#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class RadioSpectrumAnalyser(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "RadioSpectrumAnalyser")

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
        self.tuning = tuning = 102100000
        self.samp_rate = samp_rate = 1e6
        self.rf_gain_0 = rf_gain_0 = 50
        self.rf_gain = rf_gain = 50

        ##################################################
        # Blocks
        ##################################################

        self._tuning_range = Range(70000000, 6000000000, 200000, 102100000, 200)
        self._tuning_win = RangeWidget(self._tuning_range, self.set_tuning, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tuning_win)
        self._samp_rate_range = Range(1e6, 20e6, 1e6, 1e6, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "Sample Rate", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._samp_rate_win)
        self._rf_gain_0_range = Range(0, 76, 1, 50, 200)
        self._rf_gain_0_win = RangeWidget(self._rf_gain_0_range, self.set_rf_gain_0, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_0_win)
        self._rf_gain_range = Range(0, 76, 1, 50, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_win)
        self.soapy_hackrf_source_1 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_1 = soapy.source(dev, "fc32", 1, 'hackrf=0',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_1.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_1.set_bandwidth(0, samp_rate)
        self.soapy_hackrf_source_1.set_frequency(0, tuning)
        self.soapy_hackrf_source_1.set_gain(0, 'AMP', False)
        self.soapy_hackrf_source_1.set_gain(0, 'LNA', min(max(rf_gain, 0.0), 40.0))
        self.soapy_hackrf_source_1.set_gain(0, 'VGA', min(max(rf_gain_0, 0.0), 62.0))
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            tuning, #fc
            samp_rate, #bw
            "Spectrum Analyser", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_sink_x_0_0, 'freq'), (self.soapy_hackrf_source_1, 'cmd'))
        self.connect((self.soapy_hackrf_source_1, 0), (self.qtgui_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RadioSpectrumAnalyser")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.qtgui_sink_x_0_0.set_frequency_range(self.tuning, self.samp_rate)
        self.soapy_hackrf_source_1.set_frequency(0, self.tuning)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0_0.set_frequency_range(self.tuning, self.samp_rate)
        self.soapy_hackrf_source_1.set_sample_rate(0, self.samp_rate)
        self.soapy_hackrf_source_1.set_bandwidth(0, self.samp_rate)

    def get_rf_gain_0(self):
        return self.rf_gain_0

    def set_rf_gain_0(self, rf_gain_0):
        self.rf_gain_0 = rf_gain_0
        self.soapy_hackrf_source_1.set_gain(0, 'VGA', min(max(self.rf_gain_0, 0.0), 62.0))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.soapy_hackrf_source_1.set_gain(0, 'LNA', min(max(self.rf_gain, 0.0), 40.0))




def main(top_block_cls=RadioSpectrumAnalyser, options=None):

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
