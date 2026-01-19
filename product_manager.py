from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class ProductManager:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Product Manager")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()
        
        self.var_pid = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        # Title
        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        lbl_category = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=110)
        lbl_name = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30, y=160)
        
        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=60, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=110, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=160, width=200)

        # Buttons
        btn_add = Button(product_Frame, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_Frame, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=340, y=400, width=100, height=40)

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_search_by, values=("Select", "Name"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_search_txt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10, width=200)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # Product List
        p_Frame = Frame(self.root, bd=3, relief=RIDGE)
        p_Frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_Frame, orient=VERTICAL)
        scrollx = Scrollbar(p_Frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_Frame, columns=("pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Quantity")

        self.product_table.column("pid", width=90)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        con = sqlite3.connect(database='billing_system.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product Name must be required", parent=self.root)
            else:
                cur.execute("Select * from products where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Product already present, try different", parent=self.root)
                else:
                    cur.execute("Insert into products (name, price, quantity) values(?, ?, ?)", (
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
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

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_name.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])

    def update(self):
        con = sqlite3.connect(database='billing_system.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please Select Product from list", parent=self.root)
            else:
                cur.execute("Select * from products where id=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute("Update products set name=?, price=?, quantity=? where id=?", (
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database='billing_system.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Please Select Product from list", parent=self.root)
            else:
                cur.execute("Select * from products where id=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from products where id=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_pid.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_search_txt.set("")
        self.var_search_by.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database='billing_system.db')
        cur = con.cursor()
        try:
            if self.var_search_by.get()=="Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_search_txt.get()=="":
                messagebox.showerror("Error", "Enter input to search", parent=self.root)
            else:
                cur.execute("select * from products where name LIKE '%"+self.var_search_txt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
