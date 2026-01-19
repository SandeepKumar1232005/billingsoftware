# Billing Software

A desktop-based Billing Software application built with Python, Tkinter, and SQLite. This application allows small businesses to manage product inventory, create invoices, and store transaction records efficiently.

## Features

- **Product Management**
  - Add, Update, Delete Products
  - View Product List
  - Search Products by Name
- **Billing System**
  - Customer Details Entry
  - Real-time Stock Validation
  - Add to Cart functionality
  - Automated Calculation (Subtotal, Tax, Net Pay)
  - Invoice Generation (.txt export)
- **Database**
  - SQLite backend for persistent storage of products and invoices.

## Screenshots

*(Add screenshots of your application here)*

## Installation & Usage

### Prerequisites
- Python 3.x installed on your system.

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/SandeepKumar1232005/billingsoftware.git
   ```
2. Navigate to the project directory:
   ```bash
   cd billingsoftware
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Technologies Used
- **Language**: Python
- **GUI**: Tkinter
- **Database**: SQLite3

## Directory Structure
- `main.py`: Entry point of the application.
- `database.py`: Handles database connection and table initialization.
- `product_manager.py`: Logic for managing products.
- `billing_system.py`: Logic for billing and invoicing.
