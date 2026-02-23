from database import execute, fetchall


class TestProductWithDependencies:
    """
    Check that basic product CRUD workflow works along with the category and supplier dependencies.
    """

    def add_category(self, name):
        execute("INSERT INTO category(name) VALUES(?)", (name,))

    def add_supplier(self, invoice, name, contact, desc):
        execute(
            "INSERT INTO supplier(invoice, name, contact, desc) VALUES(?,?,?,?)",
            (invoice, name, contact, desc),
        )

    def add_product(self, category, supplier, name, price, qty, status):
        execute(
            "INSERT INTO product(Category, Supplier, name, price, qty, status) "
            "VALUES(?,?,?,?,?,?)",
            (category, supplier, name, price, qty, status),
        )

    def test_product_category_and_supplier(self):
        # Add a new category and supplier
        self.add_category("Electronics")
        self.add_supplier(1, "Supplier 1", "950650353", "Electronic components")

        # Verify category and supplier got added successfully
        cats = fetchall("SELECT name FROM category")
        sups = fetchall("SELECT name FROM supplier")
        assert ("Electronics",) in cats
        assert ("Supplier 1",) in sups

        # Add a product in the new category and from the new supplier
        self.add_product(
            "Electronics", "Supplier 1", "Resistor Pack", "9.99", "500", "Active"
        )

        # Check product data
        products = fetchall("SELECT * FROM product")
        assert len(products) == 1
        p = products[0]
        assert p[1] == "Electronics"
        assert p[2] == "Supplier 1"
        assert p[3] == "Resistor Pack"
        assert p[4] == "9.99"
        assert p[5] == "500"
        assert p[6] == "Active"

        # Add a second product under the same category
        self.add_supplier(2, "Supplier 2", "651445615", "Bulk parts")
        self.add_product(
            "Electronics", "Supplier 2", "Capacitor Kit", "14.50", "300", "Active"
        )
        products = fetchall("SELECT * FROM product")
        assert len(products) == 2

        # Search for products by category
        found = fetchall("SELECT * FROM product WHERE Category=?", ("Electronics",))
        assert len(found) == 2
        assert found[0][3] == "Resistor Pack"
        assert found[1][3] == "Capacitor Kit"

        # Update a product's price and quantity
        pid = products[0][0]
        execute(
            "UPDATE product SET price=?, qty=? WHERE pid=?",
            ("12.99", "450", pid),
        )
        updated = fetchall("SELECT * FROM product WHERE pid=?", (pid,))
        assert updated[0][4] == "12.99"
        assert updated[0][5] == "450"

        # Delete a product
        execute("DELETE FROM product WHERE pid=?", (pid,))
        remaining = fetchall("SELECT * FROM product")
        assert len(remaining) == 1
        assert remaining[0][3] == "Capacitor Kit"
