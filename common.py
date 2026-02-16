from tkinter import Button


def create_crud_buttons(
    frame, add_command, update_command, delete_command, clear_command
):
    btn_add = Button(
        frame,
        text="Save",
        command=add_command,
        font=("goudy old style", 15),
        bg="#2196f3",
        fg="white",
        cursor="hand2",
    )
    btn_update = Button(
        frame,
        text="Update",
        command=update_command,
        font=("goudy old style", 15),
        bg="#4caf50",
        fg="white",
        cursor="hand2",
    )
    btn_delete = Button(
        frame,
        text="Delete",
        command=delete_command,
        font=("goudy old style", 15),
        bg="#f44336",
        fg="white",
        cursor="hand2",
    )
    btn_clear = Button(
        frame,
        text="Clear",
        command=clear_command,
        font=("goudy old style", 15),
        bg="#607d8b",
        fg="white",
        cursor="hand2",
    )
    return btn_add, btn_update, btn_delete, btn_clear
