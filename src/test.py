import sys
import utilities
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lightning ATM")
        # set UIs to True when the UI is called
        self.in_welcome_ui = False
        self.in_payment_success_ui = False
        self.in_refund_ui = False
        self.in_error_ui = False
        self.in_withdraw_ui = False
    
        self.welcomeUI()

    def welcomeUI(self):
        self.in_welcome_ui = True
        self.in_payment_success_ui = False
        self.in_refund_ui = False

        self.welcome_label = QLabel("Willkommen!")
        welcome_layout = QGridLayout()
        welcome_layout.addWidget(self.welcome_label)
        welcome_layout.setAlignment(Qt.AlignCenter)

        # create central widget and set layout
        welcome_widget = QWidget()
        welcome_widget.setLayout(welcome_layout)
        self.setCentralWidget(welcome_widget)

        self.keyPressEvent = self.on_key_press
    
    def payment_successUI(self):
        self.in_withdraw_ui = False
        self.in_payment_success_ui = True

        self.payment_success_label = QLabel("Geld erfolgreich abgehoben!")
        payment_success_layout = QGridLayout()
        payment_success_layout.addWidget(self.payment_success_label)
        payment_success_layout.setAlignment(Qt.AlignCenter)

        # create central widget and set layout
        payment_success_widget = QWidget()
        payment_success_widget.setLayout(payment_success_layout)
        self.setCentralWidget(payment_success_widget)

        # wait for 2 seconds before switching to the welcomeUI
        QTimer.singleShot(2000, self.welcomeUI)
    
    def refundUI(self):
        self.in_refund_ui = True
        self.in_error_ui = False

        self.refund_label = QLabel()
        refund_layout = QGridLayout()
        refund_layout.addWidget(self.refund_label)
        refund_layout.setAlignment(Qt.AlignCenter)

        # create central widget and set layout
        refund_widget = QWidget()
        refund_widget.setLayout(refund_layout)
        self.setCentralWidget(refund_widget)

        self.cancel_conversion()

        # wait for 2 seconds before switching to the welcomeUI
        QTimer.singleShot(2000, self.welcomeUI)

    def errorUI(self):
        self.in_error_ui = True
        self.in_welcome_ui = False
        self.in_payment_success_ui = False
        self.in_refund_ui = False
        self.in_withdraw_ui = False

        self.error_label = QLabel("Es ist ein Fehler aufgetreten! Es wird im nächsten Schritt das Geld wieder ausgezahlt!")
        error_layout = QGridLayout()
        error_layout.addWidget(self.error_label)
        error_layout.setAlignment(Qt.AlignCenter)

        # create central widget and set layout
        error_widget = QWidget()
        error_widget.setLayout(error_layout)
        self.setCentralWidget(error_widget)

        # wait for 2 seconds before switching to the refundUI
        QTimer.singleShot(2000, self.refundUI)

    def withdrawUI(self):
        self.in_withdraw_ui = True

         # create widgets
        self.total_eur_label = QLabel()
        self.total_satoshi_label = QLabel()
        self.qr_label = QLabel()
        self.pay_button = QPushButton("Umtauschen")
        self.amount_edit = QLabel()

        # create layout
        withdraw_layout = QGridLayout()
        withdraw_layout.addWidget(self.total_eur_label, 0, 1)
        withdraw_layout.addWidget(self.total_satoshi_label, 1, 1)
        withdraw_layout.addWidget(self.qr_label, 1, 0, 1, 2)
        withdraw_layout.addWidget(self.pay_button, 4, 0, 1, 2)

        # create central widget and set layout
        withdraw_widget = QWidget()
        withdraw_widget.setLayout(withdraw_layout)
        self.setCentralWidget(withdraw_widget)

        self.total_eur_label.setText(f"Gesamt in EUR: {self.total_eur:.2f}")
        self.total_satoshi_label.setText(f"Gesamt in Satoshi: {utilities.calculate_satoshi(self.total_eur, self.btc_price):,}")

        self.show_qr_code()

    def homeUI(self):
        self.in_welcome_ui = False
         # create widgets
        self.total_eur_label = QLabel()
        self.total_satoshi_label = QLabel()
        self.info_label = QLabel("Bitte eine Zahl von 0 bis 9 eingeben.")
        self.cancel_button = QPushButton("Abbrechen")
        self.pay_button = QPushButton("Umtauschen")
        self.amount_edit = QLabel()

        # create layout
        layout = QGridLayout()
        layout.addWidget(self.total_eur_label, 0, 1)
        layout.addWidget(self.total_satoshi_label, 1, 1)
        layout.addWidget(self.info_label, 0, 0, 1, 1)
        layout.addWidget(self.cancel_button, 2, 1)
        layout.addWidget(self.pay_button, 4, 0, 1, 2)

        # create central widget and set layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # connect signals and slots
        self.cancel_button.clicked.connect(self.refundUI)
        self.pay_button.clicked.connect(self.withdrawUI)
        self.keyPressEvent = self.on_key_press

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
                if self.btc_price is None:
                    return self.errorUI()

            self.total_eur += eur_price
            self.total_eur_label.setText(f"Gesamt in EUR: {self.total_eur:.2f}")
            self.total_satoshi_label.setText(f"Gesamt in Satoshi: {utilities.calculate_satoshi(self.total_eur, self.btc_price):,}")
            self.pay_button.setDisabled(0)
            self.cancel_button.setDisabled(0)
        except ValueError:
            pass
    
    def cancel_conversion(self):
        self.refund_label.setText(f"Es werden {self.total_eur:.2f} EUR ausgeworfen!")
        self.total_eur = 0
        self.btc_price = None
        self.invoice = None
        self.amount_edit.clear()

    def clear_all(self):
        self.total_eur = 0
        self.btc_price = None
        self.invoice = None
        self.total_eur_label.clear()
        self.total_satoshi_label.clear()
        self.amount_edit.clear()
        self.pay_button.setText("Umtauschen")
        self.pay_button.clicked.disconnect()
        self.pay_button.clicked.connect(self.show_qr_code)
        self.pay_button.setDisabled(1)

    def show_qr_code(self):
        self.info_label.hide()
        self.cancel_button.setDisabled(1)
        if self.invoice is None:
            self.invoice = utilities.generate_invoice(self.total_eur)
        utilities.generate_qr_code(self.invoice, self.qr_label)
        self.pay_button.setText("Zahlung prüfen")
        self.pay_button.clicked.connect(self.check_payment)

    def check_payment(self, event):
        if utilities.check_payment(self):
            self.clear_all()
            self.payment_successUI()
        else:
            self.clear_all()
            self.errorUI()

    def on_key_press(self, event):
        if event.text() in "0123456789":
            if self.in_welcome_ui == True:
                self.homeUI()
            if any([self.in_withdraw_ui, self.in_welcome_ui, self.in_payment_success_ui, self.in_refund_ui, self.in_error_ui]):
                print("Error: Money may not be deposited in this screen!")
                return
            self.key = event.text()
            self.amount_edit.setText(self.key)
            self.calculate_satoshi()
        elif event.key() == 16777216:  # Esc
            self.welcomeUI()
        elif event.key() == 16777220:  # Return
            self.withdrawUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
