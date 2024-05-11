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
from test import ScheduleApp, group_, directions
import pytest

@pytest.fixture(scope='module')
def app():
    test_app = QApplication(sys.argv)
    window = ScheduleApp()
    qtbot.addWidget(window)
    return window

def test_initial_state(app):
    """Тестирование начальных условий GUI."""
    assert app.combobox_group.count() == len(group_)  # Проверка количества элементов в комбобоксе групп
    assert app.combobox_group.currentText() == 'ПИ21-1'  # Проверка начального выбора в комбобоксе
    assert app.combobox_direction.count() == len(directions)  # Проверка количества направлений
    assert app.table_widget.columnCount() == 5  # Проверка количества столбцов в таблице
    assert app.table_widget.rowCount() == 0  # Проверка наличия строк в начальном состоянии

def test_update_button_click(app):
    """Тестирование реакции на нажатие кнопки обновления."""
    app.combobox_group.setCurrentIndex(0)  # Выбор первой группы
    app.date_edit.setDate(QDate.currentDate())  # Установка текущей даты
    qtbot.mouseClick(app.update_button, Qt.LeftButton)  # Имитация нажатия кнопки обновления
    assert app.table_widget.rowCount() > 0  # Проверка, что после обновления в таблице появились строки
