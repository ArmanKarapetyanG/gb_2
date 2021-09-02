from bs4 import BeautifulSoup
import pandas as pd
import requests
import lxml

def parse_page(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    books_title = [i['title'] for i in soup.select('div ol.row li h3 a')]
    books_url = ['https://books.toscrape.com/catalogue/' + i['href'] for i in soup.select('div ol.row li h3 a')]
    books_price = [i.text for i in soup.select('div ol.row li p.price_color')]
    data_to_return = []
    for num, i in enumerate(books_title):
        data_to_return.append({
            "title": i,
            "url": books_url[num],
            "price": books_price[num].replace('Â', '')
        })
    return data_to_return




all_books = []
for i in range(1, 6):
    url = 'https://books.toscrape.com/catalogue/page-{}.html'.format(i)
    books_temp = parse_page(url)
    if i == 5:
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'lxml')
        categories = [i.text.strip() for i in soup.select('ul.nav li ul li a')]
    all_books += books_temp


pd.DataFrame(all_books).to_csv('books.csv', index=False)
pd.DataFrame({'Categories': categories}).to_csv('categories.csv', index=False)




