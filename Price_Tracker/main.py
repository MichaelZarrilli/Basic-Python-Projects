import requests
from bs4 import BeautifulSoup
from pony import orm
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


db = orm.Database()
db.bind(provider='sqlite', filename='products.db', create_db=True)
driver = webdriver.Chrome()

# Customize what price you would like to recieve notifications

PRICE_THRESHOLDS = {
    "BestBuy": 101.00,
    "NewEgg": 101.00,
    "BnH": 101.00
}

EMAIL_ADDRESS = "YOUR EMAIL HERE"
EMAIL_PASSWORD = "YOUR PASS HERE"
TO_EMAIL = "YOUR EMAIL HERE"


class Product(db.Entity):
    name = orm.Required(str)
    price = orm.Required(float)
    create_date = orm.Required(datetime)


db.generate_mapping(create_tables=True)


def bestbuy(session):
    url = "https://www.bestbuy.com/site/seagate-barracuda-8tb-internal-hard-drive-for-desktops/6616038.p?skuId=6616038"
    driver.get(url)
    time.sleep(5)
    dollars = driver.find_element(By.CSS_SELECTOR, "div.priceView-hero-price span.sr-only").text

    data = (
            "BestBuy",
            float(re.search(r"\d+\.\d+", dollars).group())
        )

    print(data)
    return data


def newegg(session):
    url = "https://www.newegg.com/seagate-barracuda-ne-st8000dm004-8tb-hard-drive-for-daily-computing-5400-rpm/p/N82E16822183793?Item=N82E16822183793&SoldByNewegg=1"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    price_container = soup.select_one("div.price-current")

    dollars = float(price_container.select_one("strong").text)
    cents = float(price_container.select_one("sup").text)

    data = (
        "NewEgg",
        dollars + cents
    )
    print(data)

    return data


def bnh(session):
    url = "https://www.bhphotovideo.com/c/product/1666827-REG/seagate_st8000dm004_8tb_barracuda_sata_iii.html"
    driver.get(url)
    time.sleep(5)
    price_text = driver.find_element(By.CSS_SELECTOR, "span[data-selenium='pricingPrice']").text

    price = float(re.search(r"\d+\.\d+", price_text).group())

    data = (
        "BnH",
        price
    )
    print(data)

    return data


def send_email(product_name, price):
    subject = f"Price Alert: {product_name}"
    body = f"The price for {product_name} is now ${price}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # noinspection PyBroadException
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print("Email sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


def check_price_and_notify(data):
    name, price = data
    if price < PRICE_THRESHOLDS[name]:
        send_email(name, price)


def main():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'YOUR USER AGENT HERE'
    })

    data = [
        bestbuy(session),
        newegg(session),
        bnh(session),
    ]
    with orm.db_session:
        for item in data:
            Product(name=item[0], price=item[1], create_date=datetime.now())
            check_price_and_notify(item)

    driver.quit()


if __name__ == '__main__':
    main()
