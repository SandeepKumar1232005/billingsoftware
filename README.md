# Billing Software Suite

This repository contains a comprehensive Billing Software solution featuring both a standalone **Desktop Application** and a modern **Web Application**. Designed for small businesses to manage inventory, sales, and invoicing efficiently.

## 🚀 Applications

### 1. Desktop Application
Built with **Python (Tkinter)** and **SQLite**. Ideal for offline, single-terminal usage.

**Features:**
- **Product Management**: Add, update, delete, and search products.
- **Billing System**: User-friendly interface for generating bills with stock validation.
- **Invoice Generation**: Auto-generates text-based invoices.
- **Database**: Local SQLite storage (`billing_system.db`).

### 2. Web Application
Built with **Flask (Python)** and **SQLite**. Ideal for network access and remote management.

**Features:**
- **Dashboard**: Overview of total products, bills, and recent sales.
- **Authentication**: Secure login system.
- **Product Management**: Web interface for inventory control.
- **Billing & Point of Sale**: Create bills with dynamic discount calculations (Flat/Percent) and tax handling.
- **Sales History**: View past transactions and total revenue.
- **Invoice View**: Digital invoice generation.
- **Database**: Local SQLite storage (`web_app/billing.db`).

---

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.x installed.
- (For Web App) Flask and dependencies.

### 📥 Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SandeepKumar1232005/billingsoftware.git
   cd billingsoftware
   ```

2. **Install Dependencies (for Web App):**
   ```bash
   pip install flask flask_sqlalchemy
   # Or if a requirements.txt is present:
   # pip install -r requirements.txt
   ```

### ▶️ Running the Applications

#### Option A: Run Desktop Application
```bash
python main.py
```

#### Option B: Run Web Application
```bash
cd web_app
python app.py
```
*Access the web app at `http://127.0.0.1:5000`*
*Default Admin Credentials (if auto-created): `admin` / `admin123`*

---

## 📂 Directory Structure

```
BILLING SOFTWARE/
├── main.py                 # Entry point for Desktop App
├── product_manager.py      # Desktop: Product logic
├── billing_system.py       # Desktop: Billing logic
├── database.py             # Desktop: Database handling
├── billing_system.db       # Desktop: Database file
├── web_app/                # Web Application Directory
│   ├── app.py              # Entry point for Web App
│   ├── billing.db          # Web: Database file
│   ├── templates/          # Web: HTML Templates
│   └── static/             # Web: CSS/JS Assets
└── README.md               # Documentation
```

## 💻 Technologies Used
- **Languages**: Python, HTML, CSS, JavaScript
- **Frameworks**: Flask (Web), Tkinter (Desktop)
- **Database**: SQLite3
