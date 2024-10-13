import time
import creds
import smtplib

from selenium import webdriver
from collections import Counter
from datetime import datetime as dt
from email.mime.text import MIMEText
from selenium.webdriver.common.by import By
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def login(driver):
    driver.get('https://app.dataannotation.tech/users/sign_in')
    usr = driver.find_element(By.ID, 'user_email')
    pwd = driver.find_element(By.ID, 'user_password')
    login_btn = driver.find_element(By.NAME, 'commit')
    usr.send_keys('mauriciojmj10@gmail.com')
    pwd.send_keys('AugyMarie@0203')
    login_btn.click()
    return

def get_available_jobs(driver):
    tables = driver.find_elements(By.XPATH, "//div[@class='active-table']")

    for table in tables:
        header_element = table.find_element(By.XPATH, ".//h3")
        header = header_element.text

        if header == 'Projects':
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            pay_values = []
            for row in rows:
                pay_cell = row.find_element(By.XPATH, ".//td[2]")
                pay_values.append(pay_cell.text)

            return pay_values

def send_email(pay_values, server, msg, driver):
    pay_values = [pay for pay in pay_values if pay != '']
    if len(pay_values) > 0:
        body = ''
        rate_counts = Counter(pay_values)
        for rate, count in rate_counts.items():
            if count == 1:
                body += f'There is {count} job that pays {rate}\n'
            elif count > 1:
                body += f'There are {count} jobs that pay {rate}\n'
    else:
        body = 'There are no jobs at the moment'

    msg.set_payload(None)
    msg.attach(MIMEText(body, 'plain'))
    server.send_message(msg)
    timestamp = dt.now().time().strftime('%H:%M')
    print(f'Email sent successfully at {timestamp}')

def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options .add_argument('--disable-gpu')
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    try:
        login(driver)
        while True:
            server = smtplib.SMTP('smtp.mail.me.com', 587)
            server.starttls()
            server.login(creds.sender, creds.pwd)

            msg = MIMEMultipart()
            msg['From'] = creds.sender
            msg['To'] = creds.receiver
            msg['Subject'] = 'Jobs available!!'
            driver.refresh()
            pay_values = get_available_jobs(driver)
            send_email(pay_values, server, msg, driver)
            time.sleep(60*60)
    finally:
        server.quit()
        driver.quit()

if __name__ == '__main__':
    main()