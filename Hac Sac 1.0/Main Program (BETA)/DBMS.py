#Importing Libraries
import sqlite3
import datetime
import os
import re
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 3000  # Set Duration To 1000 ms == 1 second
today = datetime.date.today()
current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#For Scanning the Type of Stock and Price Per Piece
def scan():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        barcodes = pyzbar.decode(frame)
        text = None
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            text = "{}".format(barcodeData)
            print(text)
            inp = text.split(',')
            type = inp[0]
            cost = int(inp[1])
            cv2.imshow("Scanner", frame)
            key = cv2.waitKey(1) & 0xFF
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c") | ord("C"):
            break
        if text != None:
            break
    cv2.destroyAllWindows()
    vs.stop()
    return (type,cost)


#Declaration Section
#File System
#For the Log File
if os.path.isfile("log.txt"):
    f = open("log.txt", "a+")
else:
    f = open("log.txt", "w+")



#For the File containing backup of password, Serial Number for log and Last Capacity of the warehouse defined by the user
if os.path.isfile("ROOT"):
    p = open("ROOT", "r+")
    temp = int(0)
    pos = p.tell()
    for line in p:
        if temp == 0:
            passwd = re.match("^([^\s]+)",line).group(0)
        elif temp == 1:
            i = re.match("^([^\s]+)",line).group(0)
            try:
                i = int(i)
            except: None
        elif temp == 2:
            cap = re.match("^([^\s]+)",line).group(0)
            try:
                cap = int(cap)
            except: None
        else:
            capm = re.match("^([^\s]+)",line).group(0)
            try:
                capm = int(capm)
            except: None
        temp += 1
    p.seek(pos)
else:
    i = int(1)
    passwd = 'password'
    os.system('cls')
    wname = input("Please Enter your Warehouse's Name: ")
    try: cap = int(input("Enter Capacity for the Warehouse: "))
    except:
        print("Please enter a Numeric Capacity, Try Again")
        quit()
    if cap <= 0:
        print("Capacity cannot be Negative or Zero, Try Again")
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        quit()
    print("---------------------------------------------------------------------------------------------------------------------------------------")
    capm = cap
    f.write("%d) %s || First Boot || Capacity Updated to %d || Administrator Mode\n" %(i,current,capm))
    i += 1
    p = open("ROOT", "w+")
    p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
    p = open("ROOT", "r+")
    print("Your password for",wname,"is 'password', Please set a new password from Administrator Mode:")
    print("---------------------------------------------------------------------------------------------------------------------------------------")
    p = open("ROOT", "w+")
    p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
    p = open("ROOT", "r+")
    time.sleep(5)



#For creating the database and linking to it
conn = sqlite3.connect('DAT.sqlite')
cur = conn.cursor()



#Create Table
cur.execute('''CREATE TABLE IF NOT EXISTS Stocks (Name_of_Owner TEXT, Type_of_Stock TEXT, Loading_Date TEXT, Departing_Date TEXT, Cost INTEGER, Quantity INTEGER)''')



#Main Program Loop
#Mode of Operation
while True:
    os.system('cls')
    today = datetime.date.today()
    current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = input("Enter your Name or Press Q to Quit: ")
    if (name == "Q") | (name == 'q'):
        conn.commit()
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        break
    print("---------------------------------------------------------------------------------------------------------------------------------------")
    temp = input("Select Mode of Operation:\n1) Administrator Mode\n2) User Mode\n3) Quit\nEnter Your Choice: ")
    print("---------------------------------------------------------------------------------------------------------------------------------------")



    #Administrator Mode: Used for changing either the system password or storage capacity
    if temp == "1":
        temp = input("Enter Password: ")
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        if temp == passwd:
            print("Available Space: ",cap)
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            temp = input("What do you want to do?\n1) Change Password\n2) Change Warehouse Capacity\n3) View Stocks\n4) Back\n5) Quit\nEnter Your Choice: ")
            print("---------------------------------------------------------------------------------------------------------------------------------------")



            #Loop for setting a new password
            if temp == "1":
                passwd = input("Please Enter Your New Password: ")
                f.write("%d) %s || Password Changed || User: %s || Administrator Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue



            #Loop for changinf the storage capacity of the warehouse
            elif temp == "2":
                print("Your Current Warehouse Capacity:",capm)
                try: temp1 = int(input("Enter New Capacity for the Warehouse: "))
                except:
                    print("Please enter a Numeric Capacity, Try Again")
                    quit()
                if temp1 <= 0:
                    print("Capacity cannot be Negative or Zero, Try Again")
                    print("---------------------------------------------------------------------------------------------------------------------------------------")
                    quit()
                temp2 = cap
                temp2 = temp1 - capm + temp2
                if temp2 < 0:
                    print("Stocks Present are already more than Capacity Required. Operation not Possible. Try Again")
                    f.write("%d) %s || Attempt to Reduce Capacity Beyond Occupied Space || Invalid Entry || %s || Administrator Mode\n" %(i,current,name))
                    i += 1
                    p = open("ROOT", "w+")
                    p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                    p = open("ROOT", "r+")
                    print("---------------------------------------------------------------------------------------------------------------------------------------")
                    winsound.Beep(frequency, duration)
                    continue
                capm = temp1
                cap = temp2
                f.write("%d) %s || Capacity Updates || User: %s || Administrator Mode || Capacity Changed to %d\n" %(i,current,name,capm))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue


            #Loop for Viewing Stocks to the Owner/Administrator
            elif temp == "3":
                cur.execute("SELECT Name_Of_Owner,Type_Of_Stock,Loading_Date,Cost,Quantity FROM Stocks")
                data = cur.fetchall()
                print("Name".center(35),"Type Of Stock".center(35),"Loading Data".center(15),"Cost".center(22),"Quantity".center(18),"\n")
                for item in data:
                    y = 0
                    for x in item:
                        x = str(x)
                        if y < 2:
                            print(x.center(35),end = "")
                        else:
                            print(x.center(20),end = "")
                        y += 1
                        if y == 5:
                            print("\n")
                print("\n")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                f.write("%d) %s || Live Stock View Requested || User: %s || Administrator Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                temp = input("Press Q to go Back: ")
                if (temp == 'q') | (temp == 'Q'):
                    continue
                else:
                    print("Invalid Entry, Automatically Going Back")
                    winsound.Beep(frequency, duration)
                    continue


            #To go back to the start
            elif temp == "4":
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue

            #To quit
            elif temp == "5":
                conn.commit()
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                break



            #For invalid entries, go back to start
            else:
                print("Invalid Entry, Please try again")
                f.write("%d) %s || Error || Invalid Entry || %s || Administrator Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue



        #For going back to start on entering an invalid password
        else:
            print("Invalid Password, Please try again")
            f.write("%d) %s || Error || Invalid Password Attempt || %s || Administrator Mode\n" %(i,current,name))
            i += 1
            p = open("ROOT", "w+")
            p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
            p = open("ROOT", "r+")
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            winsound.Beep(frequency, duration)
            continue



    #User Mode: Used to deposit an item or withdraw an item
    elif temp == "2":
        print("Available Space: ",cap)
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        temp = input("What do you wish to do:\n1) Load Stock\n2) Withdraw Stock \n3) Back\n4) Quit\nEnter Your Choice:")
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        #type = input("Enter type of Stock: ")



        #Loop to deposit the specific item
        if temp == "1":
            print("Please Scan the QR Code or Press C to Cancel:")
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            try: type,cost = scan()
            except:
                print("Scanning Cancelled, Try Again")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            try:
                winsound.Beep(frequency,1000)
                quant = int(input("Enter the Quantity: "))
            except:
                print("Stock cannot be a float number, Try Again")
                f.write("%d) %s || Attempt to Deposit a Float Number Stock || Invalid Entry || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            if quant < 0:
                print("Stock Quantity cannot be Negative, Try Again")
                f.write("%d) %s || Attempt to Deposit a Negative Number Stock || Invalid Entry || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            else: None
            temp = cap - quant
            if temp <0:
                print("Space not available, Try Again")
                f.write("%d) %s || Error || Deposit Amount more than Storage Capacity || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            else:
                cap -= quant
            cur.execute('''SELECT * FROM Stocks WHERE Name_of_Owner = ? AND Type_of_Stock = ? AND Cost = ?''',(name,type,cost))
            data = cur.fetchall()
            if len(data) == 0:
                cur.execute('''INSERT INTO Stocks (Name_of_Owner,Type_of_Stock,Loading_Date,Cost, Quantity) VALUES (?,?,?,?,?)''', (name,type,today,cost,quant))
                conn.commit()
                f.write("%d) %s || DEPOSIT: || Name: %s || Stock Type: %s || Cost of Stock Per Piece: %d || Quantity Deposit: %d\n" %(i,current,name,type,cost,quant))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("Entry Registered Successfully")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                conn.commit()
                winsound.Beep(frequency, duration)
                continue
            cur.execute('''UPDATE Stocks SET Loading_Date = ?,Quantity = Quantity + ? WHERE Name_of_Owner = ? AND Type_of_Stock = ? AND Cost = ?''',(today,quant,name,type,cost))
            f.write("%d) %s || DEPOSIT: || Name: %s || Stock Type: %s || Cost of Stock Per Piece: %d || Quantity Deposit: %d\n" %(i,current,name,type,cost,quant))
            i += 1
            p = open("ROOT", "w+")
            p.write("%s\n%d\n%d\n%d" %(passwd,i,cap,capm))
            p = open("ROOT", "r+")
            conn.commit()



        #Loop to withdraw the specific item
        elif temp == "2":
            cur.execute('''SELECT * FROM Stocks WHERE Name_of_Owner = ?''',(name,))
            data = cur.fetchall()
            if len(data) == 0:
                print("You have not Deposit Anything. Hence, You are not Authorized to Withdraw. Try Again")
                f.write("%d) %s || Error || Unauthorized User for Withdrawal || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            else: None

            print("Please Scan the QR Code or Press C to Cancel:")
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            try: type,cost = scan()
            except:
                print("Scanning Cancelled, Try Again")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            try:
                winsound.Beep(frequency, 1000)
                quant = int(input("Enter the Quantity: "))
            except:
                print("Stock cannot be a float number, Try Again")
                f.write("%d) %s || Attempt to Withdraw a Float Number Stock || Invalid Entry || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            if quant < 0:
                print("Stock Quantity cannot be Negative, Try Again")
                f.write("%d) %s || Attempt to Withdraw a Negative Number Stock || Invalid Entry || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            else: None
            if quant > capm:
                print("Required Quantity of Stock Not Available, Try Again")
                f.write("%d) %s || Error || Withdrawal Amount more than Storage Capacity || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            else: None



            #Checking if the specific row exists
            cur.execute('''SELECT * FROM Stocks WHERE Name_of_Owner = ? AND Type_of_Stock = ? AND Cost = ?''',(name,type,cost))
            data = cur.fetchall()
            if len(data) == 0:
                print("No such entry found, Try Again")
                f.write("%d) %s || Error || Entry not found for Withdrawal || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            else: None



            #If entry found, check if the required quantity is available in the stock
            cur.execute('''SELECT Quantity FROM Stocks WHERE Name_of_Owner = ? AND Type_of_Stock = ? AND Cost = ?''',(name,type,cost))
            data = cur.fetchall()
            data = int(data[0][0])
            if (data - quant) < 0:
                print("Requested Quantity not available, Try Again")
                f.write("%d) %s || Error || Requested Quantity not available for Withdrawal || %s || User Mode\n" %(i,current,name))
                i += 1
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
                print("---------------------------------------------------------------------------------------------------------------------------------------")
                winsound.Beep(frequency, duration)
                continue
            else: None



            #Update for departure if the row exist
            cur.execute('''UPDATE Stocks SET Departing_Date = ?,Quantity = Quantity - ? WHERE Name_of_Owner = ? AND Type_of_Stock = ? AND Cost = ?''',(today,quant,name,type,cost))
            conn.commit()
            cur.execute('''SELECT Quantity FROM Stocks WHERE Name_of_Owner = ? AND Type_of_Stock = ? AND Cost = ?''',(name,type,cost))
            data = cur.fetchall()
            data = int(data[0][0])
            print("Withdrawal Successful, Remaining Quantity of your Stock of Type",type,"is:",data)
            f.write("%d) %s || WITHDRAWAL: || Name: %s || Stock Type: %s || Cost of Stock Per Piece: %d || Quantity Withdrew: %d\n" %(i,current,name,type,cost,quant))
            i += 1
            cap += quant
            p = open("ROOT", "w+")
            p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
            p = open("ROOT", "r+")
            if data == 0:
                #Delete Empty Entries
                cur.execute('''DELETE FROM Stocks WHERE Name_of_Owner = ? AND Type_of_Stock = ? AND Cost = ? AND Quantity = 0''',(name,type,cost))
                f.write("%d) %s || Empty Entry Deleted || Name: %s || Stock Type: %s || Cost of Stock Per Piece: %d || Stock Empty\n" %(i,current,name,type,cost))
                print("Since your Stock of Type",type,"is Empty, We are deleting your Entry")
                i += 1
                cap += quant
                p = open("ROOT", "w+")
                p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
                p = open("ROOT", "r+")
            else: None



        #To go back to the start
        elif temp == "3":
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            winsound.Beep(frequency, duration)
            continue

        #To quit
        elif temp == "4":
            conn.commit()
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            winsound.Beep(frequency, duration)
            break



        #Go back to start for an invalid entry
        else:
            print("Invalid Entry, Please Choose an Option from '1', '2', '3' or '4'. Try Again")
            f.write("%d) %s || Error || Invalid Entry || %s || User Mode\n" %(i,current,name))
            i += 1
            p = open("ROOT", "w+")
            p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
            p = open("ROOT", "r+")
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            winsound.Beep(frequency, duration)
            continue



    #To quit the program
    elif temp == "3":
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        winsound.Beep(frequency, duration)
        break



    #Go back to start when there is an invalid entry
    else:
        print("Invalid Entry, Please Choose a Mode of Operation from '1', '2' or '3'. Try Again")
        f.write("%d) %s || Error || Invalid Entry || %s || Main Menu \n" %(i,current,name))
        i += 1
        p = open("ROOT", "w+")
        p.write("%s\n%d\n%d\n%d\n" %(passwd,i,cap,capm))
        p = open("ROOT", "r+")
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        winsound.Beep(frequency, duration)
        continue



    #Save to database
    conn.commit()
    print("Entry Registered Successfully")
    print("---------------------------------------------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------------------------------------------")
    winsound.Beep(frequency, duration)
