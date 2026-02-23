from database import execute, fetchall


class TestLoginValidation:
    def create_admin(self):
        execute(
            "INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                "Admin User",
                "admin@email.com",
                "M",
                "111",
                "01-01-1990",
                "01-01-2020",
                "1234",
                "Admin",
                "HQ",
                "50000",
            ),
        )

    def create_employee(self):
        execute(
            "INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                "Staff User",
                "staff@email.com",
                "F",
                "222",
                "02-02-1995",
                "02-02-2021",
                "5678",
                "Employee",
                "Branch",
                "30000",
            ),
        )

    def test_valid_admin(self):
        self.create_admin()
        rows = fetchall(
            "SELECT * FROM employee WHERE email=? AND pass=?",
            ("admin@email.com", "1234"),
        )
        assert len(rows) == 1
        assert rows[0][8] == "Admin"

    def test_invalid_password(self):
        self.create_admin()
        rows = fetchall(
            "SELECT * FROM employee WHERE email=? AND pass=?",
            ("admin@email.com", "1111"),
        )
        assert rows == []

    def test_non_admin(self):
        self.create_employee()
        rows = fetchall(
            "SELECT * FROM employee WHERE email=? AND pass=?",
            ("staff@email.com", "5678"),
        )
        assert len(rows) == 1
        assert rows[0][8] != "Admin"
