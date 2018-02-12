# PyQt 逻辑类
# Python 3.6.3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from pyqt.ui_calculator import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # Bind signal and slot  信号和槽
        self.pushButton.clicked.connect(self.push_btn_click)

    def push_btn_click(self):
        ret_1 = int(self.textEdit.toPlainText())
        ret_2 = int(self.textEdit_2.toPlainText())
        plus_ret = ret_1 + ret_2
        self.textEdit_3.setText(str(plus_ret))
        # show in browser
        old_text = self.textBrowser.toPlainText()
        new_text = "%d + %d = %d \n" %(ret_1, ret_2, plus_ret)
        self.textBrowser.setText(old_text + new_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
