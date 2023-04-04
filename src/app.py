import sys
import utilities
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget
from PySide6.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of the window
        self.setWindowTitle("Lightning ATM")

        # create widgets
        self.amount_label = QLabel("Gib einen Betrag in EUR ein:")
        self.amount_edit = QLineEdit()
        self.total_eur_label = QLabel()
        self.total_satoshi_label = QLabel()
        self.convert_button = QPushButton("In Bitcoin umrechnen")
        self.cancel_button = QPushButton("Abbrechen")
        self.pay_button = QPushButton("Zahlung bestätigen")
        self.qr_label = QLabel()

        # create layout
        layout = QGridLayout()
        layout.addWidget(self.amount_label, 0, 0)
        layout.addWidget(self.amount_edit, 0, 1)
        layout.addWidget(self.total_eur_label, 1, 0)
        layout.addWidget(self.total_satoshi_label, 1, 1)
        layout.addWidget(self.convert_button, 2, 0)
        layout.addWidget(self.cancel_button, 2, 1)
        layout.addWidget(self.qr_label, 3, 0, 1, 2)
        layout.addWidget(self.pay_button, 4, 0, 1, 2)

        # create central widget and set layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # connect signals and slots
        self.convert_button.clicked.connect(self.calculate_satoshi)
        self.cancel_button.clicked.connect(self.cancel_conversion)
        self.pay_button.clicked.connect(self.show_qr_code)

        # initialize variables
        self.total_eur = 0
        self.btc_price = None
        self.invoice = None
        self.pay_button.setDisabled(1)
        self.cancel_button.setDisabled(1)

    def calculate_satoshi(self):
        eur_input = self.amount_edit.text()

        try:
            eur_price = float(eur_input)
            if self.btc_price is None:
                self.btc_price = utilities.get_btc_price()

            self.total_eur += eur_price
            self.total_eur_label.setText(f"Gesamt in EUR: {self.total_eur:.2f}")
            self.total_satoshi_label.setText(f"Gesamt in Satoshi: {utilities.calculate_satoshi(self.total_eur, self.btc_price):,}")
            self.pay_button.setDisabled(0)
            self.cancel_button.setDisabled(0)
        except ValueError:
            pass

    def cancel_conversion(self):
        self.total_eur = 0
        self.btc_price = None
        self.invoice = None
        self.total_eur_label.clear()
        self.total_satoshi_label.clear()
        self.amount_edit.clear()
        self.cancel_button.setDisabled(1)
        self.pay_button.setDisabled(1)
        self.convert_button.setDisabled(0)

    def clear_all(self):
        self.total_eur = 0
        self.btc_price = None
        self.invoice = None
        self.total_eur_label.clear()
        self.total_satoshi_label.clear()
        self.amount_edit.clear()
        self.pay_button.setText("Zahlung bestätigen")
        self.pay_button.clicked.disconnect()
        self.pay_button.clicked.connect(self.show_qr_code)
        self.cancel_button.setDisabled(1)
        self.pay_button.setDisabled(1)
        self.convert_button.setDisabled(0)

    def show_qr_code(self):
        self.cancel_button.setDisabled(1)
        self.convert_button.setDisabled(1)
        if self.invoice is None:
            self.invoice = utilities.generate_invoice(self.total_eur)
        utilities.generate_qr_code(self.invoice, self.qr_label)
        self.pay_button.setText("Zahlung prüfen")
        self.pay_button.clicked.disconnect()
        self.pay_button.clicked.connect(self.check_payment)

    def check_payment(self):
        if utilities.check_payment(self):
            self.qr_label.setText("Zahlung bestätigt.")
            QTimer.singleShot(1000, lambda: self.qr_label.setText(""))
            self.clear_all()
        else:
            self.qr_label.setText("Zahlung nicht bestätigt.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
