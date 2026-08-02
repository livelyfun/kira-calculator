import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class CalculatorWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kira Calculator")
        self.resize(400, 600)

        self.create_ui()

        self.just_calculated = False

    def create_ui(self):

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(15, 15, 15, 15)

        central_widget.setLayout(self.layout)

        self.create_display()
        self.create_button_grid()

    def create_display(self):

        self.display = QLabel("0")

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.display.setMinimumHeight(80)

        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.layout.addWidget(self.display)

    def create_button_grid(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        self.layout.addLayout(grid)

        buttons = [
            "C", "⌫", "÷", "×",
            "7", "8", "9", "-",
            "4", "5", "6", "+",
            "1", "2", "3", "=",
            "0", ".",
        ]
        for index, text in enumerate(buttons):

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

            row = index // 4
            column = index % 4

            if text == "0":
                 grid.addWidget(button, 4, 0, 1, 2)

            elif text == ".":
                 grid.addWidget(button, 4, 2)

            else:
                 grid.addWidget(button, row, column)

    

        for column in range(4):
            grid.setColumnStretch(column, 1)

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
    
        # Convert calculator symbols into Python operators
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
    
        try:
            result = eval(expression)
    
            self.display.setText(str(result))
            self.just_calculated = True
    
        except Exception:
            self.display.setText("Error")

def main():

    app = QApplication(sys.argv)

    style_path = Path(__file__).parent / "styles" / "main.qss"

    if style_path.exists():
        with open(style_path, "r") as file:
            app.setStyleSheet(file.read())

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()