import sys
import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from process_miner import visualizer
from .centralWidget import Ui_centralWidget
import global_util
from process_miner.visualizer import Pm4pyTools
from process_miner.calculate import Filter, Calculate, Evaluation
from process_miner.model import Model, Accuracy
from process_miner.weight import TimeWeight, StorageWeight, AccuracyWeight, WeightSetting
from pm4py.objects.log.log import EventLog, Trace, Event

class ProMWidget(QWidget, Ui_centralWidget):
    def __init__(self):
        super().__init__()
        # loadUi("./centralWidget.ui", self)  # import UI file
        self.setupUi(self)
        self.pushButtonOpen.clicked.connect(self.slot_btn_open_file)
        self.pushButtonRun.clicked.connect(self.slot_btn_show_result)
        self.pushButtonSubmit.clicked.connect(self.slot_btn_submit_weight)
        self.file = ""
        self.timeWeight = 0
        self.storageWeight = 0
        self.variationWeight = 0
        self.best_filter = None
        self.selectedMiner = None

    @pyqtSlot()
    def slot_btn_open_file(self):
        self.file, file_type = QFileDialog.getOpenFileName(self, 'open file', './input_file', '*.xes;;*.csv;;')
        print("opened input file: %s" % self.file)

    @pyqtSlot()
    def slot_btn_show_result(self):
        if self.timeWeight == 0 and self.storageWeight == 0 and self.variationWeight == 0:
            print("submit is not clicked")
            QMessageBox().information(self, "weight not set", "please open file first, then set weight and submit")
            return
        else:
            print("time:%s" % self.timeWeight)
            print("performance:%s" % self.storageWeight)
            print("variation:%s" % self.variationWeight)

        # Get tool object
        tools = Pm4pyTools(self.file)
        log = tools.get_xes_log()

        # Get the time list of all events
        timestamps = tools.get_all_sorted_time()

        # If this is greater than 0, follow this
        filtered_log = None
        if self.variationWeight > 0:
            print("timestamps.len: %s, timestamps.data: %s" % (len(timestamps), timestamps))
            try:
                tools.set_log(log)
                filtered_log = tools.filter_time_data(timestamps, self.variationWeight)
            except Exception as e:
                QMessageBox().warning(self, "filtered error", e.__str__())
                return
        else:
            # Follow the time and case rules
            if self.timeWeight > 0 and self.storageWeight > 0:
                retain = int(len(timestamps) * self.timeWeight * self.storageWeight)
                if retain == 0:
                    QMessageBox().warning(self, "input error", "retain data is too low")
                    return

            # If the time weight is greater than 0, perform time filtering
            if self.timeWeight > 0:
                print("timestamps.len: %s, timestamps.data: %s" % (len(timestamps), timestamps))
                try:
                    tools.set_log(log)
                    filtered_log = tools.filter_time_data(timestamps, self.timeWeight)
                except Exception as e:
                    QMessageBox(self, "filtered error", e)
                    return

            # case filter
            if self.storageWeight > 0:
                if filtered_log is not None:
                    # continue filtering
                    tools.set_log(filtered_log)
                    timestamps = tools.get_all_sorted_time()
                    filtered_log = tools.filter_time_data(timestamps, self.storageWeight)
                else:
                    # filter by using the original data
                    tools.set_log(log)
                    filtered_log = tools.filter_time_data(timestamps, self.storageWeight)

        print("filtered_log: %s" % filtered_log)
        output = tools.show_log(filtered_log)
        print(output)

        output_full_name = global_util.get_full_path_output_file(output)
        png = QPixmap(output_full_name).scaled(self.labelImage.width(), self.labelImage.height())
        self.labelImage.setPixmap(png)

    @pyqtSlot()
    def slot_btn_submit_weight(self):
        self.timeWeight = float(self.doubleSpinBoxTime.text())
        self.storageWeight = float(self.doubleSpinBoxStoracy.text())
        self.variationWeight = float(self.doubleSpinBoxAccuracy.text())

    def __set_filter(self, best_filter):
        self.best_filter = best_filter
