import qrcode

# Entering the Lightning Network Invoice via the Console
invoice = input("Gib das Lightning Network Invoice ein: ")

# first
# Creating a QR code from the Lightning Network Invoice
#img = qrcode.make(invoice)

#img.save("invoice.png")

# Creating a QR code from the Lightning Network Invoice
qr = qrcode.QRCode(version=None, box_size=2, border=4)
qr.add_data(invoice)
qr.make(fit=True)

# Output of the QR code in the console
qr.print_ascii(invert=True)
