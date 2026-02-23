from database import execute, fetchall


class TestDatabase:
    def test_insert_and_fetch(self):
        execute("INSERT INTO category(name) VALUES(?)", ("Electronics",))
        execute("INSERT INTO category(name) VALUES(?)", ("Clothing",))

        rows = fetchall("SELECT * FROM category")
        assert len(rows) == 2
        names = [r[1] for r in rows]
        assert "Electronics" in names
        assert "Clothing" in names

    def test_fetching_with_params(self):
        execute("INSERT INTO category(name) VALUES(?)", ("Food",))
        execute("INSERT INTO category(name) VALUES(?)", ("Toys",))

        rows = fetchall("SELECT * FROM category WHERE name=?", ("Food",))
        assert len(rows) == 1
        assert rows[0][1] == "Food"

    def test_fetching_empty_table(self):
        rows = fetchall("SELECT * FROM category")
        assert rows == []
