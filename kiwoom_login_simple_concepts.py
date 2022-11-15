from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import sys

def comm_connect(err_code):
    if err_code == 0:
        print('Succussfully logged in')
    else:
        print('Login Failed')
    
    login_loop.exit()
    print('login_loop exited')


app = QApplication(sys.argv)

kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
kiwoom.OnEventConnect.connect(comm_connect)
login_loop = QEventLoop()

kiwoom.dynamicCall('CommConnect')
login_loop.exec_()

app.exec_()
