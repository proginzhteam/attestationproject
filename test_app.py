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
from test import *

import pytest

@pytest.fixture(scope='function')
def app(qtbot):
    test_app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
    window = ScheduleApp()
    qtbot.addWidget(window)
    yield window
    window.close()

def test_initial_state(app):
    """Проверка начальных условий интерфейса."""
    assert app.combobox_group.count() == len(group_)  # Проверка количества элементов в комбобоксе групп
    assert app.combobox_group.currentText() == 'ПИ21-1'  # Проверка начального выбора в комбобоксе групп
    assert app.table_widget.rowCount() == 0  # Проверка отсутствия строк в таблице при инициализации
    
def test_update_schedule(app, qtbot):
    """Тестирование функции обновления расписания."""
    app.combobox_group.setCurrentIndex(0)  # Выбор первой группы
    app.date_edit.setDate(QDate.currentDate())  # Установка текущей даты
    qtbot.mouseClick(app.update_button, Qt.LeftButton)  # Нажатие на кнопку обновления
    assert app.table_widget.rowCount() > 0  # Проверка, что таблица содержит строки после обновления

def test_combobox_interaction(app, qtbot):
    """Тестирование взаимодействия с комбо-боксом направлений."""
    initial_count = app.combobox_direction.count()  # Исходное количество элементов
    app.combobox_direction.setCurrentIndex(0)  # Выбор первого элемента
    qtbot.wait(500)  # Ожидание обработки выбора
    assert app.combobox_direction.currentText() == directions[0]  # Проверка отображения выбранного направления
