# Bank Management System

## Overview
The **Bank Management System** is a Python-MySQL based application developed for managing banking operations efficiently.  
It allows bank officials to manage customer accounts and transactions securely.

- **Front-end:** Python 3.8.5  
- **Database:** MySQL  
- **Connectivity:** Python-MySQL Connectivity  

---

# Features

- Open a New Account
- Close an Account
- Modify Existing Account Details
- Display All Customer Details
- Display a Specific Customer's Details
- Deposit Amount
- Withdraw Amount
- Display Transactions
- Display Balance of All Customers

---

# Database

The project uses a database named:

```sql
bama
```

## Tables

### 1. `accounts`
Stores customer account details such as:
- Account Number
- Customer Name
- Aadhar Number
- Address
- Mobile Number
- Email ID
- Balance Amount

### 2. `transaction`
Stores transaction details such as:
- Account Number
- Transaction Amount
- Transaction Type
- Transaction Date

---

# Authentication

A CSV file named:

```text
passwords.csv
```

is used to store usernames and passwords of bank officials for secure login access.

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.8.5 | Application Development |
| MySQL | Database Management |
| CSV | Login Authentication |

---

# How To Run

## Step 1
Install Python and MySQL.

## Step 2
Create the database:

```sql
CREATE DATABASE bama;
```

## Step 3
Run the project:

```bash
python main.py
```

---

# Conclusion

This project provides a simple banking management solution using Python and MySQL for handling customer accounts and transactions efficiently.
