from tkinter import *
from tkinter import messagebox
import database

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Billing Software | Developed by Antigravity")
        self.root.config(bg="white")
        
        # Initialize Database
        database.init_db()
        
        # Title
        title = Label(self.root, text="Billing Software", bd=12, relief=GROOVE, bg="#2c3e50", fg="white", font=("times new roman", 30, "bold"), pady=2).pack(fill=X)

        # Menu Frame
        F1 = LabelFrame(self.root, text="Menu", font=("times new roman", 15, "bold"), bd=10, fg="gold", bg="#2c3e50")
        F1.place(x=0, y=80, relwidth=1)

        btn_product = Button(F1, text="Products", command=self.product_details, font=("times new roman", 18, "bold"), bg="#0f4d7d", fg="white", cursor="hand2").grid(row=0, column=0, padx=20, pady=5)
        btn_billing = Button(F1, text="Billing", command=self.billing_section, font=("times new roman", 18, "bold"), bg="#0f4d7d", fg="white", cursor="hand2").grid(row=0, column=1, padx=20, pady=5)
    
    def product_details(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductManager(self.new_win)

    def billing_section(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = BillingSystem(self.new_win)

from product_manager import ProductManager
from billing_system import BillingSystem

if __name__ == "__main__":
    root = Tk()
    obj = BillingApp(root)
    root.mainloop()
