from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

# Настройки Selenium
options = Options()
options.add_argument("--headless")  # без окна браузера

# Укажите полный путь к chromedriver.exe (для Windows) или chromedriver (для Linux/Mac)
chromedriver_path = r"C:\Users\kmita\pra\chrome-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

url = "https://spiker.gastreet.com/"
driver.get(url)

# Ждём, пока появятся элементы с классом candidate-info
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "candidate-info"))
    )
except Exception as e:
    print("Элементы не найдены:", e)

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")

candidates = []

for div in soup.find_all("div", class_="candidate-info"):
    name_tag = div.find("span", class_="candidate-name")
    votes_tag = div.find("span", class_="votes")

    if name_tag and votes_tag:
        name = name_tag.text.strip()

        # Извлекаем число голосов из строки вида "(400 голосов)"
        votes_text = votes_tag.text.strip()
        match = re.search(r"\((\d+)\s*голосов\)", votes_text)
        if match:
            votes = int(match.group(1))
        else:
            votes = 0

        if votes > 350:
            candidates.append((name, votes))

# Сортируем по убыванию голосов
candidates.sort(key=lambda x: x[1], reverse=True)

for name, votes in candidates:
    print(f"{name} - {votes} голосов")

# Записываем в файл
with open("candidates_over_350.txt", "w", encoding="utf-8") as f:
    for name, votes in candidates:
        f.write(f"{name} - {votes} голосов\n")

#debug


# Записываем в файл для проверки
with open("page_source.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML-разметка страницы сохранена в файл page_source.html")
#print(html[:2000000])