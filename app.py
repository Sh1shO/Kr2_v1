from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QLineEdit, QFormLayout, QDialog, QMessageBox
from PySide6.QtCore import Qt
from fpdf import FPDF
from db import get_session, session, Rental, Car, Client, CarModel
from datetime import date


class EditRentalDialog(QDialog):
    def __init__(self, rental, parent=None):
        super().__init__(parent)
        self.rental = rental
        self.setWindowTitle("Редактировать прокат")

        # Layout для формы
        layout = QFormLayout(self)

        # Выпадающий список для выбора клиента
        self.client_combo = QComboBox()
        self.client_combo.addItem("Выберите клиента")  # Начальный элемент
        # Заполняем выпадающий список клиентами из базы данных
        clients = session.query(Client).all()
        for client in clients:
            client_info = f"{client.lastname} {client.firstname} {client.patronymic}"
            self.client_combo.addItem(client_info, userData=client.id)  # Добавляем клиента в выпадающий список с id клиента
        layout.addRow("Клиент:", self.client_combo)

        # Выпадающий список для выбора автомобиля
        self.car_combo = QComboBox()
        self.car_combo.addItem("Выберите машину")  # Начальный элемент
        # Заполняем выпадающий список машинами из базы данных
        cars = session.query(Car).all()
        for car in cars:
            car_info = f"{car.fk_model_id.name} ({car.color}, {car.number})"
            self.car_combo.addItem(car_info, userData=car.id)  # Добавляем машину в выпадающий список с id машины
        layout.addRow("Автомобиль:", self.car_combo)

        # Поле для ввода количества дней
        self.days_input = QLineEdit(str(self.rental.days_quantity))
        layout.addRow("Количество дней:", self.days_input)

        # Кнопки для подтверждения или отмены изменений
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_rental)
        layout.addWidget(self.save_button)

    def save_rental(self):
        """Сохраняет изменения в базе данных."""
        new_client_id = self.client_combo.currentData()  # Получаем выбранный id клиента
        new_car_id = self.car_combo.currentData()  # Получаем выбранный id автомобиля
        new_days_quantity = self.days_input.text()

        if not new_client_id or not new_car_id or not new_days_quantity.isdigit():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите клиента и автомобиль и введите количество дней.")
            return

        # Обновляем данные о прокате
        self.rental.client_id = new_client_id
        self.rental.car_id = new_car_id
        self.rental.days_quantity = int(new_days_quantity)
        session.commit()  # Сохраняем изменения в базе
        self.accept()  # Закрыть диалог


class RentalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Прокат автомобилей")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        # Основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Макет
        layout = QVBoxLayout(central_widget)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Клиент", "Автомобиль", "Дата начала", "Количество дней"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Запрет редактирования
        layout.addWidget(self.table)

        # Кнопка "Редактировать"
        self.edit_button = QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.edit_rental)
        layout.addWidget(self.edit_button)

        # Кнопка для формирования отчета
        generate_report_button = QPushButton("Сформировать отчет")
        generate_report_button.clicked.connect(self.generate_rental_report)
        layout.addWidget(generate_report_button)

        # Загрузка данных
        self.load_rentals()

    def load_rentals(self):
        """Загружает данные из базы в таблицу."""
        # Получаем данные о прокатах
        rentals = session.query(Rental, Client, Car, CarModel).join(Client, Rental.client_id == Client.id) \
            .join(Car, Rental.car_id == Car.id) \
            .join(CarModel, Car.model_id == CarModel.id).all()

        self.table.setRowCount(len(rentals))  # Устанавливаем количество строк
        for row, (rental, client, car, model) in enumerate(rentals):
            # Заполняем таблицу
            self.table.setItem(row, 0, QTableWidgetItem(f"{client.lastname} {client.firstname} {client.patronymic}"))
            self.table.setItem(row, 1, QTableWidgetItem(f"{model.name} ({car.color}, {car.number})"))
            self.table.setItem(row, 2, QTableWidgetItem(str(rental.start_date)))
            self.table.setItem(row, 3, QTableWidgetItem(str(rental.days_quantity)))

    def edit_rental(self):
        """Редактирует данные о прокате авто."""
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для редактирования.")
            return

        # Получаем объект проката для редактирования
        rental_id = self.table.item(row, 2).text()  # Для поиска проката можно использовать дату начала
        rental = session.query(Rental).filter(Rental.start_date == rental_id).first()  # Получаем прокат по дате начала

        if rental is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти прокат для редактирования.")
            return

        # Создаем диалоговое окно для редактирования
        dialog = EditRentalDialog(rental, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_rentals()  # Перезагружаем данные в таблице
            QMessageBox.information(self, "Успех", "Данные успешно обновлены!")

    def generate_rental_report(self):
        session = get_session()

        # Указываем начальную и конечную дату отчета
        start_date, end_date = date(2024, 1, 1), date(2024, 12, 31)

        # Извлечение данных о прокатах по каждому клиенту
        rentals = (
            session.query(
                Client.lastname,
                Client.firstname,
                Client.patronymic,
                Rental.client_id
            )
            .join(Client, Rental.client_id == Client.id)
            .filter(Rental.start_date.between(start_date, end_date))
            .all()
        )

        # Считаем количество прокатов по каждому клиенту
        client_rentals = {}
        for last_name, first_name, patronymic, client_id in rentals:
            full_name = f"{last_name} {first_name} {patronymic}"
            client_rentals[full_name] = client_rentals.get(full_name, 0) + 1

        # Создание PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
        pdf.set_font('FreeSans', '', 16)

        # Заголовок отчета
        pdf.cell(200, 10, "Отчет о количестве прокатов автомобилей по клиентам", ln=True, align='C')
        pdf.ln(10)

        # Заполнение данных отчета
        pdf.set_font('FreeSans', '', 12)
        for client, count in client_rentals.items():
            pdf.cell(200, 10, f"{client}:", ln=True)
            pdf.cell(200, 10, f"Прокатов: {count}", ln=True)
            pdf.ln(5)

        # Сохранение PDF
        pdf_output_path = f"./rental_report_by_client.pdf"
        pdf.output(pdf_output_path)

        print(f"Отчет был успешно экспортирован в {pdf_output_path}")
        session.close()

        QMessageBox.information(self, "Успех", f"Отчет был успешно экспортирован в:\n{pdf_output_path}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = RentalApp()
    window.show()
    sys.exit(app.exec())
