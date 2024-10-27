import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import uuid
import HtmlTestRunner

class SignupTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the Firefox WebDriver
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        # Navigate to the signup page before each test
        self.driver.get("http://127.0.0.1:5000/signup")  # Replace with the actual signup page URL

    def test_signup_with_unique_username(self):
        """Test case for signing up with valid data including a randomly generated unique username."""
        driver = self.driver

        # Generate a random unique username
        unique_username = f"user_{uuid.uuid4().hex[:8]}"  # Generate a username like "user_a1b2c3d4"

        # Fill in Name
        name_field = driver.find_element(By.NAME, "name")
        name_field.send_keys("Test User")

        # Fill in Username with the unique username
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(unique_username)

        # Fill in Password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("Password123!")

        # Select User Type from dropdown
        user_type_dropdown = Select(driver.find_element(By.NAME, "usertype"))
        user_type_dropdown.select_by_visible_text("Admin")  # Replace with actual option

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

        # Wait for the page to load
        time.sleep(3)

        # Verify if redirected to the login page URL
        expected_url = "http://127.0.0.1:5000/login"
        current_url = driver.current_url
        self.assertEqual(current_url, expected_url, "Signup was successful and redirected to login page.")

    def test_signup_with_duplicate_username(self):
        """Test case for signing up with a duplicate username."""
        driver = self.driver

        # Use the same username as created in the previous test
        duplicate_username = f"user_{uuid.uuid4().hex[:8]}"  # Generate a username like "user_a1b2c3d4"

        # First signup with a unique username
        self._sign_up_user("Test User", duplicate_username, "Password123!", "Admin")

        # Now try to sign up again with the same username
        self.driver.get("http://127.0.0.1:5000/signup")  # Navigate to signup page
        self._sign_up_user("Another User", duplicate_username, "AnotherPassword!", "Admin")

        # Wait for the page to load
        time.sleep(3)

        # Verify if still on the signup page
        current_url = driver.current_url
        self.assertEqual(current_url, "http://127.0.0.1:5000/signup", "Page did not forward after duplicate username attempt.")

    def test_signup_with_short_password(self):
        """Test case for signing up with a password shorter than 8 characters."""
        driver = self.driver

        # Fill in fields with a short password
        self._sign_up_user("Test User", f"user_{uuid.uuid4().hex[:8]}", "short", "Admin")

        # Wait for the page to load
        time.sleep(3)

        # Verify if still on the signup page
        current_url = driver.current_url
        self.assertEqual(current_url, "http://127.0.0.1:5000/signup", "Page did not forward after short password attempt.")

    def test_signup_with_blank_fields(self):
        """Test case for signing up with blank fields."""
        driver = self.driver

        # Leave all fields blank and submit
        name_field = driver.find_element(By.NAME, "name")
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        user_type_dropdown = Select(driver.find_element(By.NAME, "usertype"))

        name_field.clear()
        username_field.clear()
        password_field.clear()
        user_type_dropdown.select_by_visible_text("")  # Assuming there is a blank option or handle error accordingly

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

        # Wait for the page to load
        time.sleep(3)

        # Verify if still on the signup page
        current_url = driver.current_url
        self.assertEqual(current_url, "http://127.0.0.1:5000/signup", "Page did not forward after submitting blank fields.")

    def _sign_up_user(self, name, username, password, user_type):
        """Helper method to fill in the signup form and submit."""
        driver = self.driver

        # Fill in Name
        name_field = driver.find_element(By.NAME, "name")
        name_field.send_keys(name)

        # Fill in Username
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)

        # Fill in Password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        # Select User Type from dropdown
        user_type_dropdown = Select(driver.find_element(By.NAME, "usertype"))
        user_type_dropdown.select_by_visible_text(user_type)

        # Submit the form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

    @classmethod
    def tearDownClass(cls):
        # Quit the driver after all tests are done
        cls.driver.quit()

# Run the tests
if __name__ == "__main__":
    output_file = "signup_test_report.html"
    runner = HtmlTestRunner.HTMLTestRunner(output=output_file)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(SignupTestCase))
