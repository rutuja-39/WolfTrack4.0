import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import HtmlTestRunner

class LoginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the Firefox WebDriver
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        # Navigate to the login page before each test
        self.driver.get("http://127.0.0.1:5000/login")  # Replace with the actual login page URL

    def test_login_with_valid_credentials_admin(self):
        """Test case for logging in with valid admin credentials."""
        driver = self.driver

        # Fill in Username
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("abcdefgh")  # Replace with a valid admin username in your database

        # Fill in Password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("abcdefgh")  # Replace with a valid password in your database

        # Select User Role from dropdown
        user_role_dropdown = Select(driver.find_element(By.NAME, "usertype"))
        user_role_dropdown.select_by_visible_text("Admin")

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

        # Wait for the page to load
        time.sleep(3)

        # Check for server errors
        self._check_for_errors()

        # Verify if redirected to the admin dashboard page URL
        expected_url = "http://127.0.0.1:5000/admin?data=abcdefgh"  # Replace with the actual admin dashboard URL
        current_url = driver.current_url
        self.assertEqual(current_url, expected_url, "Login was successful and redirected to admin dashboard page.")

    def test_login_with_valid_credentials_student(self):
        """Test case for logging in with valid student credentials."""
        driver = self.driver

        # Fill in Username
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("12345678")  # Replace with a valid student username in your database

        # Fill in Password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("12345678")  # Replace with a valid password in your database

        # Select User Role from dropdown
        user_role_dropdown = Select(driver.find_element(By.NAME, "usertype"))
        user_role_dropdown.select_by_visible_text("Student")

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

        # Wait for the page to load
        time.sleep(3)

        # Check for server errors
        self._check_for_errors()

        # Verify if redirected to the student dashboard page URL
        expected_url = "http://127.0.0.1:5000/student?data=12345678"  # Replace with the actual student dashboard URL
        current_url = driver.current_url
        self.assertEqual(current_url, expected_url, "Login was successful and redirected to student dashboard page.")

    def test_login_with_invalid_credentials(self):
        """Test case for logging in with invalid credentials."""
        driver = self.driver

        # Fill in Username
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys("invalid_user")

        # Fill in Password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("WrongPassword!")

        # Select User Role from dropdown
        user_role_dropdown = Select(driver.find_element(By.NAME, "usertype"))
        user_role_dropdown.select_by_visible_text("Admin")

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

        # Wait for the page to load
        time.sleep(3)

        # Check for server errors
        self._check_for_errors()

        # Verify if still on the login page
        current_url = driver.current_url
        self.assertEqual(current_url, "http://127.0.0.1:5000/login", "Page did not forward after invalid login attempt.")

        # Verify if an error message is displayed
        error_message = driver.find_element(By.CLASS_NAME, "alert-danger")
        self.assertTrue(error_message.is_displayed(), "Error message is not displayed for invalid login.")

    def test_login_with_blank_fields(self):
        """Test case for logging in with blank fields."""
        driver = self.driver

        # Leave fields blank and submit
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")

        username_field.clear()
        password_field.clear()

        # Select User Role from dropdown
        user_role_dropdown = Select(driver.find_element(By.NAME, "usertype"))
        user_role_dropdown.select_by_visible_text("Admin")

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

        # Wait for the page to load
        time.sleep(3)

        # Check for server errors
        self._check_for_errors()

        # Verify if still on the login page
        current_url = driver.current_url
        self.assertEqual(current_url, "http://127.0.0.1:5000/login", "Page did not forward after submitting blank fields.")

    def _check_for_errors(self):
        # Check for a generic internal server error message in <h1>
        h1_elements = self.driver.find_elements(By.TAG_NAME, "h1")
        h1_texts = [h1.text for h1 in h1_elements]
        # Check if any <h1> contains the term "error"
        internal_error_found = any("error" in h1.lower() for h1 in h1_texts)
        # Assert that an internal server error message was not found
        self.assertFalse(internal_error_found, "Internal server error detected in the response.")

    @classmethod
    def tearDownClass(cls):
        # Quit the driver after all tests are done
        cls.driver.quit()

# Run the tests
if __name__ == "__main__":
    output_file = "login_test_report.html"
    runner = HtmlTestRunner.HTMLTestRunner(
        output='.',  # Specify the output directory
        report_name='login_test_report',  # Set the report name (without extension)
        report_title='Login Test Report',  # Title for the report
        descriptions='Unit test results'  # Description for the report
    )
    runner.run(unittest.TestLoader().loadTestsFromTestCase(LoginTestCase))
