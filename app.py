import sys
from datetime import datetime
from configparser import ConfigParser
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QSlider,
                             QTabWidget, QTextEdit, QMenu, QMenuBar, QToolButton, QStatusBar,
                             QHBoxLayout, QVBoxLayout, QFormLayout)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QEvent, QRect
from PyQt6.QtGui import QIcon
from openai_playground import OpenAIPlayground

class AIAssistant(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.openai_playground = OpenAIPlayground(API_KEY)

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.init_ui()

    def init_ui(self):
        #add sub layout manager
        self.layout['inputs'] = QFormLayout()
        self.layout['main'].addLayout(self.layout['inputs'])

        #add textbox
        self.prompt = QTextEdit()
        self.output = QTextEdit()

        #Add Sliders
        self.max_tokens = QSlider(Qt.Orientation.Horizontal, minimum=10, maximum=4000, singleStep=500, pageStep=500, value=100)
        self.temperature = QSlider(Qt.Orientation.Horizontal, minimum=0, maximum=200)
        self.presence_penalty = QSlider(Qt.Orientation.Horizontal, minimum=0, maximum=200)

        #add buttons
        self.btn_submit = QPushButton('&Submit', clicked=self.submit)
        self.tbn_reset = QPushButton('&Reset', clicked=self.reset_fields)

        #add status bar
        self.status = QStatusBar()

        #organize widgets
        #----------------
        #maximum token slider
        self.max_tokens_values = QLabel('0.0')
        self.layout['slider_layout'] = QHBoxLayout()
        self.layout['slider_layout'].addWidget(self.max_tokens_values)
        self.layout['slider_layout'].addWidget(self.max_tokens)
        self.layout['inputs'].addRow(QLabel('Max Token:'), self.layout['slider_layout'])

        #temperature slider
        self.temperature_value = QLabel('0.0')

class TabManager(QTabWidget):
    #add customized signals
    plusClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        #add event filter
        self.tabBar().installEventFilter(self)
        
        #add tab close button
        self.setTabsClosable(True)

        # Create the add tab button and implement signal's
        self.add_tab_button = QToolButton(self, text='+')
        self.add_tab_button.clicked.connect(self.plusClicked)

        self.tabCloseRequested.connect(self.closeTab)

    def closeTab(self, tab_index):
        if self.count() == 1:
            return
        self.removeTab(tab_index)
    
    def eventFilter(self, obj, event):
        # move add button to the last position
        if obj is self.tabBar() and event.type() == QEvent.Type.Resize:
            r = self.tabBar().geometry()
            h = r.height()
            self.add_tab_button.setFixedSize((h - 1.5) * QSize(1,1))
            self.add_tab_button.move(r.right() - 6, 1)
        return super().eventFilter(obj, event)
       
class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        #define window minimum size
        self.window_width, self.window_height = 700, 500
        self.setMinimumSize(self.window_width, self.window_height)

        # set window icon
        self.setWindowIcon(QIcon('chatgpt32_32.png'))

        #self window title
        self.setWindowTitle('AI Personal Assistant By Ozzy and OpenAI 1.0')
        
        #apply css style sheet (apply to alll child widgets)
        self.setStyleSheet('''
            QWidget{
                font-size: 15px;
            }
        ''')
        self.tab_index_tracker = 1
        self.layout = {}

        #set the windows layout manager 
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.init_ui()

    def init_ui(self):
        # add tab manager
        self.tab_manager = TabManager()
        self.layout['main'].addWidget(self.tab_manager)

        self.tab_manager.addTab(AIAssistant(), 'Conversation #{0}'.format(self.tab_index_tracker))


if __name__ == "__main__":
    #load OpenAI KEY
    config = ConfigParser()
    config.read('password_manager.ini')
    API_KEY = config.get('openai', 'API_KEY')

    #construct application instance
    app = QApplication(sys.argv)

    #launch app window
    app_window = AppWindow()
    app_window.show()
    sys.exit(app.exec())
