import random, string, time, os, subprocess, platform, sys  # Standard libraries
from datetime import datetime  # For timestamping reports
from selenium import webdriver  # For web browser automation
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.support.ui import WebDriverWait, Select  # For waiting and dropdowns
from selenium.webdriver.support import expected_conditions as EC  # For expected conditions in waits
from selenium.webdriver.chrome.service import Service  # For managing ChromeDriver service
from selenium.webdriver.chrome.options import Options  # For Chrome options
from webdriver_manager.chrome import ChromeDriverManager  # For automatic ChromeDriver management


# Function to generate a random string of lowercase letters
def generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Function to fill in a text input field and log the action
def fill_input_field(driver, log_info, by, value, input_text):
    field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
    field.send_keys(input_text)
    log_info.append(f"Filled field {value} with {input_text}.")
    time.sleep(0.5)  # Short delay

# Generate random email and username for registration
random_username = generate_random_string()
random_email = f"{random_username}@example.com"

# Initialize ChromeDriver with options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Initialize the ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Log information to be included in the report
log_info = []

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

    # Fill in the registration form fields
    for field_id, value in [
        ("AccountFrm_firstname", inputs["First Name"]),
        ("AccountFrm_lastname", inputs["Last Name"]),
        ("AccountFrm_email", inputs["Email"]),
        ("AccountFrm_telephone", inputs["Telephone"]),
        ("AccountFrm_fax", inputs["Fax"]),
        ("AccountFrm_company", inputs["Company"]),
        ("AccountFrm_address_1", inputs["Address 1"]),
        ("AccountFrm_address_2", inputs["Address 2"]),
        ("AccountFrm_city", inputs["City"]),
        ("AccountFrm_postcode", inputs["Postcode"]),
        ("AccountFrm_loginname", inputs["Username"]),
        ("AccountFrm_password", inputs["Password"]),
        ("AccountFrm_confirm", inputs["Password"]),
    ]:
        fill_input_field(driver, log_info, By.ID, field_id, value)

    # Select country and region/state
    Select(driver.find_element(By.ID, "AccountFrm_country_id")).select_by_visible_text(inputs["Country"])
    log_info.append(f"Selected country: {inputs['Country']}.")
    time.sleep(1)  # Short delay to ensure the region/state dropdown is populated

    Select(driver.find_element(By.ID, "AccountFrm_zone_id")).select_by_visible_text(inputs["Region/State"])
    log_info.append(f"Selected region/state: {inputs['Region/State']}.")
    time.sleep(0.5)  # Short delay

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
        time.sleep(3)  # 3-second delay before further verification

        # Click on the "ACCOUNT" button from the header bar
        log_info.append("Clicking on the 'ACCOUNT' button from the header bar.")
        account_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ACCOUNT"))
        )
        account_button.click()
        time.sleep(2)  # 2-second delay

        # Verify that the name displayed on the account page matches the first name
        log_info.append("Verifying the account name on the account page.")
        page_source = driver.page_source
        expected_name = inputs["First Name"]

        if expected_name in page_source:
            log_info.append(
                f"Account verification successful: The name '{expected_name}' is displayed on the account page.")
        else:
            log_info.append(
                f"Account verification failed: The name '{expected_name}' is not found on the account page.")
            result = "Failed"
        time.sleep(3)  # 3-second delay on the account page

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

except Exception as e:
    result = f"Failed with error: {e}"
    log_info.append(f"An error occurred: {e}")

finally:
    driver.quit()

# Generate test report with timestamp in filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# Create Logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), "Logs")
os.makedirs(logs_dir, exist_ok=True)
report_filename = f"test_report_{timestamp}.txt"
report_path = os.path.join(logs_dir, report_filename)
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

# Open the report
if platform.system() == 'Darwin':  # macOS
    subprocess.run(['open', report_path])
elif platform.system() == 'Windows':  # Windows
    os.startfile(report_path)
    sys.exit()  # Ensure the script exits after opening the report
elif platform.system() == 'Linux':  # Linux
    subprocess.run(['xdg-open', report_path])
else:
    print(f"Unsupported OS: {platform.system()}")
    sys.exit()
