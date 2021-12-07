from bs4 import BeautifulSoup
import requests
import mysql.connector

url = "https://www.newegg.com/p/pl?Submit=StoreIM&Category=34"

website = requests.get(url).text
website_body = BeautifulSoup(website, "html.parser")
# print(website_body.prettify())

processors = website_body.find_all("div", class_="item-cell")
# print(processors)
processor_data = []
for processor in processors:
    # extracting processor names
    processor_name = processor.find("img", title=True)["title"]

    # extracting processor link
    processor_link = processor.find("a", href=True)["href"]

    # extracting processor price
    processor_price = processor.find("li", class_="price-current")
    processor_price = processor_price.text.strip("\xa0")[1:8]
    processor_price = processor_price.replace(",", "")

    processor_data.append((processor_name, processor_link, processor_price))

# connecting to database
database = mysql.connector.connect(
     host="localhost",
     user="root",
     passwd="852702449a",
     database="Computer"
)

cursor = database.cursor()
# cursor.execute("CREATE DATABASE Computer") - creating database

# creating table
sql_table = """ CREATE TABLE Processors (Processor_ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Processor_Name
VARCHAR(200), Processor_Link VARCHAR(200), Processor_Price DECIMAL(6,2))"""
cursor.execute(sql_table)

# inserting information from web scraper into MySQL
sql_insert = """INSERT IGNORE INTO Processors(Processor_Name, Processor_Link, Processor_Price) VALUES (%s, %s, %s)"""
cursor.executemany(sql_insert, processor_data)

database.commit()
cursor.close()
database.close()

