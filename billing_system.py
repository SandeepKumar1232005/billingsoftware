from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Billing System")
        self.root.config(bg="white")

        self.cart_list = []
        self.chk_print = 0

        # Variables
        self.var_search = StringVar()
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        
        # Product Vars for cart
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()
        self.var_cal_input = StringVar()  # For quantity input

        # Title
        title = Label(self.root, text="Billing Area", bd=12, relief=GROOVE, bg="#f39c12", fg="white", font=("times new roman", 30, "bold"), pady=2).pack(fill=X)

        # Customer Frame
        F1 = LabelFrame(self.root, text="Customer Details", font=("times new roman", 15, "bold"), bd=10, fg="gold", bg="#2c3e50")
        F1.place(x=0, y=80, relwidth=1)

        cname_lbl = Label(F1, text="Customer Name", bg="#2c3e50", fg="white", font=("times new roman", 18, "bold")).grid(row=0, column=0, padx=20, pady=5)
        cname_txt = Entry(F1, textvariable=self.var_cname, width=20, font="arial 15", bd=7, relief=SUNKEN).grid(row=0, column=1, pady=5, padx=10)

        cphn_lbl = Label(F1, text="Phone No.", bg="#2c3e50", fg="white", font=("times new roman", 18, "bold")).grid(row=0, column=2, padx=20, pady=5)
        cphn_txt = Entry(F1, textvariable=self.var_contact, width=20, font="arial 15", bd=7, relief=SUNKEN).grid(row=0, column=3, pady=5, padx=10)

        # Product Search Frame
        F2 = LabelFrame(self.root, text="Select Product", font=("times new roman", 15, "bold"), bd=10, fg="gold", bg="#2c3e50")
        F2.place(x=0, y=180, width=380, height=380)

        lbl_search = Label(F2, text="Search By Name", bg="#2c3e50", fg="white", font=("times new roman", 15, "bold")).grid(row=0, column=0, padx=2, pady=10, sticky="w")
        txt_search = Entry(F2, textvariable=self.var_search, font=("times new roman", 15, "bold"), bg="lightyellow").grid(row=0, column=1, padx=2, pady=10)
        btn_search = Button(F2, text="Show", command=self.search, font=("times new roman", 12, "bold"), bg="#2196f3", fg="white", cursor="hand2").grid(row=0, column=2, padx=2, pady=10)

        # Product Search Result (Treeview)
        product_frame = Frame(F2, bd=3, relief=RIDGE)
        product_frame.place(x=2, y=50, width=360, height=180)

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(product_frame, columns=("pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="PID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")

        self.product_table.column("pid", width=40)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=80)
        self.product_table.column("qty", width=60)
        
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        # Product Details Selection
        lbl_pname = Label(F2, text="Product Name", font=("times new roman", 15, "bold"), bg="#2c3e50", fg="lightyellow").place(x=2, y=240)
        txt_pname = Entry(F2, textvariable=self.var_pname, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=2, y=270, width=150)

        lbl_pprice = Label(F2, text="Price Per Qty", font=("times new roman", 15, "bold"), bg="#2c3e50", fg="lightyellow").place(x=160, y=240)
        txt_pprice = Entry(F2, textvariable=self.var_price, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=160, y=270, width=100)
        
        lbl_pqty = Label(F2, text="Quantity", font=("times new roman", 15, "bold"), bg="#2c3e50", fg="lightyellow").place(x=270, y=240)
        txt_pqty = Entry(F2, textvariable=self.var_cal_input, font=("times new roman", 15), bg="lightyellow").place(x=270, y=270, width=80)

        btn_add_cart = Button(F2, text="Add | Update Cart", command=self.add_cart, font=("times new roman", 15, "bold"), bg="orange", fg="black", cursor="hand2").place(x=10, y=310, width=340, height=30)

        # Cart Frame
        F3 = Frame(self.root, bd=10, relief=GROOVE)
        F3.place(x=390, y=180, width=540, height=380)

        cart_title = Label(F3, text="Cart Items", font=("times new roman", 15, "bold"), bg="gray", fg="white").pack(side=TOP, fill=X)
        
        scrolly_cart = Scrollbar(F3, orient=VERTICAL)
        scrollx_cart = Scrollbar(F3, orient=HORIZONTAL)

        self.Cart_Table = ttk.Treeview(F3, columns=("pid", "name", "price", "qty", "total"), yscrollcommand=scrolly_cart.set, xscrollcommand=scrollx_cart.set)
        scrollx_cart.pack(side=BOTTOM, fill=X)
        scrolly_cart.pack(side=RIGHT, fill=Y)
        scrollx_cart.config(command=self.Cart_Table.xview)
        scrolly_cart.config(command=self.Cart_Table.yview)

        self.Cart_Table.heading("pid", text="PID")
        self.Cart_Table.heading("name", text="Name")
        self.Cart_Table.heading("price", text="Price")
        self.Cart_Table.heading("qty", text="Qty")
        self.Cart_Table.heading("total", text="Total")

        self.Cart_Table.column("pid", width=40)
        self.Cart_Table.column("name", width=90)
        self.Cart_Table.column("price", width=90)
        self.Cart_Table.column("qty", width=40)
        self.Cart_Table.column("total", width=90)

        self.Cart_Table.pack(fill=BOTH, expand=1)

        # Bill Area
        F4 = Frame(self.root, bd=10, relief=GROOVE, bg="white")
        F4.place(x=940, y=180, width=400, height=380)
        
        bill_title = Label(F4, text="Bill Summary", font=("times new roman", 15, "bold"), bd=7, relief=GROOVE, bg="gray", fg="white").pack(fill=X)
        
        scrolly_bill = Scrollbar(F4, orient=VERTICAL)
        self.txt_bill_area = Text(F4, yscrollcommand=scrolly_bill.set)
        scrolly_bill.pack(side=RIGHT, fill=Y)
        scrolly_bill.config(command=self.txt_bill_area.yview)
        self.txt_bill_area.pack(fill=BOTH, expand=1)

        # Billing Menu (Bottom)
        F5 = LabelFrame(self.root, text="Bill Menu", font=("times new roman", 15, "bold"), bd=10, fg="gold", bg="#2c3e50")
        F5.place(x=0, y=565, relwidth=1, height=135)
        
        self.var_amnt = StringVar()
        self.var_tax = StringVar()
        self.var_net_pay = StringVar()

        lbl_amnt = Label(F5, text="Sub Total", font=("times new roman", 15, "bold"), bg="#2c3e50", fg="white").place(x=20, y=10)
        txt_amnt = Entry(F5, textvariable=self.var_amnt, font=("times new roman", 15, "bold"), bg="lightyellow", state='readonly').place(x=120, y=10, width=120)

        lbl_tax = Label(F5, text="Tax (5%)", font=("times new roman", 15, "bold"), bg="#2c3e50", fg="white").place(x=20, y=50)
        txt_tax = Entry(F5, textvariable=self.var_tax, font=("times new roman", 15, "bold"), bg="lightyellow", state='readonly').place(x=120, y=50, width=120)

        lbl_net = Label(F5, text="Net Pay", font=("times new roman", 15, "bold"), bg="#2c3e50", fg="white").place(x=260, y=30)
        txt_net = Entry(F5, textvariable=self.var_net_pay, font=("times new roman", 15, "bold"), bg="lightyellow", state='readonly').place(x=360, y=30, width=120)

        btn_generate = Button(F5, text="Generate Bill", command=self.generate_bill, font=("times new roman", 15, "bold"), bg="#3f51b5", fg="white", cursor="hand2").place(x=550, y=20, width=150, height=50)
        btn_clear = Button(F5, text="Clear", command=self.clear_all, font=("times new roman", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2").place(x=710, y=20, width=150, height=50)
        btn_exit = Button(F5, text="Exit", font=("times new roman", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.root.destroy).place(x=870, y=20, width=150, height=50)

        self.welcome_bill()
        self.show_products()

    def show_products(self):
        con = sqlite3.connect(database='billing_system.db')
        cur = con.cursor()
        try:
            cur.execute("select * from products")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database='billing_system.db')
        cur = con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error", "Enter input to search", parent=self.root)
            else:
                cur.execute("select * from products where name LIKE '%"+self.var_search.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_stock.set(row[3])
            self.var_cal_input.set('1')

    def add_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please Select Product from list", parent=self.root)
        elif self.var_cal_input.get() == "":
            messagebox.showerror("Error", "Enter Quantity", parent=self.root)
        elif int(self.var_cal_input.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Insufficient Stock!", parent=self.root)
        else:
            price_cal = float(self.var_price.get())
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_cal_input.get(), price_cal * int(self.var_cal_input.get())]
            
            # Check if product already in cart
            present = 'no'
            index = -1
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    index = self.cart_list.index(row)
                    break 
            
            if present == 'yes':
                op = messagebox.askyesno('Confirm', "Product already present, Do you want to Update or Remove from Cart List?", parent=self.root)
                if op == True:
                    if self.var_cal_input.get() == "0":
                         self.cart_list.pop(index)
                    else:
                        self.cart_list[index][3] = self.var_cal_input.get() #update qty
                        self.cart_list[index][4] = float(self.var_price.get()) * int(self.var_cal_input.get()) #update total
            else:
                 self.cart_list.append(cart_data)
            
            self.show_cart()
            self.bill_updates()

    def show_cart(self):
        try:
            self.Cart_Table.delete(*self.Cart_Table.get_children())
            for row in self.cart_list:
                self.Cart_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def bill_updates(self):
        self.bill_amnt = 0
        for row in self.cart_list:
            self.bill_amnt += float(row[4])
        
        self.bill_tax = (self.bill_amnt * 5) / 100
        self.net_pay = self.bill_amnt + self.bill_tax

        self.var_amnt.set(str(self.bill_amnt))
        self.var_tax.set(str(self.bill_tax))
        self.var_net_pay.set(str(self.net_pay))

    def welcome_bill(self):
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert(END, "\t\tBilling Software\n")
        self.txt_bill_area.insert(END, f"\n Bill Number : {str(int(time.time()))}")
        self.txt_bill_area.insert(END, f"\n Customer Name : {self.var_cname.get()}")
        self.txt_bill_area.insert(END, f"\n Phone Number : {self.var_contact.get()}")
        self.txt_bill_area.insert(END, f"\n=================================================")
        self.txt_bill_area.insert(END, f"\n Product\t\tQty\t\tPrice\t\tTotal")
        self.txt_bill_area.insert(END, f"\n=================================================")

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
             messagebox.showerror("Error", "Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
             messagebox.showerror("Error", "Please add products to cart", parent=self.root)
        else:
            self.welcome_bill()
            for row in self.cart_list:
                 self.txt_bill_area.insert(END, f"\n {row[1]}\t\t{row[3]}\t\t{row[2]}\t\t{row[4]}")
            
            self.txt_bill_area.insert(END, f"\n=================================================")
            self.txt_bill_area.insert(END, f"\n Sub Total :\t\t\t{self.bill_amnt}")
            self.txt_bill_area.insert(END, f"\n Tax (5%) :\t\t\t{self.bill_tax}")
            self.txt_bill_area.insert(END, f"\n Total (Inc. Tax) :\t\t\t{self.net_pay}")
            self.txt_bill_area.insert(END, f"\n=================================================")
            
            self.save_bill()

    def save_bill(self):
        op = messagebox.askyesno("Save Bill", "Do you want to save the Bill?", parent=self.root)
        if op == True:
            # 1. Save to Database
            # 2. Update Stock
            # 3. Save as Text File
            invoice_id = str(int(time.time()))
            con = sqlite3.connect(database='billing_system.db')
            cur = con.cursor()
            try:
                # Insert Invoice
                cur.execute("INSERT INTO invoices (customer_name, contact, total_amount) VALUES (?, ?, ?)", (
                    self.var_cname.get(),
                    self.var_contact.get(),
                    self.net_pay
                ))
                
                # Get ID of inserted invoice (though we generated a time-based one for display, DB has auto-increment ID)
                # But for consistency let's use the DB's ID or the timestamp?
                # The schema says ID is auto-increment.
                # Let's search by something or just trust the process.
                # Actually, I used time.time() as bill number, maybe store that?
                # My schema doesn't have 'invoice_number' column, just 'id'.
                # Let's use the 'id' from DB for the actual record linkage.
                
                db_invoice_id = cur.lastrowid
                
                # Insert Items & Update Stock
                for row in self.cart_list:
                    # row: [pid, name, price, qty, total]
                    pid = row[0]
                    name = row[1]
                    price = row[2]
                    qty = int(row[3])
                    total = row[4]
                    
                    cur.execute("INSERT INTO invoice_items (invoice_id, product_name, quantity, price, total) VALUES (?, ?, ?, ?, ?)", (
                        db_invoice_id, name, qty, price, total
                    ))
                    
                    # Update Stock
                    cur.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (qty, pid))
                
                con.commit()
                messagebox.showinfo("Success", "Bill Saved Successfully", parent=self.root)
                self.chk_print = 1
                
                # Save as Text File
                bill_content = self.txt_bill_area.get('1.0', END)
                with open(f"bill_{invoice_id}.txt", "w") as f:
                    f.write(bill_content)
                
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_all(self):
        self.cart_list = []
        self.var_cname.set("")
        self.var_contact.set("")
        self.var_search.set("")
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_stock.set("")
        self.var_cal_input.set("")
        self.var_amnt.set("")
        self.var_tax.set("")
        self.var_net_pay.set("")
        self.show_products()
        self.show_cart()
        self.welcome_bill()
