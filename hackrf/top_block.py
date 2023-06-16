#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
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

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

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
        self.volume_slider = volume_slider = 25
        self.stat_chooser = stat_chooser = 89.45e6
        self.samp_rate = samp_rate = 2e6
        self.rfgain = rfgain = 15
        self.down_rate = down_rate = 250e3

        ##################################################
        # Blocks
        ##################################################

        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'tuner')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'audio')
        self.top_layout.addWidget(self.tab)
        self._volume_slider_range = Range(0, 100, 1, 25, 200)
        self._volume_slider_win = RangeWidget(self._volume_slider_range, self.set_volume_slider, "Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tab_layout_1.addWidget(self._volume_slider_win)
        # Create the options list
        self._stat_chooser_options = [89450000.0, 100000000.0, 92100000.0, 96100000.0, 104700000.0, 103700000.0, 21438.0]
        # Create the labels list
        self._stat_chooser_labels = ['NoName', 'Nostalgie', 'RC Brussels', 'La Premiere', 'Fun Radio', 'NRJ', 'Armada Russe']
        # Create the combo box
        self._stat_chooser_tool_bar = Qt.QToolBar(self)
        self._stat_chooser_tool_bar.addWidget(Qt.QLabel("Station Chooser" + ": "))
        self._stat_chooser_combo_box = Qt.QComboBox()
        self._stat_chooser_tool_bar.addWidget(self._stat_chooser_combo_box)
        for _label in self._stat_chooser_labels: self._stat_chooser_combo_box.addItem(_label)
        self._stat_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._stat_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._stat_chooser_options.index(i)))
        self._stat_chooser_callback(self.stat_chooser)
        self._stat_chooser_combo_box.currentIndexChanged.connect(
            lambda i: self.set_stat_chooser(self._stat_chooser_options[i]))
        # Create the radio buttons
        self.tab_layout_0.addWidget(self._stat_chooser_tool_bar)
        self._rfgain_range = Range(0, 40, 8, 15, 200)
        self._rfgain_win = RangeWidget(self._rfgain_range, self.set_rfgain, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tab_layout_0.addWidget(self._rfgain_win)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, stat_chooser)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(rfgain, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(20, 0.0), 62.0))
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=24,
                decimation=250,
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            stat_chooser, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            down_rate, #bw
            "Demod out", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            (int(samp_rate/down_rate)),
            firdes.low_pass(
                2,
                samp_rate,
                100e3,
                10e3,
                window.WIN_KAISER,
                6.76))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff((volume_slider/100))
        self.audio_sink_0 = audio.sink(24000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=down_rate,
        	audio_decimation=1,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.qtgui_freq_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_volume_slider(self):
        return self.volume_slider

    def set_volume_slider(self, volume_slider):
        self.volume_slider = volume_slider
        self.blocks_multiply_const_vxx_1.set_k((self.volume_slider/100))

    def get_stat_chooser(self):
        return self.stat_chooser

    def set_stat_chooser(self, stat_chooser):
        self.stat_chooser = stat_chooser
        self._stat_chooser_callback(self.stat_chooser)
        self.qtgui_freq_sink_x_1.set_frequency_range(self.stat_chooser, self.samp_rate)
        self.soapy_hackrf_source_0.set_frequency(0, self.stat_chooser)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(2, self.samp_rate, 100e3, 10e3, window.WIN_KAISER, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range(self.stat_chooser, self.samp_rate)
        self.soapy_hackrf_source_0.set_sample_rate(0, self.samp_rate)

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(self.rfgain, 0.0), 40.0))

    def get_down_rate(self):
        return self.down_rate

    def set_down_rate(self, down_rate):
        self.down_rate = down_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.down_rate)




def main(top_block_cls=top_block, options=None):

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
