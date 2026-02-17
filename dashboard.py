from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import os
from database import fetchall

from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClass
from sales import SalesClass

# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_DIR, exist_ok=True)
# ---------------------------------------------------


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # ------------- title --------------
        self.icon_title = PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
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

        # ---------------- left menu ---------------
        self.menu_logo = Image.open(os.path.join(IMAGE_DIR, "menu_im.png"))
        self.menu_logo = self.menu_logo.resize((200, 200))
        self.menu_logo = ImageTk.PhotoImage(self.menu_logo)

        left_menu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_menu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo = Label(left_menu, image=self.menu_logo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(
            left_menu, text="Menu", font=("times new roman", 20), bg="#009688"
        ).pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file=os.path.join(IMAGE_DIR, "side.png"))

        btn_employee = self._create_menu_btn(left_menu, "Employee", self.employee)
        btn_supplier = self._create_menu_btn(left_menu, "Supplier", self.supplier)
        btn_category = self._create_menu_btn(left_menu, "Category", self.category)
        btn_product = self._create_menu_btn(left_menu, "Products", self.product)
        btn_sales = self._create_menu_btn(left_menu, "Sales", self.sales)
        btn_exit = self._create_menu_btn(left_menu, "Exit", self.root.destroy)

        # ----------- content ----------------

        self.lbl_employee = self._create_content_lbl("Total Employee\n{ 0 }", "#33bbf9")
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = self._create_content_lbl("Total Supplier\n{ 0 }", "#ff5722")
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = self._create_content_lbl("Total Category\n{ 0 }", "#009688")
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = self._create_content_lbl("Total Product\n{ 0 }", "#607d8b")
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = self._create_content_lbl("Total Sales\n{ 0 }", "#ffc107")
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # ------------ footer -----------------
        lbl_footer = Label(
            self.root,
            text="IMS-Inventory Management System",
            font=("times new roman", 12),
            bg="#4d636d",
            fg="white",
        ).pack(side=BOTTOM, fill=X)

        self.update_content()

    # -------------- functions ----------------
    def _create_menu_btn(self, frame, text, command):
        newButton = Button(
            frame,
            text=text,
            command=command,
            image=self.icon_side,
            compound=LEFT,
            padx=5,
            anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white",
            bd=3,
            cursor="hand2",
        )
        newButton.pack(side=TOP, fill=X)
        return newButton

    def _create_content_lbl(self, text, bg):
        return Label(
            self.root,
            text=text,
            bd=5,
            relief=RIDGE,
            bg=bg,
            fg="white",
            font=("goudy old style", 20, "bold"),
        )

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CategoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SalesClass(self.new_win)

    def update_content(self):
        try:
            product = fetchall("select * from product")
            self.lbl_product.config(text=f"Total Product\n[ {len(product)} ]")

            category = fetchall("select * from category")
            self.lbl_category.config(text=f"Total Category\n[ {len(category)} ]")

            employee = fetchall("select * from employee")
            self.lbl_employee.config(text=f"Total Employee\n[ {len(employee)} ]")

            supplier = fetchall("select * from supplier")
            self.lbl_supplier.config(text=f"Total Supplier\n[ {len(supplier)} ]")

            bill = len(os.listdir(BILL_DIR))
            self.lbl_sales.config(text=f"Total Sales\n[ {bill} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )

            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
