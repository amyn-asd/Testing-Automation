import random
import string
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Function to generate a random string
def generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


# Generate random email and username
random_username = generate_random_string()
random_email = f"{random_username}@example.com"

# Initialize ChromeDriver with options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Path to ChromeDriver executable
service = Service('C:/Users/amina/Documents/ChromeDriver/chromedriver.exe')

# Initialize the ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Log information to be included in the report
log_info = []

try:
    # Navigate to the main page
    log_info.append("Navigating to the main page.")
    driver.get("https://automationteststore.com/")
    time.sleep(2)  # 2-second delay

    # Click on the "Login or register" link
    log_info.append("Clicking on 'Login or register' link.")
    login_register_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Login or register"))
    )
    login_register_link.click()
    time.sleep(2)  # 2-second delay

    # Click on the "Continue" button in the "I AM A NEW CUSTOMER" section
    log_info.append("Clicking on 'Continue' button in the 'I AM A NEW CUSTOMER' section.")
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Continue']"))
    )
    continue_button.click()
    time.sleep(2)  # 2-second delay

    # Dictionary containing the input data for the registration form
    inputs = {
        "First Name": "Ole",
        "Last Name": "Nordmann",
        "Email": random_email,
        "Telephone": "123456789",
        "Fax": "123456789",
        "Company": "ExampleCompany",
        "Address 1": "123 Example Street",
        "Address 2": "Suite 100",
        "City": "Oslo",
        "Postcode": "0010",
        "Country": "Norway",
        "Region/State": "Oslo",
        "Username": random_username,
        "Password": "password123"
    }


    # Function to fill in a text input field
    def fill_input_field(by, value, input_text):
        field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        field.send_keys(input_text)
        log_info.append(f"Filled field {value} with {input_text}.")
        time.sleep(0.5)  # Short delay


    # Fill in the registration form fields
    fill_input_field(By.ID, "AccountFrm_firstname", inputs["First Name"])
    fill_input_field(By.ID, "AccountFrm_lastname", inputs["Last Name"])
    fill_input_field(By.ID, "AccountFrm_email", inputs["Email"])
    fill_input_field(By.ID, "AccountFrm_telephone", inputs["Telephone"])
    fill_input_field(By.ID, "AccountFrm_fax", inputs["Fax"])
    fill_input_field(By.ID, "AccountFrm_company", inputs["Company"])
    fill_input_field(By.ID, "AccountFrm_address_1", inputs["Address 1"])
    fill_input_field(By.ID, "AccountFrm_address_2", inputs["Address 2"])
    fill_input_field(By.ID, "AccountFrm_city", inputs["City"])
    fill_input_field(By.ID, "AccountFrm_postcode", inputs["Postcode"])

    # Select country and region/state
    country = Select(driver.find_element(By.ID, "AccountFrm_country_id"))
    country.select_by_visible_text(inputs["Country"])
    log_info.append(f"Selected country: {inputs['Country']}.")
    time.sleep(1)  # Short delay to ensure the region/state dropdown is populated

    region_state = Select(driver.find_element(By.ID, "AccountFrm_zone_id"))
    region_state.select_by_visible_text(inputs["Region/State"])
    log_info.append(f"Selected region/state: {inputs['Region/State']}.")
    time.sleep(0.5)  # Short delay

    # Fill in the login details and password
    fill_input_field(By.ID, "AccountFrm_loginname", inputs["Username"])
    fill_input_field(By.ID, "AccountFrm_password", inputs["Password"])
    fill_input_field(By.ID, "AccountFrm_confirm", inputs["Password"])

    # Subscribe to newsletter and agree to privacy policy
    driver.find_element(By.ID, "AccountFrm_newsletter1").click()
    log_info.append("Selected 'Subscribe to Newsletter'.")
    time.sleep(0.5)  # Short delay

    # Scroll down before agreeing to the privacy policy
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # Short delay after scrolling

    # Agreeing to terms
    driver.find_element(By.ID, "AccountFrm_agree").click()
    log_info.append("Agreed to the privacy policy.")
    time.sleep(0.5)  # Short delay

    # Submit the registration form
    driver.find_element(By.XPATH, "//button[@title='Continue']").click()
    log_info.append("Submitted the registration form.")

    # Check success based on URL
    WebDriverWait(driver, 10).until(EC.url_to_be("https://automationteststore.com/index.php?rt=account/success"))
    current_url = driver.current_url
    if current_url == "https://automationteststore.com/index.php?rt=account/success":
        result = "Passed"
        log_info.append("Test Passed: Redirected to the success URL.")
    else:
        result = "Failed"
        log_info.append(f"Test Failed: Did not redirect to the success URL, current URL is {current_url}.")

        # Capture any error messages displayed on the page
        try:
            error_messages = driver.find_elements(By.CSS_SELECTOR, "div.alert.alert-danger")
            for error in error_messages:
                log_info.append(f"Error message: {error.text.strip()}")
        except Exception as e:
            log_info.append(f"Failed to capture error messages: {e}")

    # 3-second delay before closing the browser
    time.sleep(3)

except Exception as e:
    result = f"Failed with error: {e}"
    log_info.append(f"An error occurred: {e}")

finally:
    # Ensure the browser is closed even if an error occurs
    driver.quit()

# Generate test report with timestamp in filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_filename = f"test_report_{timestamp}.txt"
report_path = os.path.join(os.path.dirname(__file__), report_filename)
with open(report_path, "w") as report:
    report.write("Test Report\n")
    report.write("===========\n")
    for key, value in inputs.items():
        report.write(f"{key}: {value}\n")
    report.write("\nLog Information:\n")
    report.write("===============\n")
    for log in log_info:
        report.write(f"{log}\n")
    report.write(f"\nResult: {result}\n")

# Print the result to the console
print(f"Test Result: {result}")
print(f"A detailed report has been generated in '{report_path}'")

# Open the report file automatically
os.startfile(report_path)
