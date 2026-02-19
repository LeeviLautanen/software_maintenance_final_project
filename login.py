from tkinter import *
from tkinter import messagebox
from database import fetchall


class LoginClass:
    def __init__(self, root):
        self.root = root
        self.root.title("IMS - Login")
        self.root.geometry("400x250+500+250")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        self.var_email = StringVar()
        self.var_pass = StringVar()

        # ------------ title --------------
        title = Label(
            self.root,
            text="Login",
            font=("goudy old style", 25, "bold"),
            bg="#0f4d7d",
            fg="white",
        ).pack(side=TOP, fill=X)

        # ------------ fields --------------
        lbl_email = Label(
            self.root, text="Email", font=("goudy old style", 15), bg="white"
        ).place(x=30, y=80)
        txt_email = Entry(
            self.root,
            textvariable=self.var_email,
            font=("goudy old style", 15),
            bg="lightyellow",
        ).place(x=120, y=80, width=240)

        lbl_password = Label(
            self.root, text="Password", font=("goudy old style", 15), bg="white"
        ).place(x=30, y=130)
        txt_password = Entry(
            self.root,
            textvariable=self.var_pass,
            font=("goudy old style", 15),
            bg="lightyellow",
            show="*",
        ).place(x=120, y=130, width=240)

        # ------------ button --------------
        btn_login = Button(
            self.root,
            text="Log In",
            command=self.login,
            font=("goudy old style", 15),
            bg="#2196f3",
            fg="white",
            cursor="hand2",
        ).place(x=120, y=190, width=240, height=35)

    def login(self):
        if self.var_email.get() == "" or self.var_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            rows = fetchall(
                "SELECT * FROM employee WHERE email=? AND pass=?",
                (self.var_email.get(), self.var_pass.get()),
            )
            if not rows:
                messagebox.showerror(
                    "Error", "Invalid email or password", parent=self.root
                )
            elif rows[0][8] != "Admin":
                messagebox.showerror(
                    "Error",
                    "Access denied. Admin privileges required.",
                    parent=self.root,
                )
            else:
                from dashboard import IMS  # Delayed import to avoid circular dependency

                self.root.destroy()
                dashboard_root = Tk()
                IMS(dashboard_root)
                dashboard_root.mainloop()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    LoginClass(root)
    root.mainloop()
