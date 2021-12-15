from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

csv_file = open("business_finance_law_books.cvs", "w")
csv_writer = csv.writer(csv_file, dialect=csv.excel)
csv_writer.writerow(['book_isbn', 'book_name', 'book_desc', 'book_author', 'book_date', 'book_type', 'book_link', 'book_price', 'book_rrp', 'book_category', 'book_availability', 'delivery_type', 'delivery'])

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/95.0.4638.69 Safari/537.36"}

url = "https://wordery.com/business-finance-law?page=1"
website = requests.get(url, headers=header, timeout=10).text
website_body = BeautifulSoup(website, "html.parser")
pages = website_body.find("span", {"class": "js-pnav-max"}).text
pages = int(pages) + 1
book_info = []

def web_scraper(num_pages):
    url = f"https://wordery.com/business-finance-law?page={num_pages}"
    website = requests.get(url, headers=header).text
    website_body = BeautifulSoup(website, "html.parser")
    book_body = website_body.find_all("li", {"class": "o-book-list__book"})

    for books in book_body:
        book_isbn = books.find("a", {"c-book__media ga-view"})['href']
        book_isbn = filter(str.isdigit, book_isbn)
        book_isbn = "".join(book_isbn).rstrip()

        book_name = books.find("a", {"class": "c-book__title"}).text.rstrip().strip("\n")

        book_type = books.small.text
        book_type = book_type.rstrip().strip("()").strip("\n")

        book_link = "https://wordery.com" + books.a['href']
        book_page = requests.get(book_link, headers=header).text
        book_body = BeautifulSoup(book_page, "html.parser")

        try:
            book_category = book_body.find("p", {"class": "c-cat-list u-m0"})
            book_category = book_category.get_text(strip=True, separator=", ").rstrip().strip("\n")
        except Exception as e:
            book_category = None

        try:
          book_date = book_body.find("span", {"class": "u-d--ib"}).text.rstrip().strip("()").strip("\n")
        except Exception as e:
           book_data = None

        try:
            book_availability = book_body.find("p",{"class": "u-mb1/4 u-color--green-dark u-fs--md"}).text.rstrip().strip("\n")
        except Exception as e:
            book_availability = None
            if book_availability == None:
                try:
                    book_availability = book_body.find("p", {"class": "u-mb1/4 u-color--red-mid u-fs--md"}).text.rstrip().strip("\n")
                except Exception as e:
                    book_availability == None

        try:
            book_desc = books.find("p", {"class": "c-book__description"}).text.rstrip().strip("\n")
        except Exception as e:
            book_desc = None

        try:
            book_price = books.find("span", {"class": "c-book__price c-price"}).text[0:7].rstrip().strip("\n")
            book_price = book_price.strip("£")
        except Exception as e:
            book_price = None

        try:
            book_rrp = books.find("del", {"class": "c-price__rrp"}).text.rstrip().strip("£").strip("\n")
        except Exception as e:
            book_rrp = None

        try:
            book_author = books.find("span", {"class": "c-book__by"}).text.rstrip().strip("\n")
        except Exception as e:
            book_author = None

        try:
            delivery_type = books.find("span", {"class": "c-book__express"}).text.rstrip().strip("\n")
        except Exception as e:
            delivery_type = None

        try:
            delivery = book_body.find("span", {"class": "u-fs--xl u-color--red-mid u-t--heavy u-d--ib"}).text.strip("+").strip("\n")
        except Exception as e:
            delivery = None

        csv_writer.writerow([book_isbn, book_name, book_desc, book_author, book_date, book_type, book_link, book_price, book_rrp, book_category, book_availability, delivery_type, delivery])

for page_number in range(0, pages):
    web_scraper(page_number)

csv_file.close()

# converting .csv to an excel file (.xlsx)
df = pd.read_csv("business_finance_law_books.cvs", encoding='unicode_escape')
df.to_excel("business_finance_law_books.xlsx", index=None, header=True)
