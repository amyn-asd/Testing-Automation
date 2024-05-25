# Selenium Automated Registration Test

This repository contains a Selenium script (`PySelTest-extended.py`) that automates the process of registering a new user on the [Automation Test Store](https://automationteststore.com/). The script navigates to the website, fills out the registration form with randomized user details, submits the form, and verifies the successful creation of the account.

## Requirements

- Python 3.x
- Google Chrome browser
- ChromeDriver

## Setup

### Install Dependencies

First, ensure you have all the required Python packages. You can install them using `pip`:

\`\`\`sh
pip install -r requirements.txt
\`\`\`

### Requirements File

Here is the content of the `requirements.txt`:

\`\`\`txt
selenium
webdriver-manager
\`\`\`

### ChromeDriver

The script uses `webdriver-manager` to automatically manage the ChromeDriver binary. No additional setup is required for ChromeDriver.

## Usage

1. Clone this repository:

\`\`\`sh
git clone https://github.com/yourusername/selenium-automated-registration.git
cd selenium-automated-registration
\`\`\`

2. Run the script:

\`\`\`sh
python PySelTest-extended.py
\`\`\`

## Script Overview

### PySelTest-extended.py

This script performs the following steps:

1. Generates a random username and email for the new user.
2. Initializes the Chrome WebDriver with specific options.
3. Navigates to the [Automation Test Store](https://automationteststore.com/).
4. Clicks on the "Login or register" link.
5. Clicks on the "Continue" button in the "I AM A NEW CUSTOMER" section.
6. Fills out the registration form with the following details:
    - First Name
    - Last Name
    - Email
    - Telephone
    - Fax
    - Company
    - Address 1
    - Address 2
    - City
    - Postcode
    - Country
    - Region/State
    - Username
    - Password
7. Subscribes to the newsletter and agrees to the privacy policy.
8. Submits the registration form.
9. Verifies successful registration by checking the URL.
10. Clicks on the "ACCOUNT" button from the header bar.
11. Verifies that the account name matches the first name used during registration.
12. Generates a detailed report of the test, including the result and any errors encountered, and saves it in the `Logs` directory.

### Log Files

Log files are saved in the `Logs` directory with a timestamped filename (e.g., `test_report_20230401_123456.txt`). Each log file contains detailed information about the test execution, including the input data used, the steps performed, and the result of the test.

## Notes

- Ensure that the Chrome browser is installed and updated on your machine.
- The script is designed to be cross-platform, but it has been primarily tested on Windows. Adjustments may be needed for other operating systems.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests with any improvements or bug fixes.
"""
