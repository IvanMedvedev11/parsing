import pandas as pd
import requests
import bs4
req = requests.get("https://books.toscrape.com/")
src = req.text
soup = bs4.BeautifulSoup(src, "html.parser")
titles = soup.findAll('h3')
prices = soup.findAll('p', class_='price_color')
data = []
for title, price in zip(titles, prices):
    data.append([title.text.strip(), price.text.strip()])
df = pd.DataFrame(data, columns=['Название', 'Цена'])

    # Сохраняем в Excel
df.to_excel('file.xlsx', index=False)
print("Данные успешно записаны в file.xlsx")
