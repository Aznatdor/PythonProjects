import sys
import os
import classes
from datetime import datetime
from PyQt5 import  QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
import json

"""
При нажатии на кнопку "Новый день" добавить проверку, что если день изменился, то создавать
новый день. Делать проверку, чтобы после закрытия приложения кнопка "Новый день" не создавала новый день, если день
ещё не изменился.
Проведи тест показывания графиков.
Сделать удаление расписаний.

Кешем будет открытые расписания, чтобы по новой из не создавать каждый раз. Если у меня такой прикол выйдет
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
        self.get_schedules_names()

        # Empty widget to add spacing
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(spacer)

        '''# Field to enter name of the new schedule
        self.schedule_name = QtWidgets.QLineEdit()
        self.schedule_name.setWhatsThis('Это подсказка для поля ввода')
        layout.addWidget(self.schedule_name)'''

        # Button to add new schedule
        self.add_button = QtWidgets.QPushButton("Add New Schedule")
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
        '''
        Creating window to manage schedule addition
        '''
        def confirm_additon():
            name = schedule_name.text()

            # if name is an empty string or name already has been added, do nothing
            if not name or self.schedules_list.findText(name) != -1:
                return
            schedule_name.clear() 
            self.schedules_list.addItem(name)
            self.main_window.setDisabled(False)
            self.inquire_box.close()

            with open(r"ScheduleData\Schedules\{}.json".format(name), 'w') as json_file:
                activities_list = activities_list_LineEdit.text().split(',')
                json_dict = {
                        "Activities" : activities_list,
                        "Days" : []
                    }
                json.dump(json_dict, json_file, indent=4)

            path = r"ScheduleData\Days\{}".format(name)
            os.mkdir(path)
                

        # Creating main layout
        self.inquire_box = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.inquire_box)

        # Layout for schudule name LineEdit
        name_layout = QtWidgets.QHBoxLayout()

        # Activities layout
        activities_layout = QtWidgets.QHBoxLayout()

        # Adding layouyts
        layout.addLayout(name_layout)
        layout.addLayout(activities_layout)

        # Creating LineEdit to get new schedule name
        schedule_name = QtWidgets.QLineEdit()
        schedule_name.setPlaceholderText('My Schedule')

        # Adding description to the name LineEdit
        name_description = QtWidgets.QLabel("Schedule name")
        name_layout.addWidget(name_description)
        name_layout.addWidget(schedule_name)

        # Creating LineEdit to get new schedule activities
        activities_list_LineEdit = QtWidgets.QLineEdit()
        activities_list_LineEdit.setPlaceholderText('Анжумания, Пресс качат, Бегит')
        activities_list_LineEdit.setToolTip("Названия активностей чрез запятую")

        # Adding description to the activities list LineEdit
        activities_description = QtWidgets.QLabel("Activities List")
        activities_layout.addWidget(activities_description)
        activities_layout.addWidget(activities_list_LineEdit)

        # Ading confirmation button
        confirm_button = QtWidgets.QPushButton("Confirm")
        layout.addWidget(confirm_button)
        confirm_button.clicked.connect(confirm_additon)

        self.inquire_box.show()

        self.main_window.setDisabled(True)

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

    def get_schedules_names(self):
        folder_path = r"ScheduleData\Schedules"
        file_names = os.listdir(folder_path)

        # Adding saved names to list
        for file_name in file_names:
            self.schedules_list.addItem(file_name[:-5])

# ------------------------------------------------------------------------------------------------------------------#
#                                Window to manipulate with choosen schedule                                         #
# ------------------------------------------------------------------------------------------------------------------#


class ScheduleManager(QtWidgets.QMainWindow):
    def __init__(self, schedule_name, main_window):
        super().__init__()
        self.init_ui(schedule_name, main_window)

    def init_ui(self, schedule_name, main_window):
        # getting data
        self.activities = None
        self.schedule = self.deserialize_schedule(schedule_name)
        self.days = []

        self.resize(500, 700)
        self.setWindowTitle("Schedule Manager: " + schedule_name)
        self.main_window = main_window
        self.schedule_name = schedule_name

        central_widget = QtWidgets.QWidget()  # Создаем виджет-контейнер
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        self.layout = QtWidgets.QVBoxLayout(central_widget)  # Создаем вертикальный макет

        # Button to add new day
        self.add_day_button = QtWidgets.QPushButton("Новый день", self)
        self.add_day_button.clicked.connect(self.add_new_day)
        self.add_day_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.add_day_button)

        # Button to get distribution
        self.get_distribution_button = QtWidgets.QPushButton("Просмотреть распределение", self)
        self.get_distribution_button.clicked.connect(self.get_distribution)
        self.get_distribution_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.get_distribution_button)

        # Button to open given day
        self.view_day_button = QtWidgets.QPushButton("Просмотреть день", self)
        self.view_day_button.clicked.connect(self.view_day)
        self.view_day_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.view_day_button)

        # Button to update scedule
        '''
        Сделай разделение на папки в днях, чтобы можно было сохранять одинаковые дни разных расписаний
        '''
        self.update_button = QtWidgets.QPushButton("Обновить", self)
        self.update_button.clicked.connect(self.update_schedule)
        self.update_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.update_button)

        # Button to return to main window
        self.return_button = QtWidgets.QPushButton("Вернуться", self)
        self.return_button.clicked.connect(self.return_home)
        self.layout.addWidget(self.return_button)



# ------------------------------------------------------------------------------------------------------------------#
#                                                   Methods                                                         #    
# ------------------------------------------------------------------------------------------------------------------#
        
    def add_new_day(self):
        if self.days == []:
            today_date = QtCore.QDate.currentDate()
            new_day = DayManager(today_date.toString("dd.MM.yyyy"), 
                                        self.schedule_name, self, False)
            self.days.append(new_day)
        
        self.days[-1].show()
        self.setVisible(False)


    def get_distribution(self):
        pass

    def view_day(self):
        self.calendar_window = CalendarWindow(self, self.schedule_name)
        self.setVisible(False)
        self.calendar_window.show()

    def return_home(self):
        self.main_window.setVisible(True)  # Показываем второе окно
        self.setVisible(False) # Закрываем основное окно

    def update_schedule(self):
        for day in self.days:
            day.serialize_day()

    def deserialize_schedule(self, schedule_name):
        schedule = None

        with open(r'ScheduleData\Schedules\{}.json'.format(schedule_name), 'r') as schedule_file:
            schedules_dict = json.load(schedule_file)
            schedule = classes.TimeStatistics(schedules_dict["Activities"])
            self.activities = schedules_dict["Activities"]

            for day in schedules_dict["Days"]:
                with open(r'ScheduleData\Days\{0}\{1}.json'.format(schedule_name, day), 'r') as day_file:
                    day_dict = json.load(day_file)
                    schedule.begin_day(day)

                    for activity in self.activities:
                        for time_stamp in day_dict[activity]:
                            schedule.add_timestamp(activity, classes.TimeStamp(*time_stamp))

                    schedule.end_day()

        return schedule


# ------------------------------------------------------------------------------------------------------------------#
#                                    Window to choose day from calendar                                             #
# ------------------------------------------------------------------------------------------------------------------#

class CalendarWindow(QWidget):
    def __init__(self, schedule_manager, schedule_name):
        super().__init__()

        self.init_ui(schedule_manager, schedule_name)

    def init_ui(self, schedule_manager, schedule_name):
        self.choosen_date = None
        self.schedule_manager = schedule_manager
        self.schedule_name = schedule_name

        self.resize(500, 700)
        self.layout = QtWidgets.QVBoxLayout(self)

        # Создаем виджет календаря
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.selectionChanged.connect(self.on_date_selected)
        self.layout.addWidget(self.calendar)

        # Layout to show choosen date and confirmation button
        self.info_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.info_layout)

        # Confirmation button
        self.confirmation_buttion = QtWidgets.QPushButton("Подтвердить", self)
        self.confirmation_buttion.clicked.connect(self.confirm)
        self.info_layout.addWidget(self.confirmation_buttion)

        # Метка для отображения выбранного дня
        self.selected_day_label = QtWidgets.QLabel("Выберите день", self)
        self.info_layout.addWidget(self.selected_day_label)

        self.setLayout(self.layout)
        self.setWindowTitle("Choose a date")
        self.show()

    def on_date_selected(self):
        selected_date = self.calendar.selectedDate()
        selected_day = selected_date.toString("dd.MM.yyyy")
        self.selected_day_label.setText(f"Выбранная дата: {selected_day}")
        self.choosen_date = selected_date

    def confirm(self):
        today = QtCore.QDate.currentDate()
        if (self.choosen_date is not None) and (today < self.choosen_date):
            return
        if self.choosen_date is None:
            self.choosen_date = today
        
        self.day_manager = DayManager(self.choosen_date.toString("dd.MM.yyyy"), 
                                      self.schedule_name, self.schedule_manager, True)
        self.setVisible(False)
        self.day_manager.show()

# ------------------------------------------------------------------------------------------------------------------#
#                                    Window to manipulate with choosen day                                          #
# ------------------------------------------------------------------------------------------------------------------#
        

class DayManager(QtWidgets.QWidget):
    def __init__(self, date, schedule_name, schedule_window, deserialize):
        super().__init__()
        self.init_ui(date, schedule_name, schedule_window, deserialize)

    def init_ui(self, date : str, schedule_name : str, schedule_window,  deserialize : bool):
        # Resizing
        self.resize(500, 700)
        self.setWindowTitle("Day Manager: " + date)
        self.schedule_window = schedule_window
        self.date = date
        self.deserialize_flag = deserialize

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
        self.tool_box.addWidget(self.return_button)
        self.return_button.clicked.connect(self.return_home)
        self.edit_time_points_layout.addLayout(self.tool_box)

        # Adding button to show distribution if we're deserializing day
        if self.deserialize_flag:
            self.show_time_distribution_button = QtWidgets.QPushButton("Показать распределение", self)
            self.tool_box.addWidget(self.show_time_distribution_button)

        # Adding names to columns
        self.description_layout = QtWidgets.QHBoxLayout()
        self.edit_time_points_layout.addLayout(self.description_layout)
        self.time_column_name = QtWidgets.QLabel("Время")
        self.comments_column_name = QtWidgets.QLabel("Комментарии")

        # Adding "spacer" widget
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.description_layout.addWidget(self.time_column_name)
        self.description_layout.addWidget(self.spacer)
        self.description_layout.addWidget(self.comments_column_name)

        # Another spacer
        self.spacer2 = QtWidgets.QWidget()
        self.spacer2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.spacer2)

        self.line_edits = [] # To properly add points
        self.activities_marker = [] # To properly add actvity type of the given timestamp

        # Dict for timestamp to activity map
        self.time_stamp_to_activity = dict()
        if not self.deserialize_flag:
            # Adding button to add QLineEdits
            self.add_button = QtWidgets.QPushButton("Добавить QLineEdit", self)
            self.add_button.clicked.connect(self.add_line_edits)
            self.layout.addWidget(self.add_button)

            # Adding button to add time stamps to the QLineEdit
            self.add_text_button = QtWidgets.QPushButton("Добавить текст")
            self.add_text_button.clicked.connect(self.add_text_to_last_edit)
            self.layout.addWidget(self.add_text_button)

        # Set the scroll widget as the main layout for the window
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

        # Adding first lines if it's a new day or deserializing existing
        if not self.deserialize_flag:
            self.add_line_edits()
        else:
            self.deserialize()


# ------------------------------------------------------------------------------------------------------------------#
#                                                   Methods                                                         #    
# ------------------------------------------------------------------------------------------------------------------#
    def add_activity_type(self, time_stamp : tuple):
        '''
        Method to add activity type to the corresponding day entry
        '''
        for activity_mark in self.activities_marker:
            if activity_mark.text() == "":
                activity_mark.setText(self.time_stamp_to_activity[time_stamp])
                break


    def add_line_edits(self):
        '''
        Method to add new day entry
        '''
        # Creating layout of 2 line edits and one text edit
        line_edit_layout = QtWidgets.QHBoxLayout()

        # Widgets to add
        line_edit1 = QtWidgets.QLineEdit()
        line_edit2 = QtWidgets.QLineEdit()
        text_edit = QtWidgets.QLineEdit()

        if not self.deserialize_flag:
            # if we're managing new day, add Combobox
            activites_list = QtWidgets.QComboBox()
            # filling up activities ComboBox 
            for activity in self.schedule_window.schedule.activity_names:
                activites_list.addItem(activity)
        else:
            # if we're looking at the past day, add LineEdit
            activites_list = QtWidgets.QLineEdit()
            activites_list.setReadOnly(True)
        self.activities_marker.append(activites_list)


        # Setting line edit widgets to read only mode
        line_edit1.setReadOnly(True)
        line_edit2.setReadOnly(True)

        if self.deserialize_flag:
           text_edit.setReadOnly(True)


        # Adding widgets to line_edits list
        self.line_edits.append(line_edit1)
        self.line_edits.append(line_edit2)

        # Adding widgets to layout
        line_edit_layout.addWidget(line_edit1)
        line_edit_layout.addWidget(line_edit2)
        line_edit_layout.addWidget(text_edit)
        line_edit_layout.addWidget(activites_list)

        # Adding layout to the main layout
        self.edit_time_points_layout.addLayout(line_edit_layout)

    def add_text_to_last_edit(self, time = False):
        '''
        Method to add timestamps to the last empty LineEdit
        '''
        if time == False:
            current_time = datetime.today()
            # Prettifying minute part of string appearance
            minutes = str(current_time.minute) if current_time.minute > 9 else "0" + str(current_time.minute) 
            # Adding hours:minutes string to schedule
            text_to_add = ':'.join([str(current_time.hour), minutes])
        else:
            text_to_add = time

        for line_edit in self.line_edits:
            if line_edit.text() == "":
                line_edit.setText(text_to_add)
                break
    
    def return_home(self):
        self.schedule_window.setVisible(True)  # Показываем второе окно
        self.setVisible(False) # Закрываем основное окно

    def time_stamp_to_str(self, time_stamp : list):
        '''
        To convert time_stamp list into pretty string
        '''
        begin, end = time_stamp

        begin = begin[:]
        end = end[:]

        if int(begin[1]) < 10:
            begin[1] = "0" + str(begin[1])
        if int(end[1]) < 10:
            end[1] = "0" + str(end[1])

        str1, str2 = ":".join([str(begin[0]), str(begin[1])]), ":".join([str(end[0]), str(end[1])])
        return str1, str2
    
    def str_to_timestamp(self, time_stamp_str1, time_stamp_str2):
        '''
        To conver time_stamp string into list
        '''
        if time_stamp_str1 == '' or time_stamp_str2 == '':
            return
        
        time_stamp1 = time_stamp_str1.split(':')
        time_stamp2 = time_stamp_str2.split(':')

        time_stamp_list1 = list(map(int, time_stamp1))
        time_stamp_list2 = list(map(int, time_stamp2))

        return [time_stamp_list1, time_stamp_list2]


    def deserialize(self):
        """
        Showing time of the given day
        """
        schedule_name = self.schedule_window.schedule_name
        folder_path = r"ScheduleData\Days\{}".format(schedule_name)
        file_names = os.listdir(folder_path)


        if (self.date + ".json") in file_names:
            with open(r"ScheduleData\Days\{0}\{1}.json".format(schedule_name, self.date), "r") as day:
                data = json.load(day)

                time_stamps = []
                for activity in data:
                    for timeStamp in data[activity]:
                        # to be able to map
                        time_stamp_string = self.time_stamp_to_str(timeStamp)
                        self.time_stamp_to_activity[time_stamp_string] = activity
                        time_stamps.append(timeStamp)

                time_stamps.sort()

                for i in range(len(time_stamps)):
                    self.add_line_edits()

                for timeStamp in time_stamps:
                    begin, end = self.time_stamp_to_str(timeStamp)

                    self.add_text_to_last_edit(begin)
                    self.add_text_to_last_edit(end) 
                    self.add_activity_type((begin, end))                
        else:
            self.return_home()

    def serialize_day(self):
        '''
        Method to covert day into json file
        '''
        json_dict = {activity : [] for activity in self.schedule_window.activities}

        for entry_num in range(len(self.activities_marker)):
            time_stamp_str1 = self.line_edits[2 * entry_num].text()
            time_stamp_str2  = self.line_edits[2 * entry_num + 1].text()

            activity = self.activities_marker[entry_num].currentText()

            time_stamp_list = self.str_to_timestamp(time_stamp_str1, time_stamp_str2)
            if time_stamp_list is not None:
                json_dict[activity].append(time_stamp_list)

        day_file_path = r"ScheduleData\Days\{0}\{1}.json".format(self.schedule_window.schedule_name, self.date)

        # you can use 'x' instead of 'w' to prevent rewriting
        with open(day_file_path, 'w') as json_file:
            json.dump(json_dict, json_file, indent=4)

        schedule_file_path = r'ScheduleData\Schedules\{}.json'.format(self.schedule_window.schedule_name)
        with open(schedule_file_path, 'r+') as json_file:
            # Loading data
            data = json.load(json_file)
            data["Days"].append(self.date)

            # moving pointer to the begining of the file
            json_file.seek(0)
            json.dump(data, json_file, indent=4)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
