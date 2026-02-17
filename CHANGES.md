# Inventory-Management-System changes

Changes done to the base project listed per module.

### Global changes

- The entire codebase was formatted by the Ruff formatter
- All variables have been formatted to be snake_case.
- Moved database handling to its own file database.py
- Created a library for shared functionality, like creating the CRUD buttons
- All classes names changed to PascalCase

### 1. dashboard.py

- Moved left menu button and content label creation into functions to reduce duplication

### 2. employee.py

- Changed to use shared CRUD button creation

### 3. supplier.py

- Changed to use shared CRUD button creation

### 4. product.py

- Changed to use shared CRUD button creation

### 5. category.py

- Changed "Add" button to PascalCase to match the rest of the buttons

### 6. sales.py

- No changes

### 7. create_db.py

- No changes

### 8. billing.py

- Removed duplicated code from keypad creation
- Cleaned up some commented out code and redundant comments
