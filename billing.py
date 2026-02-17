from tkinter import *
from tkinter import ttk, messagebox
from database import fetchall, execute
import time
import os
import tempfile


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # ------------ variables --------------
        self.cart_list = []
        self.chk_print = 0
        self.var_search = StringVar()
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        self.var_cal_input = StringVar()
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        # ------------- title --------------
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20,
        ).place(x=0, y=0, relwidth=1, height=70)

        # ------------ logout button -----------
        btn_logout = Button(
            self.root,
            text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow",
            cursor="hand2",
        ).place(x=1150, y=10, height=50, width=150)

        # ------------ clock -----------------
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=("times new roman", 15),
            bg="#4d636d",
            fg="white",
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # -------------- product frame -----------------
        product_frame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        product_frame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(
            product_frame1,
            text="All Products",
            font=("goudy old style", 20, "bold"),
            bg="#262626",
            fg="white",
        ).pack(side=TOP, fill=X)

        product_frame2 = Frame(product_frame1, bd=2, relief=RIDGE, bg="white")
        product_frame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(
            product_frame2,
            text="Search Product | By Name",
            font=("times new roman", 15, "bold"),
            bg="white",
            fg="green",
        ).place(x=2, y=5)

        lbl_search = Label(
            product_frame2,
            text="Product Name",
            font=("times new roman", 15, "bold"),
            bg="white",
        ).place(x=2, y=45)
        txt_search = Entry(
            product_frame2,
            textvariable=self.var_search,
            font=("times new roman", 15),
            bg="lightyellow",
        ).place(x=128, y=47, width=150, height=22)
        btn_search = Button(
            product_frame2,
            text="Search",
            command=self.search,
            font=("goudy old style", 15),
            bg="#2196f3",
            fg="white",
            cursor="hand2",
        ).place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(
            product_frame2,
            text="Show All",
            command=self.show,
            font=("goudy old style", 15),
            bg="#083531",
            fg="white",
            cursor="hand2",
        ).place(x=285, y=10, width=100, height=25)

        product_frame3 = Frame(product_frame1, bd=3, relief=RIDGE)
        product_frame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(product_frame3, orient=VERTICAL)
        scrollx = Scrollbar(product_frame3, orient=HORIZONTAL)
        self.product_table = ttk.Treeview(
            product_frame3,
            columns=("pid", "name", "price", "qty", "status"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"
        self.product_table.column("pid", width=40)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=40)
        self.product_table.column("status", width=90)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        lbl_note = Label(
            product_frame1,
            text="Note: 'Enter 0 Quantity to remove product from the Cart'",
            font=("goudy old style", 12),
            anchor="w",
            bg="white",
            fg="red",
        ).pack(side=BOTTOM, fill=X)

        # -------------- customer frame ---------------
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        cTitle = Label(
            CustomerFrame,
            text="Customer Details",
            font=("goudy old style", 15),
            bg="lightgray",
        ).pack(side=TOP, fill=X)

        lbl_name = Label(
            CustomerFrame, text="Name", font=("times new roman", 15), bg="white"
        ).place(x=5, y=35)
        txt_name = Entry(
            CustomerFrame,
            textvariable=self.var_cname,
            font=("times new roman", 13),
            bg="lightyellow",
        ).place(x=80, y=35, width=180)

        lbl_contact = Label(
            CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white"
        ).place(x=270, y=35)
        txt_contact = Entry(
            CustomerFrame,
            textvariable=self.var_contact,
            font=("times new roman", 15),
            bg="lightyellow",
        ).place(x=380, y=35, width=140)

        cal_cart_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cal_cart_frame.place(x=420, y=190, width=530, height=360)

        # --------------- calculator frame ---------------------
        cal_frame = Frame(cal_cart_frame, bd=9, relief=RIDGE, bg="white")
        cal_frame.place(x=5, y=10, width=268, height=340)

        self.txt_cal_input = Entry(
            cal_frame,
            textvariable=self.var_cal_input,
            font=("arial", 15, "bold"),
            width=21,
            bd=10,
            relief=GROOVE,
            state="readonly",
            justify=RIGHT,
        )
        self.txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = self._create_calc_btn(cal_frame, 7, lambda: self.get_input(7), 1, 0)
        btn_8 = self._create_calc_btn(cal_frame, 8, lambda: self.get_input(8), 1, 1)
        btn_9 = self._create_calc_btn(cal_frame, 9, lambda: self.get_input(9), 1, 2)
        btn_sum = self._create_calc_btn(
            cal_frame, "+", lambda: self.get_input("+"), 1, 3
        )

        btn_4 = self._create_calc_btn(cal_frame, 4, lambda: self.get_input(4), 2, 0)
        btn_5 = self._create_calc_btn(cal_frame, 5, lambda: self.get_input(5), 2, 1)
        btn_6 = self._create_calc_btn(cal_frame, 6, lambda: self.get_input(6), 2, 2)
        btn_sub = self._create_calc_btn(
            cal_frame, "-", lambda: self.get_input("-"), 2, 3
        )

        btn_1 = self._create_calc_btn(cal_frame, 1, lambda: self.get_input(1), 3, 0)
        btn_2 = self._create_calc_btn(cal_frame, 2, lambda: self.get_input(2), 3, 1)
        btn_3 = self._create_calc_btn(cal_frame, 3, lambda: self.get_input(3), 3, 2)
        btn_mul = self._create_calc_btn(
            cal_frame, "*", lambda: self.get_input("*"), 3, 3
        )

        btn_0 = self._create_calc_btn(cal_frame, 0, lambda: self.get_input(0), 4, 0)
        btn_c = self._create_calc_btn(cal_frame, "C", self.clear_cal, 4, 1)
        btn_eq = self._create_calc_btn(cal_frame, "=", lambda: self.perform_cal(), 4, 2)
        btn_div = self._create_calc_btn(
            cal_frame, "/", lambda: self.get_input("/"), 4, 3
        )

        # ------------------ cart frame --------------------
        cart_frame = Frame(cal_cart_frame, bd=3, relief=RIDGE)
        cart_frame.place(x=280, y=8, width=245, height=342)
        self.cart_title = Label(
            cart_frame,
            text="Cart \t Total Products: [0]",
            font=("goudy old style", 15),
            bg="lightgray",
        )
        self.cart_title.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)
        self.cart_table = ttk.Treeview(
            cart_frame,
            columns=("pid", "name", "price", "qty"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cart_table.xview)
        scrolly.config(command=self.cart_table.yview)
        self.cart_table.heading("pid", text="P ID")
        self.cart_table.heading("name", text="Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("qty", text="Quantity")
        self.cart_table["show"] = "headings"
        self.cart_table.column("pid", width=40)
        self.cart_table.column("name", width=100)
        self.cart_table.column("price", width=90)
        self.cart_table.column("qty", width=30)
        self.cart_table.pack(fill=BOTH, expand=1)
        self.cart_table.bind("<ButtonRelease-1>", self.get_data_cart)

        # -------------- add cart widgets frame ---------------
        add_cart_widgets_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        add_cart_widgets_frame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(
            add_cart_widgets_frame,
            text="Product Name",
            font=("times new roman", 15),
            bg="white",
        ).place(x=5, y=5)
        txt_p_name = Entry(
            add_cart_widgets_frame,
            textvariable=self.var_pname,
            font=("times new roman", 15),
            bg="lightyellow",
            state="readonly",
        ).place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(
            add_cart_widgets_frame,
            text="Price Per Qty",
            font=("times new roman", 15),
            bg="white",
        ).place(x=230, y=5)
        txt_p_price = Entry(
            add_cart_widgets_frame,
            textvariable=self.var_price,
            font=("times new roman", 15),
            bg="lightyellow",
            state="readonly",
        ).place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(
            add_cart_widgets_frame,
            text="Quantity",
            font=("times new roman", 15),
            bg="white",
        ).place(x=390, y=5)
        txt_p_qty = Entry(
            add_cart_widgets_frame,
            textvariable=self.var_qty,
            font=("times new roman", 15),
            bg="lightyellow",
        ).place(x=390, y=35, width=120, height=22)

        self.lbl_in_stock = Label(
            add_cart_widgets_frame,
            text="In Stock",
            font=("times new roman", 15),
            bg="white",
        )
        self.lbl_in_stock.place(x=5, y=70)

        btn_clear_cart = Button(
            add_cart_widgets_frame,
            command=self.clear_cart,
            text="Clear",
            font=("times new roman", 15, "bold"),
            bg="lightgray",
            cursor="hand2",
        ).place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(
            add_cart_widgets_frame,
            command=self.add_update_cart,
            text="Add | Update",
            font=("times new roman", 15, "bold"),
            bg="orange",
            cursor="hand2",
        ).place(x=340, y=70, width=180, height=30)

        # ------------------- billing area -------------------
        bill_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_frame.place(x=953, y=110, width=400, height=410)

        lbl_bill_area = Label(
            bill_frame,
            text="Customer Bill Area",
            font=("goudy old style", 20, "bold"),
            bg="#262626",
            fg="white",
        ).pack(side=TOP, fill=X)
        scrolly = Scrollbar(bill_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(bill_frame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # ------------------- billing buttons -----------------------
        bill_menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_menu_frame.place(x=953, y=520, width=400, height=140)

        self.lbl_amnt = Label(
            bill_menu_frame,
            text="Bill Amount\n[0]",
            font=("goudy old style", 15, "bold"),
            bg="#3f51b5",
            fg="white",
        )
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(
            bill_menu_frame,
            text="Discount\n[5%]",
            font=("goudy old style", 15, "bold"),
            bg="#8bc34a",
            fg="white",
        )
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(
            bill_menu_frame,
            text="Net Pay\n[0]",
            font=("goudy old style", 15, "bold"),
            bg="#607d8b",
            fg="white",
        )
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(
            bill_menu_frame,
            text="Print",
            command=self.print_bill,
            cursor="hand2",
            font=("goudy old style", 15, "bold"),
            bg="lightgreen",
            fg="white",
        )
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(
            bill_menu_frame,
            text="Clear All",
            command=self.clear_all,
            cursor="hand2",
            font=("goudy old style", 15, "bold"),
            bg="gray",
            fg="white",
        )
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(
            bill_menu_frame,
            text="Generate Bill",
            command=self.generate_bill,
            cursor="hand2",
            font=("goudy old style", 15, "bold"),
            bg="#009688",
            fg="white",
        )
        btn_generate.place(x=246, y=80, width=160, height=50)

        self.show()
        self.update_date_time()

    # ---------------------- all functions ------------------------------
    def _create_calc_btn(self, frame, text, function, row, col):
        return Button(
            frame,
            text=text,
            font=("arial", 15, "bold"),
            command=function,
            bd=5,
            width=4,
            pady=15,
            cursor="hand2",
        ).grid(row=row, column=col)

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set("")

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        try:
            rows = fetchall(
                "select pid,name,price,qty,status from product where status='Active'"
            )
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def search(self):
        try:
            if self.var_search.get() == "":
                messagebox.showerror(
                    "Error", "Search input should be required", parent=self.root
                )
            else:
                rows = fetchall(
                    "select pid,name,price,qty,status from product where name LIKE ?",
                    ("%" + self.var_search.get() + "%",),
                )
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert("", END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No record found!!!", parent=self.root
                    )
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def get_data(self, ev):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_in_stock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    def get_data_cart(self, ev):
        f = self.cart_table.focus()
        content = self.cart_table.item(f)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_in_stock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror(
                "Error", "Please select product from the list", parent=self.root
            )
        elif self.var_qty.get() == "":
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
        else:
            price_cal = self.var_price.get()
            cart_data = [
                self.var_pid.get(),
                self.var_pname.get(),
                price_cal,
                self.var_qty.get(),
                self.var_stock.get(),
            ]
            # ---------- update cart --------------
            present = "no"
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_ += 1
            if present == "yes":
                op = messagebox.askyesno(
                    "Confirm",
                    "Product already present\nDo you want to Update|Remove from the Cart List",
                    parent=self.root,
                )
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.siscount = 0

        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2]) * int(row[3]))

        self.discount = (self.bill_amnt * 5) / 100
        self.net_pay = self.bill_amnt - self.discount
        self.lbl_amnt.config(text=f"Bill Amnt\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cart_title.config(
            text=f"Cart \t Total Products: [{str(len(self.cart_list))}]"
        )

    def show_cart(self):
        try:
            self.cart_table.delete(*self.cart_table.get_children())
            for row in self.cart_list:
                self.cart_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get() == "" or self.var_contact.get() == "":
            messagebox.showerror(
                "Error", f"Customer Details are required", parent=self.root
            )
        elif len(self.cart_list) == 0:
            messagebox.showerror(
                "Error", f"Please Add product to the Cart!!!", parent=self.root
            )
        else:
            # --------- bill parts ---------
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            fp = open(f"bill/{str(self.invoice)}.txt", "w")
            fp.write(self.txt_bill_area.get("1.0", END))
            fp.close()
            messagebox.showinfo("Saved", "Bill has been generated", parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f"""
\t\tXYZ-Inventory
\t Phone No. 9899459288 , Delhi-110053
{str("=" * 46)}
 Customer Name: {self.var_cname.get()}
 Ph. no. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("=" * 46)}
 Product Name\t\t\tQTY\tPrice
{str("=" * 46)}
"""
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert("1.0", bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f"""
{str("=" * 46)}
Bill Amount\t\t\t\tRs.{self.bill_amnt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("=" * 46)}\n
"""
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                if int(row[3]) != int(row[4]):
                    status = "Active"
                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(
                    END, "\n " + name + "\t\t\t" + row[3] + "\tRs." + price
                )
                # ------------- update qty in product table --------------
                execute(
                    "update product set qty=?,status=? where pid=?", (qty, status, pid)
                )
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_in_stock.config(text=f"In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print = 0
        self.txt_bill_area.delete("1.0", END)
        self.cart_title.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set("")

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}"
        )
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo("Print", "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp(".txt")
            open(new_file, "w").write(self.txt_bill_area.get("1.0", END))
            os.startfile(new_file, "print")
        else:
            messagebox.showinfo(
                "Print", "Please generate bill to print the receipt", parent=self.root
            )


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
