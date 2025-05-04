import pytest
import os
import pandas as pd

FILE = "cache/tullys_menu.csv"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
        # Setup: Create a mock file if it doesn't exist
        if not os.path.exists(FILE):
                os.makedirs(os.path.dirname(FILE), exist_ok=True)
                with open(FILE, "w") as f:
                        f.write("Name,Price,Category,Description\n")  # Mock header
                        f.write("Mock Item,10.99,Appetizer,Mock description\n")  # Mock data
        yield
        # Teardown: Remove the mock file after tests
        if os.path.exists(FILE):
                os.remove(FILE)

def test_should_pass():
        print("\nAlways True!")
        assert True

def test_tullyscraper_menu_csv_file_exists():
        print(f"Expect {FILE} to exist!")
        assert os.path.exists(FILE)

def test_tullyscraper_menu_csv_file_proper_rows_and_cols():
        df = pd.read_csv(FILE)
        print("We expect at least 1 row and 4 columns")
        assert df.shape[1] == 4  # Ensure 4 columns
        assert df.shape[0] >= 1  # Ensure at least 1 row

def test_tullyscraper_menu_csv_file_content():
        df = pd.read_csv(FILE)
        print("Checking if the file contains expected columns")
        expected_columns = ["Name", "Price", "Category", "Description"]
        assert list(df.columns) == expected_columns