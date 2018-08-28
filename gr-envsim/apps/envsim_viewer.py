#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Envsim Viewer
# Generated: Thu Apr  5 16:10:46 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui


class envsim_viewer(gr.top_block, Qt.QWidget):

    def __init__(self, debug_ip='10.169.25.92', port_num=52005):
        gr.top_block.__init__(self, "Envsim Viewer")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Envsim Viewer")
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

        self.settings = Qt.QSettings("GNU Radio", "envsim_viewer")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.debug_ip = debug_ip
        self.port_num = port_num

        ##################################################
        # Variables
        ##################################################
        self.zmq_base_addr = zmq_base_addr = "tcp://" + debug_ip + ":"
        self.samp_rate = samp_rate = 1e6

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, zmq_base_addr+str(port_num), 100, False, -1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/25)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)




        ##################################################
        # Connections
        ##################################################
        self.connect((self.zeromq_pull_source_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "envsim_viewer")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_debug_ip(self):
        return self.debug_ip

    def set_debug_ip(self, debug_ip):
        self.debug_ip = debug_ip
        self.set_zmq_base_addr("tcp://" + self.debug_ip + ":")

    def get_port_num(self):
        return self.port_num

    def set_port_num(self, port_num):
        self.port_num = port_num

    def get_zmq_base_addr(self):
        return self.zmq_base_addr

    def set_zmq_base_addr(self, zmq_base_addr):
        self.zmq_base_addr = zmq_base_addr

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--debug-ip", dest="debug_ip", type="string", default='10.169.25.92',
        help="Set debug_ip [default=%default]")
    parser.add_option(
        "", "--port-num", dest="port_num", type="intx", default=52005,
        help="Set port_num [default=%default]")
    return parser


def main(top_block_cls=envsim_viewer, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(debug_ip=options.debug_ip, port_num=options.port_num)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
