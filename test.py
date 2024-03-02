import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QTextEdit, QLabel, QDateEdit, QListWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
import requests
from icalendar import Calendar, Event, Timezone
null_dull = {'auditorium': '', 'beginLesson': '', 'building': '', 'date': '', 'discipline': '', 'endLesson': '',
             'kindOfWork': '',
             'dayOfWeekString': ''}

directions = ['Модуль "ERP-системы"', 'Модуль "Системное программирование"', 'Модуль "Управление разработкой"',
              'Модуль "Технологии искусственного интеллекта"', 'Модуль "Языки и методы программирования"',
              'Модуль "Разработка распределенных приложений"',
              'Модуль "Технологии машинного обучения"', 'Модуль "Финтех"']

group_ = {'ПИ21-1': 110687, 'ПИ21-2': 110809, 'ПИ21-3': 110811, 'ПИ21-4': 110812, 'ПИ21-5': 110813, 'ПИ21-6': 110814,
          'ПИ21-7': 110815}

specializations = {
    "Модуль \"ERP-системы\"": [
        "Разработка корпоративных и облачных приложений",
        "Корпоративные информационные системы",
    ],
    "Модуль \"Системное программирование\"": [
        "Разработка эффективных вычислительных алгоритмов",
        "Низкоуровневое программирование",
    ],
    "Модуль \"Управление разработкой\"": [
        "Управление качеством программных систем",
        "Проектирование информационных систем",
    ],
    "Модуль \"Технологии искусственного интеллекта\"": [
        "Технологии и алгоритмы анализа сетевых моделей",
    ],
    "Модуль \"Языки и методы программирования\"": [
        "Программирование в среде R",
    ],
    "Модуль \"Разработка распределенных приложений\"": [
        "Основы технологий интернета вещей",
    ],
    "Модуль \"Технологии машинного обучения\"": [
        "Оптимизационные задачи в машинном обучении",
    ],
    "Модуль \"Финтех\"": [
        "Теоретические основы финансовых технологий",
    ],
}

basic_disciplines = ['Иностранный язык в профессиональной сфере', 'Информационное право',
                     'Машинное обучение в семантическом и сетевом анализе', 'Программная инженерия',
                     'Бухгалтерские информационные системы']


def get_schedule(group, start_date, finish_date):
    url = f'https://ruz.fa.ru/api/schedule/group/{group}?start={start_date}&finish={finish_date}&lng=1'
    try:
        schedule_data = requests.get(url).json()
    except Exception as e:
        print(f"Ошибка при получении расписания: {e}")
        return []
    return schedule_data
class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_disciplines = basic_disciplines.copy()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Расписание занятий')
        self.setGeometry(100, 100, 1280, 720)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.label_group = QLabel('Выберите группу:')
        layout.addWidget(self.label_group)
        self.combobox_group = QComboBox()
        self.combobox_group.addItems(list(group_.keys()))
        layout.addWidget(self.combobox_group)

        self.label_direction = QLabel('Выберите направление:')
        layout.addWidget(self.label_direction)
        self.combobox_direction = QComboBox()
        self.combobox_direction.addItems(directions)
        layout.addWidget(self.combobox_direction)

        self.label_specialization = QLabel('Выберите специализацию:')
        layout.addWidget(self.label_specialization)
        self.combobox_specialization = QComboBox()
        self.combobox_specialization.addItems(directions)
        layout.addWidget(self.combobox_specialization)

        self.label_date = QLabel('Выберите дату начала:')
        layout.addWidget(self.label_date)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        self.update_button = QPushButton('Обновить расписание')
        layout.addWidget(self.update_button)

        self.update_button.clicked.connect(self.update_schedule)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)  # Устанавливаем количество столбцов
        self.table_widget.setColumnWidth(0, 100)  # Ширина столбца "Дата"
        self.table_widget.setColumnWidth(1, 80)  # Ширина столбца "Время"
        self.table_widget.setColumnWidth(2, 350)  # Ширина столбца "Дисциплина"
        self.table_widget.setColumnWidth(3, 250)  # Ширина столбца "Тип"
        self.table_widget.setColumnWidth(4, 120)  # Ширина столбца "Аудитория"
        self.table_widget.setHorizontalHeaderLabels(['Дата', 'Время', 'Дисциплина', 'Тип', 'Место'])
        # Стилизация таблицы
        self.table_widget.horizontalHeader().setStyleSheet(
            "::section{Background-color:rgb(240,240,240);border-radius:10px;}")
        layout.addWidget(self.table_widget)

    def get_schedule(self, group, start_date, finish_date):
        url = f'https://ruz.fa.ru/api/schedule/group/{group}?start={start_date}&finish={finish_date}&lng=1'
        try:
            schedule_data = requests.get(url).json()
        except Exception as e:
            print(f"Ошибка при получении расписания: {e}")
            return []
        return schedule_data



    def update_schedule(self):
        group = self.combobox_group.currentText()
        group_id = group_[group]
        start_date = self.date_edit.date().toString("yyyy-MM-dd")
        finish_date = self.date_edit.date().addDays(6).toString("yyyy-MM-dd")

        # Получаем данные расписания (здесь предполагается, что вы уже определили get_schedule)
        schedule_data = self.get_schedule(group_id, start_date, finish_date)

        # Очищаем таблицу и устанавливаем количество строк исходя из данных
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        last_date = None
        for item in schedule_data:
            current_date = item['date']
            # Форматируем строку времени
            time_str = f"{item.get('beginLesson', 'Н/Д')} - {item.get('endLesson', 'Н/Д')}"
            # Если день изменился, добавляем заголовок с новым днем
            if current_date != last_date:
                self.table_widget.insertRow(self.table_widget.rowCount())
                day_of_week = datetime.strptime(current_date, "%Y.%m.%d").strftime('%A')
                day_of_week_item = QTableWidgetItem(day_of_week)
                day_of_week_item.setFont(QFont('Arial', 14, QFont.Bold))
                day_of_week_item.setBackground(Qt.lightGray)
                day_of_week_item.setTextAlignment(Qt.AlignCenter)
                day_of_week_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table_widget.setSpan(self.table_widget.rowCount() - 1, 0, 1, self.table_widget.columnCount())
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, day_of_week_item)

            # Добавляем информацию о занятии
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(current_date))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(time_str))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(item.get('discipline', 'Н/Д')))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(item.get('kindOfWork', 'Н/Д')))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(item.get('auditorium', 'Н/Д')))

            last_date = current_date

        #self.setCentralWidget(self.table_widget)  # Устанавливаем таблицу как центральный виджет


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScheduleApp()
    ex.show()
    sys.exit(app.exec_())
