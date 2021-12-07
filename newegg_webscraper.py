from bs4 import BeautifulSoup
import requests
import mysql.connector
import csv

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/95.0.4638.69 Safari/537.36"}

graphic_cards_data = []

# csv_file = open("graphics_card.cvs", "w")
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(["card_name", "card_link", "card_price", "card_review", "card_shipping_cost"])


def graphics_card(page_number):
    url = f"https://www.newegg.com/global/uk-en/Desktop-Graphics-Cards/SubCategory/ID-48/Page-0{page_number}?Tid=1582767"
    website = requests.get(url, headers=header).text
    website_body = BeautifulSoup(website, "html.parser")
    graphic_cards = website_body.find_all("div", {"class": "item-cell"})
    for cards in graphic_cards:
        card_name = cards.find("a", {"class": "item-title"}).text
        card_link = cards.find("a", href=True)["href"]
        card_price = cards.find("li", {"class": "price-current"}).text.strip("\xa0–")[1:9]
        card_price = card_price.replace(",", "")
        try:
            card_review = cards.find("div", {"class": "item-branding"}).i['aria-label']
        except Exception as e:
            card_review = "No Review"
        card_shipping_cost = cards.find("li", {"class": "price-ship"}).text

        graphic_cards_data.append((card_name, card_link, card_price, card_review, card_shipping_cost))

        # csv_writer.writerow([card_name, card_link, card_price, card_review, card_shipping_cost])


for page in range(0, 9):
    graphics_card(page)

# csv_file.close()

# SQL CODE
database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="852702449a",
    database="Computer"
)

cursor = database.cursor()
sql_table = """ CREATE TABLE Graphic_Cards (Card_ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Card_Name VARCHAR(
1000), Card_Link VARCHAR(1000), Card_Price DECIMAL(6,2), Card_Review VARCHAR(100), Shipping_Cost VARCHAR(100))"""
cursor.execute(sql_table)

insert_sql = """INSERT INTO Graphic_Cards(Card_Name, Card_Link, Card_Price, Card_Review, Shipping_Cost) VALUES (%s,%s,
%s,%s,%s) """

cursor.executemany(insert_sql, graphic_cards_data)

database.commit()
cursor.close()
database.close()