import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QButtonGroup

class ButtonGroupExample(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        button_group = QButtonGroup(self)

        # Создание нескольких кнопок и добавление их в группу
        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")

        button_group.addButton(button1)
        button_group.addButton(button2)
        button_group.addButton(button3)

        # Установка обработчика сигнала о смене состояния кнопок
        button_group.buttonClicked[int].connect(self.on_button_clicked)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

    def on_button_clicked(self, id):
        # Обработчик сигнала о смене состояния кнопок
        print(f"Button {id + 1} clicked")

def main():
    app = QApplication(sys.argv)
    window = ButtonGroupExample()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
