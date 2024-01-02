import sys
from datetime import datetime
from PyQt5 import  QtWidgets

"""
Сделай добавление нового дня. Просмотр предыдущего. Проведи тест показывания графиков. 
Возмжно стоит добавить промежуточный экран. Типа с выбором действий.
"""

# ------------------------------------------------------------------------------------------------------------------#
#                                                   Main Window                                                     #
# ------------------------------------------------------------------------------------------------------------------#


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Dictionary of schedules
        self.schedules_dict = {}

        self.main_window = QtWidgets.QMainWindow()
        self.main_window.resize(500, 700)

        central_widget = QtWidgets.QWidget()  # Создаем виджет-контейнер
        self.main_window.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)  # Создаем вертикальный макет

        # Button to choose shedule
        self.choose_button = QtWidgets.QPushButton("Choose Schedule")
        layout.addWidget(self.choose_button)
        self.choose_button.clicked.connect(self.choose_schedule)

        # List to choose schedule
        self.schedules_list = QtWidgets.QComboBox()
        layout.addWidget(self.schedules_list)

        # Empty widget to add spacing
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(spacer)

        # Field to enter name of the new schedule
        self.schedule_name = QtWidgets.QLineEdit()
        layout.addWidget(self.schedule_name)

        # Button to add new schedule
        self.add_button = QtWidgets.QPushButton("Add Schedule")
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_schedule)

        # Button to delete choosen schedule
        self.delete_button = QtWidgets.QPushButton("Delete Schedule")
        layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_schedule)
        
    # ------------------------------------------------------------------------------------------------------------------#
    #                                                   On-click methods                                                #
    # ------------------------------------------------------------------------------------------------------------------#
        
    def add_schedule(self):
        name = self.schedule_name.text()

        # if name is an empty string or name already has been added, do nothing
        if not name or self.schedules_list.findText(name) != -1:
            return
        self.schedule_name.clear() 
        self.schedules_list.addItem(name)

    def delete_schedule(self):
        name = self.schedules_list.currentText()
        del self.schedules_dict[name]
        self.schedules_list.removeItem(self.schedules_list.findText(name))

    def choose_schedule(self):
        self.main_window.setVisible(False) # Закрываем основное окно

        schedule_name = self.schedules_list.currentText()

        # If we're choosing new schedule
        if schedule_name in self.schedules_dict:
            self.schedules_dict[schedule_name].setVisible(True)
        else:
            # If schedule has been used previously
            choosen_schedule_window = ScheduleManager(schedule_name, self.main_window) # Создаем экземпляр второго окна
            self.schedules_dict[schedule_name] = choosen_schedule_window
            choosen_schedule_window.show()  # Показываем второе окно



# ------------------------------------------------------------------------------------------------------------------#
#                                    Window to manipulate with choosen schedule                                     #
# ------------------------------------------------------------------------------------------------------------------#
        

class ScheduleManager(QtWidgets.QWidget):
    '''
    Добавть кнопку для возвращения на основной экран.
    '''
    def __init__(self, schedule_name, main_window):
        super().__init__()
        self.init_ui(schedule_name, main_window)

    def init_ui(self, schedule_name, main_window):
        # Resizing
        self.resize(500, 700)
        self.setWindowTitle("Schedule Manager: " + schedule_name)
        self.main_window = main_window

        # Scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        # Main layout inside the scroll widget
        self.layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.layout)

        # Layout to add time points via QLineEdit
        self.edit_time_points_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.edit_time_points_layout)

        # Adding "tool box"
        self.tool_box = QtWidgets.QHBoxLayout()
        self.return_button = QtWidgets.QPushButton("Назад", self)
        self.show_time_distribution_button = QtWidgets.QPushButton("Показать распределение", self)
        self.tool_box.addWidget(self.return_button)
        self.return_button.clicked.connect(self.return_home)
        self.edit_time_points_layout.addLayout(self.tool_box)
        self.tool_box.addWidget(self.show_time_distribution_button)

        # Adding names to columns
        self.description_layout = QtWidgets.QHBoxLayout()
        self.edit_time_points_layout.addLayout(self.description_layout)
        self.time_column_name = QtWidgets.QLabel("Время")
        self.comments_column_name = QtWidgets.QLabel("Комментарии")

        # Adding "spacer" widget
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.description_layout.addWidget(self.time_column_name)
        self.description_layout.addWidget(self.spacer)
        self.description_layout.addWidget(self.comments_column_name)

        # Adding button to add QLineEdits
        self.add_button = QtWidgets.QPushButton("Добавить QLineEdit", self)
        self.add_button.clicked.connect(self.add_line_edits)
        self.layout.addWidget(self.add_button)

        # Adding button to add time stamps to the QLineEdit
        self.line_edits = [] # To properly add points
        self.add_text_button = QtWidgets.QPushButton("Добавить текст")
        self.add_text_button.clicked.connect(self.add_text_to_last_edit)
        self.layout.addWidget(self.add_text_button)

        # Set the scroll widget as the main layout for the window
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

        # Adding first lines
        self.add_line_edits()

# ------------------------------------------------------------------------------------------------------------------#
#                                                   Methods                                                         #    
# ------------------------------------------------------------------------------------------------------------------#

    def add_line_edits(self):
        # Creating layout of 2 line edits and one text edit
        line_edit_layout = QtWidgets.QHBoxLayout()

        # Widgets to add
        line_edit1 = QtWidgets.QLineEdit()
        line_edit2 = QtWidgets.QLineEdit()
        text_edit = QtWidgets.QTextEdit()

        # Setting line edit widgets to read only mode
        line_edit1.setReadOnly(True)
        line_edit2.setReadOnly(True)

        # Adding widgets to line_edits list
        self.line_edits.append(line_edit1)
        self.line_edits.append(line_edit2)

        # Adding widgets to layout
        line_edit_layout.addWidget(line_edit1)
        line_edit_layout.addWidget(line_edit2)
        line_edit_layout.addWidget(text_edit)

        # Adding layout to the main layout
        self.edit_time_points_layout.addLayout(line_edit_layout)

    def add_text_to_last_edit(self):
        current_time = datetime.today()

        # Prettifying minute part of string appearance
        minutes = str(current_time.minute) if current_time.minute > 9 else "0" + str(current_time.minute) 

        # Adding hours:minutes string to schedule
        text_to_add = ':'.join([str(current_time.hour), minutes])
        for line_edit in self.line_edits:
            if line_edit.text() == "":
                line_edit.setText(text_to_add)
                break
    
    def return_home(self):
        self.main_window.setVisible(True)  # Показываем второе окно
        self.setVisible(False) # Закрываем основное окно

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
