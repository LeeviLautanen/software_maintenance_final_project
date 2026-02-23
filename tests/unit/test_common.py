from tkinter import Tk
from common import create_crud_buttons


class TestCommon:
    def test_create_crud_buttons(self):
        root = Tk()
        btn_add, btn_update, btn_delete, btn_clear = create_crud_buttons(
            root, lambda: None, lambda: None, lambda: None, lambda: None
        )
        assert btn_add.winfo_class()  # validates it's a widget
        assert btn_update.winfo_class()
        assert btn_delete.winfo_class()
        assert btn_clear.winfo_class()
        root.destroy()
