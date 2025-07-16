import requests
from bs4 import BeautifulSoup

URL = "https://spiker.gastreet.com/"
OUTPUT_FILE = "candidates_over_350.txt"

response = requests.get(URL)
response.encoding = 'utf-8'  # на случай кириллицы

soup = BeautifulSoup(response.text, 'lxml')

# Предположим, что каждый кандидат находится в каком-то теге, например, div с классом 'candidate'
# или в списке ul/li, нужно адаптировать под реальную структуру сайта.
# Для примера возьмём все элементы, где есть имя и количество голосов в формате "Имя (число голосов)"

candidates = []

# Ищем все теги, где есть текст с форматом "Имя (число голосов)"
for tag in soup.find_all(text=True):
    text = tag.strip()
    if text:
        # Проверяем, есть ли в тексте число голосов в скобках
        import re
        match = re.match(r"(.+?)\s*\((\d+)\s*голосов\)", text)
        if match:
            name = match.group(1).strip()
            votes = int(match.group(2))
            if votes > 350:
                candidates.append((name, votes))

# Сортируем по убыванию голосов
candidates.sort(key=lambda x: x[1], reverse=True)

# Записываем в файл
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for name, votes in candidates:
        f.write(f"{name} - {votes} голосов\n")

print(f"Список кандидатов с голосами > 350 сохранён в {OUTPUT_FILE}")
