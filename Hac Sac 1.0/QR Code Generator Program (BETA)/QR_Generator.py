# Import QRCode from pyqrcode
import pyqrcode
import png
from pyqrcode import QRCode
import os

while True:
    type = input("Enter Stock Type: ")
    try:
        cost = int(input("Enter Cost Per Piece: "))
    except:
        print("Please Enter a Numeric Cost, Try Again")
        continue
    if cost < 0:
        print("Cost cannot be a Negative Number, Try Again")
        continue
    cost = str(cost)
    s = type + "," + cost
    print(s)
    # Generate QR code
    url = pyqrcode.create(s)
    name = input("Enter File Name: ")
    fname = "%s.png" % name
    # Create and save the png file naming "myqr.png"
    url.png(fname, scale = 6)
    print("Copy Your QR Code and Scan it for Loading the Material")
    os.system(fname)
