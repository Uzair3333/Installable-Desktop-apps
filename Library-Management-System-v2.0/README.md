# 📚 Library Management System v2.0

A full-featured **Desktop Library Management System** built using **Python & Tkinter**.  
Designed with **role-based access**, persistent CSV storage, and a modern dashboard.

---

## 🚀 Features

### 🔐 Authentication System
- Admin, Librarian, and Member roles
- Secure login with role-based dashboards

### 📚 Book Management
- Add, view, search, edit, and delete books
- ISBN validation
- Availability tracking

### 👥 Member Management
- Register, view, edit, and delete members
- Prevent deletion if books are borrowed

### 🔄 Transactions
- Borrow & return books
- Due date tracking
- Overdue detection

### 📊 Dashboard
- Total books
- Available vs borrowed books
- Members count
- Transaction statistics

### ⚠️ Overdue System
- Automatic overdue calculation
- Alerts for near-due & overdue books

---

## 🛠 Tech Stack

- **Python 3**
- **Tkinter** (GUI)
- **CSV Files** (Persistent storage)
- **PyInstaller** (Executable)
- **Inno Setup** (Installer)

---

## 📂 Project Structure
Library-Management-System-v2.0/
├── gui.py
├── main.py
├── data/
│ ├── books.csv
│ ├── members.csv
│ ├── users.csv
│ └── transactions.csv
└── assets/


---

## 🔑 Default Login Credentials

| Role | Username | Password |
|----|--------|---------|
| Admin | admin | admin123 |
| Librarian | librarian | lib123 |
| Member | member | mem123 |

---

## ▶️ How to Run (Development)

```bash
python gui.py