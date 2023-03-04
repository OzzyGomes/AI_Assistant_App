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
        self.init_configure_signals()
        self.init_set_default_settings()

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
        self.btn_reset = QPushButton('&Reset', clicked=self.reset_fields)

        #add status bar
        self.status = QStatusBar()

        #organize widgets
        #----------------
        #maximum token slider
        self.max_token_value = QLabel('0.0')
        self.layout['slider_layout'] = QHBoxLayout()
        self.layout['slider_layout'].addWidget(self.max_token_value)
        self.layout['slider_layout'].addWidget(self.max_tokens)
        self.layout['inputs'].addRow(QLabel('Max Token:'), self.layout['slider_layout'])

        #temperature slider
        self.temperature_value = QLabel('0.0')
        self.layout['slider_layout2'] = QHBoxLayout()
        self.layout['slider_layout2'].addWidget(self.temperature_value)
        self.layout['slider_layout2'].addWidget(self.temperature)
        self.layout['inputs'].addRow(QLabel('Temperature:'), self.layout['slider_layout2'])

        #presence penalty slider
        self.presence_penalty_value = QLabel('0.0')
        self.layout['slider_layout3'] = QHBoxLayout()
        self.layout['slider_layout3'].addWidget(self.presence_penalty_value)
        self.layout['slider_layout3'].addWidget(self.presence_penalty)
        self.layout['inputs'].addRow(QLabel('Presence penalty:'), self.layout['slider_layout3'])

        # textboxs
        self.layout['inputs'].addRow(QLabel('Prompt:'), self.prompt)
        self.layout['inputs'].addRow(QLabel('Output:'), self.output)
        self.layout['inputs'].setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        #buttons
        self.layout['buttons'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['buttons'])
        
        self.layout['buttons'].addWidget(self.btn_submit)
        self.layout['buttons'].addWidget(self.btn_reset)
        self.layout['main'].addWidget(self.status)

    def init_set_default_settings(self):
        #token slider
        self.max_tokens.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.max_tokens.setTickInterval(500)
        self.max_tokens.setTracking(True)
        self.max_token_value.setText('{0:,}'.format(self.max_tokens.value()))

        #temperature slider
        self.temperature.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.temperature.setTickInterval(10)
        self.temperature.setTracking(True)
        self.temperature_value.setText('{0:.2f}'.format(self.temperature.value()))

        #presence_penalty slider
        self.presence_penalty.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.presence_penalty.setTickInterval(10)
        self.presence_penalty.setTracking(True)
        self.presence_penalty_value.setText('{0:.2f}'.format(self.presence_penalty.value()))

    def init_configure_signals(self):
        self.max_tokens.valueChanged.connect(lambda: self.max_token_value.setText('{0: ,}'.format(self.max_tokens.value())))
        self.temperature.valueChanged.connect(lambda: self.temperature_value.setText('{0: .2f}'.format(self.temperature.value() / 100)))
        self.presence_penalty.valueChanged.connect(lambda: self.presence_penalty_value.setText('{0: .2f}'.format(self.presence_penalty.value() / 100)))


    def reset_fields(self):
        self.prompt.clear()
        self.output.clear()
        self.status.clearMessage()

    def submit(self):
        text_block = self.prompt.toPlainText()
        if not text_block:
            self.status.showMessage('Prompt is empty.')
            return
        else:
            self.status.clearMessage()

        self.output.clear()

        temperature = float('{0:.2f}'.format(self.temperature.value() / 100))
        presence_penalty = float('{0:.2f}'.format(self.presence_penalty.value() / 100))
        try:
            response = self.openai_playground.send_prompt_request(text_block.strip(), max_tokens=self.max_tokens.value(), temperature=temperature, presence_penalty=presence_penalty)
            self.output.setPlainText(response.get('outputs').strip())
            self.status.setStyleSheet('''
                color: green;
            ''')
            self.status.showMessage('Token used: {0}'.format(response.get('total_tokens')))
        except Exception as e:
            self.status.setStyleSheet('''
                color: red;
            ''')
            self.status.showMessage((str(e)))



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

        self.layout['main'].insertSpacing(0, 20)

        self.init_ui()
        self.init_configure_signal()
        self.init_menu()

    def init_ui(self):
        # add tab manager
        self.tab_manager = TabManager()
        self.layout['main'].addWidget(self.tab_manager)

        self.tab_manager.addTab(AIAssistant(), 'Conversa #{0}'.format(self.tab_index_tracker))
    
    def init_menu(self):
        self.menuBar = QMenuBar(self)
        self.menuBar.setStyleSheet('''
            * {
                background-color:#f0f0f0;
                color: black;
            }
            *::item:selected {
                background-color:#e3e3e3;
            }

        ''')

        fileMenu = QMenu('&File', self.menuBar)
        saveOutputAction = fileMenu.addAction('&Save Output', self.save_output)
        self.menuBar.addMenu(fileMenu)

    def add_tab(self):
        self.tab_index_tracker += 1
        self.tab_manager.addTab(AIAssistant(), 'Conversa #{0}'.format(self.tab_index_tracker))

    def init_configure_signal(self):
        self.tab_manager.plusClicked.connect(self.add_tab)

    def save_output(self):
        active_tab = self.tab_manager.currentWidget()

        prompt = active_tab.prompt.toPlainText()
        output = active_tab.output.toPlainText()
        timestamp = datetime.now().strftime('%y_%m_%d_%H%M%S')

        s = 'Prompt: \n{0}\n\nOutput:\n{1}'.format(prompt, output).strip()

        with open('{0}_Conversa.txt'.format(timestamp), 'w') as _f:
            _f.write(s)

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
