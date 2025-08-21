# whatsapp_script.py

import pandas as pd
import time
import datetime
import random
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import chromedriver_autoinstaller


def start_whatsapp_automation(file_path, log_callback=lambda msg: print(msg)):
    try:
        # Setup
        chromedriver_autoinstaller.install()
        logging.basicConfig(filename='whatsapp_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        df = pd.read_excel(file_path)
        numbers = df['number'].drop_duplicates().astype(str).tolist()

        processed_file = 'processed_numbers.txt'
        if os.path.exists(processed_file):
            with open(processed_file, 'r') as f:
                processed_numbers = set(line.strip() for line in f)
        else:
            processed_numbers = set()

        # Message to send
        message = [
            'Time is Ticking -Act Now!',
            '',
            'Don\'t wait until the last moment to submit your 2024 tax returns.',
            '',
            'Take advantage of the 100% Financial Penalty Exemption Initiative announced by the General Tax Authority(GTA) by ensuring timely tax filings and clearing any outstanding dues',
            '',
            'Deadline: 31st August 2025',
            '',
            'For assistance and inquiries, please contact us at 31238818.',
            '',
            'With regards,',
            '',
            'Shakir Thalappil.',
            'AK and Partners - Auditors and Chartered Accountants',
        ]

        # Allowed time windows
        active_windows = [
            (datetime.time(7, 0), datetime.time(18, 0)),
            (datetime.time(19, 0), datetime.time(22, 0)),
        ]

        def is_within_active_window(current_time):
            return any(start <= current_time <= end for start, end in active_windows)

        # Start browser
        driver = webdriver.Chrome()
        driver.get('https://web.whatsapp.com/')
        log_callback("📷 Please scan the QR code to log in...")

        try:
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'app')))
            log_callback("✅ Logged in successfully!")
        except TimeoutException:
            log_callback("❌ Login timeout. Please scan the QR code faster next time.")
            driver.quit()
            return

        for number in numbers:
            formatted_number = number.strip()

            if formatted_number in processed_numbers:
                log_callback(f"⏭️ Skipping already processed number: {formatted_number}")
                continue

            while not is_within_active_window(datetime.datetime.now().time()):
                log_callback("⏰ Outside allowed sending hours. Waiting 5 minutes...")
                time.sleep(300)

            try:
                driver.get(f'https://web.whatsapp.com/send?phone={formatted_number}&text&type=phone_number')
                time.sleep(random.uniform(15, 25))

                # Optional "Continue to chat" button
                try:
                    continue_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "web.whatsapp.com/send")]'))
                    )
                    continue_btn.click()
                    time.sleep(5)
                except Exception:
                    pass

                # Invalid number check
                try:
                    driver.find_element(By.XPATH, '//span[contains(text(), "Phone number shared via url is invalid")]')
                    log_callback(f"❌ Invalid WhatsApp number: {formatted_number}")
                    logging.warning(f"{formatted_number} - Invalid number.")
                    continue
                except NoSuchElementException:
                    pass

                # Locate message box
                try:
                    message_box = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                    )
                except TimeoutException:
                    log_callback(f"⏳ Retrying chat load for {formatted_number}...")
                    time.sleep(10)
                    try:
                        message_box = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                        )
                    except TimeoutException:
                        log_callback(f"🚫 Message box not found for {formatted_number}. Skipping.")
                        logging.warning(f"{formatted_number} - Message box not found.")
                        continue

                # Send message
                for part in message:
                    message_box.send_keys(part)
                    message_box.send_keys(Keys.SHIFT, Keys.RETURN)
                    time.sleep(0.3)
                time.sleep(1.5)
                message_box.send_keys(Keys.RETURN)

                log_callback(f"✅ Message sent to {formatted_number}")
                logging.info(f"{formatted_number} - Message sent.")

                with open(processed_file, 'a') as f:
                    f.write(f"{formatted_number}\n")
                processed_numbers.add(formatted_number)

                time.sleep(random.uniform(15, 25))

            except Exception as e:
                log_callback(f"❌ Error sending to {formatted_number}: {str(e)}")
                logging.error(f"{formatted_number} - Error: {str(e)}")
                continue

        log_callback("🎉 All messages processed!")
        driver.quit()

    except Exception as ex:
        log_callback(f"💥 Unexpected error: {str(ex)}")
        logging.error(f"Unexpected error: {str(ex)}")
