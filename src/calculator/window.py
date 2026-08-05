from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from calculator.logic import calculate


class CalculatorWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kira Calculator")
        self.resize(750, 650)
        self.setMinimumSize(700, 600)
        self.setMaximumSize(900,700)

        self.create_ui()

        self.just_calculated = False

    def create_ui(self):
    
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
    
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
    
        central_widget.setLayout(self.main_layout)
    
        # ==========================
        # Left Side (Calculator)
        # ==========================

        self.calculator_layout = QVBoxLayout()
        self.calculator_layout.setSpacing(15)

        self.create_display()
        self.create_button_grid()

        calculator_widget = QWidget()
        calculator_widget.setLayout(self.calculator_layout)
        calculator_widget.setMinimumWidth(430)

        self.main_layout.addWidget(calculator_widget, 4)

        # ==========================
        # Right Side (History)
        # ==========================

        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(10)

        self.create_history()

        history_widget = QWidget()
        history_widget.setLayout(self.history_layout)
        history_widget.setMinimumWidth(260)

        self.main_layout.addWidget(history_widget, 2)

    def create_display(self):

        self.display = QLabel("0")

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.display.setMinimumHeight(100)

        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.calculator_layout.addWidget(self.display)
   
    def create_history(self):

        title = QLabel("History")
        title.setObjectName("historyTitle")

        self.history = QListWidget()
        self.history.setObjectName("history")

        self.history.itemDoubleClicked.connect(
            self.restore_history
        )

        clear_button = QPushButton("Clear History")
        clear_button.setObjectName("clearHistoryButton")
        clear_button.clicked.connect(
            self.history.clear
        )

        self.history_layout.addWidget(title)
        self.history_layout.addWidget(self.history)
        self.history_layout.addWidget(clear_button)  

    def create_button_grid(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        self.calculator_layout.addLayout(grid)

        buttons = [
            ("C", 0, 0),
            ("⌫", 0, 1),
            ("÷", 0, 2),
            ("×", 0, 3),
        
            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("-", 1, 3),
        
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("+", 2, 3),
        
            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("=", 3, 3),
        
            ("0", 4, 0),
            (".", 4, 2),
        ]
        for text, row, column in buttons:

            button = QPushButton(text)
            # Give each button a style name
            if text.isdigit():
                button.setObjectName("numberButton")
            
            elif text in ["+", "-", "×", "÷"]:
                button.setObjectName("operatorButton")
            
            elif text == "=":
                button.setObjectName("equalsButton")
           
            elif text == ".":
                 button.setObjectName("numberButton")

            elif text == "⌫":
                button.setObjectName("backspaceButton")     

            elif text == "C":
                button.setObjectName("clearButton")
            button.clicked.connect(
                lambda checked=False, t=text: self.button_clicked(t)
            )

            if text == "0":
                grid.addWidget(button, row, column, 1, 2)
            
            else:
                grid.addWidget(button, row, column)

    

        for column in range(4):
            grid.setColumnStretch(column, 1)
    def keyPressEvent(self, event: QKeyEvent):
    
        key = event.key()
        text = event.text()
    
        if text.isdigit() or text in ["+", "-", "."]:
            self.append_text(text)
    
        elif text == "*":
            self.append_text("×")
    
        elif text == "/":
            self.append_text("÷")
    
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.calculate_result()
    
        elif key == Qt.Key.Key_Backspace:
            self.backspace()
    
        elif key == Qt.Key.Key_Escape:
            self.clear_display()
    
        else:
            super().keyPressEvent(event)
    def button_clicked(self, text):
        
        if text == "C":
            self.clear_display()

        elif text == "=":
            self.calculate_result()

        elif text == "⌫":
            self.backspace()    

        else:
            self.append_text(text)

    def append_text(self, text):

      current = self.display.text()
      
      operators = ["+", "-", "×", "÷"]
      
      # Start fresh after pressing =
      if self.just_calculated:
          self.display.setText(text)
          self.just_calculated = False
          return
      
      # Prevent starting with × or ÷
      if current == "0" and text in ["×", "÷"]:
          return
      
      # Replace the last operator if user presses another operator
      if current[-1] in operators and text in operators:
          self.display.setText(current[:-1] + text)
          return
      # Prevent multiple decimal points in the current number
      if text == ".":
      
          last_number = current
      
          for operator in ["+", "-", "×", "÷"]:
              last_number = last_number.split(operator)[-1]
      
          if "." in last_number:
              return
      # Replace the initial 0
      if current == "0":
          self.display.setText(text)
      else:
          self.display.setText(current + text)
          
    def clear_display(self):

        self.display.setText("0")

    def backspace(self):

        current = self.display.text()

        if current == "Error":
            self.display.setText("0")
            return

        if len(current) == 1:
            self.display.setText("0")
            return

        self.display.setText(current[:-1])   


    def calculate_result(self):
    
        expression = self.display.text()
    
        result = calculate(expression)
    
        if result != "Error":
        
            self.history.insertItem(
                0,
                f"{expression} = {result}"
            )
    
        self.display.setText(result)
    
        if result != "Error":
            self.just_calculated = True

    def restore_history(self, item):

        text = item.text()
    
        expression = text.split("=")[0].strip()
    
        self.display.setText(expression)
    
        self.just_calculated = False        