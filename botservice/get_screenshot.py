from selenium import webdriver
import time, os
from selenium.webdriver.chrome.options import Options
from datetime import datetime


firewall_host="34.148.193.64"
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
system_url=f"https://{firewall_host}/index.php"
rules_url=f"https://{firewall_host}/firewall_rules.php"
folder_path= "../screenshots"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)


chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

username="admin"
password="arm0rbl0x!"

def get_screenshot():
    driver.get(system_url)
    driver.find_element("id", "usernamefld").send_keys(username)
    driver.find_element("id", "passwordfld").send_keys(password)
    driver.find_element("name", "login").click()
    driver.get("rules_url")
    driver.save_screenshot(f"./screenshots/screenshot_{current_time}.png")
    driver.quit()



def get_latestscreenshots():
    directory = "./screenshots"
    files = os.listdir(directory)
    filtered_files = [file for file in files if file.startswith("screenshot_")]
    sorted_files = sorted(filtered_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    latest_files = [os.path.join(directory, file) for file in sorted_files[:2]]
    return latest_files
