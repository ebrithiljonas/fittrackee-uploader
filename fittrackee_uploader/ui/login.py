# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_LoginWindow:
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(400, 200)
        LoginWindow.setMinimumSize(QtCore.QSize(400, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_1 = QtWidgets.QLabel(parent=LoginWindow)
        self.label_1.setMinimumSize(QtCore.QSize(70, 0))
        self.label_1.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_1.setObjectName("label_1")
        self.horizontalLayout_6.addWidget(self.label_1)
        self.tbServer = QtWidgets.QLineEdit(parent=LoginWindow)
        self.tbServer.setObjectName("tbServer")
        self.horizontalLayout_6.addWidget(self.tbServer)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_2 = QtWidgets.QLabel(parent=LoginWindow)
        self.label_2.setMinimumSize(QtCore.QSize(70, 0))
        self.label_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_7.addWidget(self.label_2)
        self.tbEmail = QtWidgets.QLineEdit(parent=LoginWindow)
        self.tbEmail.setObjectName("tbEmail")
        self.horizontalLayout_7.addWidget(self.tbEmail)
        self.horizontalLayout_7.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_3 = QtWidgets.QLabel(parent=LoginWindow)
        self.label_3.setMinimumSize(QtCore.QSize(70, 0))
        self.label_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_8.addWidget(self.label_3)
        self.tbPassword = QtWidgets.QLineEdit(parent=LoginWindow)
        self.tbPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.tbPassword.setObjectName("tbPassword")
        self.horizontalLayout_8.addWidget(self.tbPassword)
        self.horizontalLayout_8.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.widget = QtWidgets.QWidget(parent=LoginWindow)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btCancel = QtWidgets.QPushButton(parent=LoginWindow)
        self.btCancel.setMinimumSize(QtCore.QSize(100, 0))
        self.btCancel.setObjectName("btCancel")
        self.horizontalLayout_5.addWidget(self.btCancel)
        self.widget_2 = QtWidgets.QWidget(parent=LoginWindow)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_5.addWidget(self.widget_2)
        self.btLogin = QtWidgets.QPushButton(parent=LoginWindow)
        self.btLogin.setMinimumSize(QtCore.QSize(100, 0))
        self.btLogin.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btLogin.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btLogin.setObjectName("btLogin")
        self.horizontalLayout_5.addWidget(self.btLogin)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout.setStretch(3, 1)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.label_1.setText(_translate("LoginWindow", "Server URL"))
        self.label_2.setText(_translate("LoginWindow", "Email"))
        self.label_3.setText(_translate("LoginWindow", "Password"))
        self.btCancel.setText(_translate("LoginWindow", "Cancel"))
        self.btLogin.setText(_translate("LoginWindow", "Login"))
