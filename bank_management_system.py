import PySimpleGUI as sg
import mysql.connector
import re
from datetime import datetime
import csv


conn=mysql.connector.connect(host='localhost',user='root',passwd= password ,database= databasename)
cur_conn=conn.cursor()

cur_conn.execute("CREATE DATABASE IF NOT EXISTS bama")
cur_conn.execute("USE bama")

cur_conn.execute("CREATE TABLE IF NOT EXISTS accounts(Account_Number Bigint,Customer_Name VARCHAR(100),Aadhar_Number bigint,Age INT(4),Address VARCHAR(500),Mobile_Number bigint,Occupation VARCHAR(100),Email_ID VARCHAR (100),Date_Of_Birth DATE,Mon_Avg_Bal BIGINT,Balance_Amount BIGINT, PRIMARY KEY(Account_Number))")
cur_conn.execute("create table if not exists transaction(Act_no bigint, tran_amt bigint,tran_type char(1), tran_date TIMESTAMP, foreign key (Act_no) references accounts(Account_Number))")

def valid_name():
    name=input("Enter Name: ")
    if name.replace(' ','').isalpha():
        return name
    else:
        return -1
    
def valid_aadhar():
    flag=True
    while flag:
        try:
            ad=int(input("Enter 12 digits Aadhar Number: "))
            if not len(str(ad)) == 12:
                flag = True
                print("Incorrect Aadhar Number")
            else:
                flag = False
        except:
            print("Incorrect Aadhar Number")
    return ad


def valid_acn():
    flag=True
    while flag:
        try:
            ac=int(input("Enter 11 digits Account Number: "))
            if not len(str(ac)) == 11:
                flag = True
                print("Incorrect Account Number")
            else:
                if account_validate(ac)==0:
                    print("Account Number already exists")
                    flag = True
                else:
                    flag = False
        except:
            print("Incorrect Account Number")
    return ac 

def valid_mod_acn():
    flag=True
    while flag:
        try:
            ac=int(input("Enter 11 digits Account Number: "))
            if not len(str(ac)) == 11:
                flag = True
                print("Incorrect Account Number")
            else:
                if account_validate(ac)==0:
                    flag = False
                else:
                    flag = True
                    print("Incorrect Account Number")
        except:
            print("Incorrect Account Number")
    return ac

def valid_age():
    flag = True
    while flag:
        try:
            age = int(input('Enter Age: '))
            if not len(str(age)) <= 3:
                flag = True 
                print("Incorrect Age")
            else:
                flag=False
        except:
            print('Incorrect Age')
    return age

def valid_addre():
    a=input("Enter Address: ")  
    return a

def valid_mobile():
    flag=True
    while flag:
        try:
            m=int(input("Enter 10 digits Mobile Number: "))
            if not len(str(m)) == 10:
                flag = True
                print("Incorrect Mobile Number")
            else:
                flag = False
        except:
            print("Incorrect Mobile Number")
    return m 
    

def valid_occu():
    occu=input("Enter Occupation: ")
    if occu.replace(' ','').isalpha():
        return occu
    else:
        #print("Incorrect Occupation")
        return -1

def valid_email():
    email=input("Enter Email ID: ")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
      #  print("Valid Email")
        return email
    else:
        #print("Incorrect Email")
        return -1

def valid_dob():
    flag = True
    while flag:
        date_format='%Y-%m-%d'
        date_input=input('Enter (YYYY-MM-DD) Date of Birth :')
        try:
            dob=datetime.strptime(date_input,date_format)
            flag = False
        except ValueError:
            print('Incorrect date format, should be YYYY-MM-DD')
            flag = True
    return dob

def account_validate(acn):
    cur_conn.execute("SELECT count(1) FROM accounts WHERE  Account_Number='"+str(acn)+"'")
    rows=cur_conn.fetchall()
    for row in rows:
        count=row[0]
    if count==1:
        return 0
    else:
        return 1
   

def display_bal_amt():
    query="select Account_Number, Customer_Name, Balance_Amount from accounts"
    cur_conn.execute(query)
    rows=cur_conn.fetchall()
    print('-'*60)
    rows=[("Account Number","Customer Name","Balance Amount"),]+rows
    main=[]
    for i in range(len(rows[0])):
        main.append('')
        for j in range(len(rows)):
            if len(str(rows[j][i]))>len(main[i]):
                main[i]=str(rows[j][i])

    for i in rows:
        for j in range(len(i)):
            print(str(i[j])+(' '*(len(main[j])-len(str(i[j])))), end=' ')
        print()
    print('-'*60)

def valid_dep():
    flag=True
    while flag:
        try:
            dep=int(input("Enter amount to deposit: "))
            if not dep >= 1000:
                flag = True
                print("Incorrect amount")
            else:
                flag = False
        except:
            print("Incorrect amount")
    return dep

def valid_wit():
    flag=True
    while flag:
        try:
            wit=int(input("Enter amount to withdraw: "))
            if not wit > 0:
                flag = True
                print("Incorrect amount")
            else:
                flag = False
        except:
            print("Incorrect amount")
    return wit
      
def new_acc():
    #cur_conn=conn.cursor()
    acc=valid_acn()

    flag = True
    while flag:
        s=valid_name()
        if s == -1:
            print('Invalid Name') 
            flag = True   
        else:
            flag = False
            name=s

    aadhar=valid_aadhar()
    age=valid_age()
    address=valid_addre()
    mobile=valid_mobile()

    flago = True
    while flago:
        o=valid_occu()
        if o == -1:
            print('Invalid Occupation') 
            flago = True   
        else:
            flago = False
            occu=o
    
    flage = True
    while flage:
        e=valid_email()
        if e == -1:
            print('Invalid Email') 
            flage = True   
        else:
            flage = False
            email=e

    dob=valid_dob()
    maba=1000
    dep=valid_dep()
    query="INSERT INTO accounts(Account_Number, Customer_Name, Aadhar_Number, Age, Address, Mobile_Number,Occupation, Email_ID, Date_Of_Birth, Mon_Avg_Bal, Balance_Amount) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    record=(acc,name,aadhar,age,address,mobile,occu,email,dob,maba,dep)
    cur_conn.execute(query,record)
    conn.commit()
    print("Record Entered Successfully!\n")

def close_acc(actn):
    query="DELETE FROM accounts WHERE Account_Number=%s"
    tquery="DELETE FROM transaction WHERE Act_no=%s"
    if account_validate(actn) == 0:
        wreck=(actn,)
        cur_conn.execute(tquery,wreck)
        cur_conn.execute(query,wreck)
        conn.commit()
        if cur_conn.rowcount==0:
            print("Record unavailable")
        else:
            print("Record has been deleted successfully!")
    else:
        print("Invalid Account Number")

def mod_acc():
    acn=valid_mod_acn()

    flag = True
    while flag:
        s=valid_name()
        if s == -1:
            print('Invalid Name') 
            flag = True   
        else:
            flag = False
            n=s

    an=valid_aadhar()
    a=valid_age()
    ad=valid_addre()
    m=valid_mobile()
    
    flago = True
    while flago:
        o1=valid_occu()
        if o1 == -1:
            print('Invalid Occupation') 
            flago = True   
        else:
            flago = False
            o=o1

    flage = True
    while flage:
        e1=valid_email()
        if e1 == -1:
            print('Invalid Email') 
            flage = True   
        else:
            flage = False
            e=e1

    d=valid_dob()
    maba=1000
    l=(n,an,a,ad,m,o,e,d,maba)
    query="update accounts set Customer_Name=%s, Aadhar_Number=%s, Age=%s, Address=%s, Mobile_Number=%s,Occupation=%s, Email_ID=%s, Date_Of_Birth=%s, Mon_Avg_Bal=%s where Account_Number='"+str(acn)+"'"
    cur_conn.execute(query,l)
    conn.commit()
    print("Modified Successfully!")

def display_acc():
    cur_conn.execute("select * from accounts")
    data=cur_conn.fetchall()
    print('-'*149)
    data=[("Account No","Customer Name","Aadhar No","Age","Address","Mobile No","Occupation","Email ID","DOB","Mon_Avg_Bal","Balance Amount"),]+data
    main=[]
    for i in range(len(data[0])):
        main.append('')
        for j in range(len(data)):
            if len(str(data[j][i]))>len(main[i]):
                main[i]=str(data[j][i])

    for i in data:
        for j in range(len(i)):
            print(str(i[j])+(' '*(len(main[j])-len(str(i[j])))), end=' ')
        
        print()
    print('-'*149)

def display_one(acn):
    cur_conn.execute("SELECT * FROM accounts WHERE  Account_Number='"+str(acn)+"'")
    resultset=cur_conn.fetchall()
    print('-'*149)
    #print("Act_no","Cust_name","Aadhar_no","Age","Address","Mobile_no","Occupation","Email_id","DOB","Mon_Avg_Bal","Bal_amt",sep='\t')
    resultset=[("Account No","Customer Name","Aadhar No","Age","Address","Mobile No","Occupation","Email ID","DOB","Mon_Avg_Bal","Balance Amount"),]+resultset
    #print('-'*150)
    main=[]
    for i in range(len(resultset[0])):
        main.append('')
        for j in range(len(resultset)):
            if len(str(resultset[j][i]))>len(main[i]):
                main[i]=str(resultset[j][i])

    for i in resultset:
        for j in range(len(i)):
            print(str(i[j])+(' '*(len(main[j])-len(str(i[j])))), end=' ')
        print()
    print('-'*149)

def display_tran():
    cur_conn.execute("select * from transaction")
    data=cur_conn.fetchall()
    print('-'*80)
    data=[("Account No","Transaction Amount","Transaction Type","Transaction Date"),]+data
    main=[]
    for i in range(len(data[0])):
        main.append('')
        for j in range(len(data)):
            if len(str(data[j][i]))>len(main[i]):
                main[i]=str(data[j][i])

    for i in data:
        for j in range(len(i)):
            print(str(i[j])+(' '*(len(main[j])-len(str(i[j])))), end=' ')
        
        print()
    print('-'*80)

def deposit():
    acn=int(input("Enter 11 digit account number: "))
    if account_validate(acn)==0:
        dep_amt=valid_dep()
        d="D"
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        insert_i="INSERT INTO transaction (Act_no, tran_amt,Tran_type, tran_date) VALUES(%s,%s,%s,%s)" 
        record_i=(acn,dep_amt,d,dt_string)
        cur_conn.execute(insert_i,record_i)
        
        update_u="UPDATE ACCOUNTS set Balance_Amount=Balance_Amount+%s where Account_Number=%s"
        record_u=(dep_amt,acn)
        cur_conn.execute(update_u,record_u)
        conn.commit()
        print("Deposited successfully!")
    else:
        print("Invalid Account Number")
    
   # cur_conn.execute("INSERT INTO transaction VALUES('+(acn)+','(dep_amt)','"+str(d)+"','"+datetime(dt_string)+")")
   # cur_conn.execute("update accounts set Balance_Amount=Balance_Amount+'+(dep_amt)+' where Account_Number='"+str(acn)+"'")
    

def withdraw():
    acn=int(input("Enter 11 digit account number: "))
    if account_validate(acn)==0:
        wit_amt=valid_wit()
        w="W"
        query="select Balance_Amount from accounts where Account_Number='"+str(acn)+"'"
        cur_conn.execute(query)
        rows=cur_conn.fetchall()
        for row in rows:
            amt=row[0]

        #print (amt)

        if amt-wit_amt < 1000:
            print("Withdrawal unsuccessful\nWithdrawal limit =",amt-1000)
        else:
        
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

            insert_i="INSERT INTO transaction (Act_no, tran_amt,Tran_type, tran_date) VALUES(%s,%s,%s,%s)" 
            record_i=(acn,wit_amt,w,dt_string)
            cur_conn.execute(insert_i,record_i)    
        
        
            update_u="UPDATE ACCOUNTS set Balance_Amount=Balance_Amount-%s where Account_Number=%s"
            record_u=(wit_amt,acn)
            cur_conn.execute(update_u,record_u)
            conn.commit()
            print("Withdrawn successfully!")
    

        #cur_conn.execute("update accounts set Balance_Amount=Balance_Amount-'"+str(wit_amt)+"' where Account_Number='"+str(acn)+"'")
        conn.commit()
        #print("Withdrawn successfully!")
    else:
        print("Invalid Account Number")

def main():
    if conn.is_connected():
        while True:
            print('#'*60)
            print()
            print('\t',' ','BANK MANAGEMENT SYSTEM','\n')
            print('\t\tMAIN MENU')
            print()
            print('''\t1. Open A New Account
\t2. Closing An Account
\t3. Modifying Existing Account
\t4. Display all Customer Details 
\t5. Display 1 Customer's Details
\t6. Deposit
\t7. Withdraw
\t8. Display transactions
\t9. Balance Amount of all Customers 
\t10. Exit''')
            print()
            print('#'*60)
            print('\t')
            choice=input('Enter your choice: ')
            if choice=='1':
                new_acc()
            elif choice=='2':
                actn=input("Enter customer's 11 digit account number to close account: ")
                close_acc(actn)
            elif choice=='3':
                mod_acc()
            elif choice=='4':
                display_acc()
            elif choice=='5':
                cust_aid=input("Enter Customer's Account Number: ")
                if account_validate(cust_aid)==0:
                    display_one(cust_aid)
                else:
                    print("Account Number does not exist")
            elif choice=='6':
                deposit()
            elif choice=='7':
                withdraw()
            elif choice=='8':
                display_tran()
            elif choice=='9':
                display_bal_amt()
            elif choice=='10':
                end_page()
                conn.close()
                break
            else:
                print('Incorrect Choice!')
    else:
        print("MySQL Connection Error")

def end_page():
    sg.popup_auto_close("Thank You!")

def login_page():
    layout = [[sg.Text("Username: "), sg.Input(key="-Username-", do_not_clear=False)],
          [sg.Text("Password: "), sg.InputText('',key='-Password-', password_char='*')],
          [sg.Button("Submit"),sg.Button("Exit")]]

    window = sg.Window('Login', layout, modal=True)

    def verify_pwd(username,password):
        with open ("bank-managment\passwords.csv","r") as f:
            ro = csv.reader(f)
            found = False
            for i in ro:
                if i[0]==username and i[1]==password:
                    window.close()
                    main()
                    found = True
            if found == False:
                sg.popup("Incorrect Username or Password")
                window.close()
                login_page()

    while True:
        event, values = window.read()
        if event == "Submit":
            username=values["-Username-"]
            password=values["-Password-"]
            verify_pwd(username,password)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        window.close()

login_page()