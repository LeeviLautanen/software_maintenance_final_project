from billing import BillClass
from tkinter import Tk


class TestBillGeneration:
    """
    Tests adding product to cart, adding customer information and generating the text bill.
    """

    def test_bill_generation(self):
        root = Tk()
        root.withdraw()  # Hide GUI during testing
        billing = BillClass(root)

        row = [1, "Electronics", "Supplier 1", "Resistor Pack", "9.99", "500", "Active"]
        billing.var_pid.set(row[0])
        billing.var_pname.set(row[3])
        billing.var_price.set(row[4])
        billing.lbl_in_stock.config(text=f"In Stock [{str(row[5])}]")
        billing.var_stock.set(row[5])
        billing.var_qty.set("1")

        # Add new product to cart
        billing.add_update_cart()

        # Add customer details
        billing.var_cname.set("Customer 1")
        billing.var_contact.set("253623634")

        # Generate the bill
        billing.bill_top()
        billing.bill_middle()
        billing.bill_bottom()

        expected_bill = f"""
		XYZ-Inventory
	 Phone No. 9899459288 , Delhi-110053
==============================================
 Customer Name: Customer 1
 Ph. no. : 253623634
 Bill No. {billing.invoice}			Date: 23/02/2026
==============================================
 Product Name			QTY	Price
==============================================

 Resistor Pack			1	Rs.9.99
==============================================
Bill Amount				Rs.9.99
Discount				Rs.0.49950000000000006
Net Pay				Rs.9.4905
==============================================
"""

        # Check that generated bill matches expected
        assert billing.txt_bill_area.get("1.0", "end").strip() == expected_bill.strip()

        # Clear the data and check that everything is reset
        billing.clear_all()
        assert billing.cart_list == []
        assert billing.txt_bill_area.get("1.0", "end").strip() == ""
        assert billing.var_cname.get() == ""
        assert billing.var_contact.get() == ""
