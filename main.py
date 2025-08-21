import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import chromedriver_autoinstaller

# Install the appropriate chromedriver
chromedriver_autoinstaller.install()

# Read the Excel file with the batch of numbers
df = pd.read_excel('sample.xlsx')  # Ensure your file is named correctly
numbers = df['numbers'].drop_duplicates().tolist()  # Remove duplicates before processing

# Your message in parts to simulate paragraph breaks
message = [
    'Indulge in ultimate relaxation with our ',
    '** Waterfall Head Bath with 1 Hour Massage for just QAR 80 **',
    '**Benefits:**',
    '    •  Scalp Health',
    '    •  Stress Relief',
    '    • Hair Care',
    '    • Mental Wellness',
    'Valid until 15/01/2025.',
    'Book now at +974 5546 4490 and visit us at 2nd Floor, A Block, Mirqab Mall, Doha, Qatar.',
    'Don’t miss this rejuvenating experience! '
]

# Use a set to store processed numbers to avoid duplicates
processed_numbers = set()

# Start a new Chrome browser instance using Selenium
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get('https://web.whatsapp.com/')

# Give time for the user to scan the QR code
print("Please scan the QR code to log in to WhatsApp Web.")
time.sleep(60)

# Loop through the list of numbers and send messages
for number in numbers:
    formatted_number = str(number).strip()

    # Skip the number if it has already been processed
    if formatted_number in processed_numbers:
        print(f"Skipping duplicate number: {formatted_number}")
        continue

    try:
        # Open chat with unsaved contact
        url = f'https://web.whatsapp.com/send?phone={formatted_number}'
        driver.get(url)
        time.sleep(10)  # Wait for the page to load

        # Check if the "Chat not found" message appears
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Phone number shared via url is invalid")]'))
            )
            print(f"Invalid number or no WhatsApp account: {formatted_number}")
            continue
        except TimeoutException:
            pass  # No error means the chat opened successfully

        # Wait for the message input box to appear
        message_box.send_keys(Keys.CONTROL, 'v')
        time.sleep(10)
        try:
            message_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p'))
            )
        except TimeoutException:
            print(f"Unable to reselect message box for {formatted_number}, skipping.")
            continue

        # Type each paragraph and send the message
        for part in message:
            message_box.send_keys(part)  # Type the paragraph
            message_box.send_keys(Keys.SHIFT, Keys.RETURN)  # Shift+Enter for a new line
        message_box.send_keys(Keys.RETURN)  # Send the message
        time.sleep(8)

        print(f"Message sent to {formatted_number}")
        processed_numbers.add(formatted_number)

    except NoSuchElementException:
        print(f"Error finding chat for {formatted_number}, skipping.")
        continue

    # Wait for a short period to prevent too fast sending
    time.sleep(5)

# End the process
print("Process completed!")
driver.quit()
