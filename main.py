# from flask import Flask, jsonify
# from bs4 import BeautifulSoup
# from pymongo import MongoClient
# import requests
# import time
# from datetime import datetime
#
# # Initialize Flask app
# app = Flask(__name__)
#
# # MongoDB connection
# MONGO_URI = "mongodb+srv://dinesh2003:7386531980@cluster0.gaw7dkr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(MONGO_URI)
# db = client["govt_tenders"]
# collection = db["eprocure_tenders"]
#
# # Keywords to filter
# FILTER_KEYWORDS = ['software', 'web development', 'web dev', 'AI', 'data entry', 'artificial intelligence']
#
#
# def scrape_tenders():
#     print(f"\n⏱️ Scraping started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     page = 1
#     max_pages = 5
#     new_tenders = 0
#
#     while page <= max_pages:
#         try:
#             cookies = {
#                 'cookieWorked': 'yes',
#                 'SSESS4e4a4d945e1f90e996acd5fb569779de': '6dJ1kcF3FqZAMvAHtXpX_Vyv8XAkAjzA60YFZ9TSQ5w',
#             }
#
#             headers = {
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#                 'Accept-Language': 'en-US,en;q=0.9',
#                 'Connection': 'keep-alive',
#                 'Referer': 'https://eprocure.gov.in/',
#                 'Sec-Fetch-Dest': 'document',
#                 'Sec-Fetch-Mode': 'navigate',
#                 'Sec-Fetch-Site': 'same-origin',
#                 'Sec-Fetch-User': '?1',
#                 'Upgrade-Insecure-Requests': '1',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#                 'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#                 'sec-ch-ua-mobile': '?0',
#                 'sec-ch-ua-platform': '"Windows"',
#                 # 'Cookie': 'cookieWorked=yes; SSESS4e4a4d945e1f90e996acd5fb569779de=6dJ1kcF3FqZAMvAHtXpX_Vyv8XAkAjzA60YFZ9TSQ5w',
#             }
#             params = {'page': str(page)}
#
#             response = requests.get(
#                 'https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata',
#                 params=params,
#                 cookies=cookies,
#                 headers=headers,
#                 timeout=30
#             )
#             response.raise_for_status()
#             soup = BeautifulSoup(response.content, 'html.parser')
#             listing = soup.find_all('tbody')
#
#             if not listing:
#                 break
#
#             for data in listing:
#                 try:
#                     title = data.find('a', {'title': 'External Url'}).text.strip()
#                 except:
#                     title = ''
#                 try:
#                     url = 'https://eprocure.gov.in' + data.find('a')['href']
#                 except:
#                     url = ''
#                 try:
#                     publish_date = data.find_all('td')[1].text.strip()
#                 except:
#                     publish_date = ''
#                 try:
#                     close_date = data.find_all('td')[2].text.strip()
#                 except:
#                     close_date = ''
#                 try:
#                     org_name = data.find_all('td')[5].text.strip()
#                 except:
#                     org_name = ''
#
#                 if collection.find_one({"url": url}):
#                     continue
#
#                 if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
#                     tender = {
#                         "title": title,
#                         "publish_date": publish_date,
#                         "close_date": close_date,
#                         "organisation": org_name,
#                         "url": url,
#                         "source": "eProcure",
#                         "timestamp": datetime.now()
#                     }
#                     print('--------------->',tender)
#                     collection.insert_one(tender)
#                     new_tenders += 1
#
#             page += 1
#             time.sleep(1)
#
#         except Exception as e:
#             print(f"❗ Error on page {page}: {e}")
#             break
#
#     print(f"✅ Scraping done. New tenders: {new_tenders}")
#     return new_tenders
#
#
# # Flask Routes
# @app.route('/')
# def home():
#     return "✅ Government Tender Scraper is Live!"
#
#
# @app.route('/tenders', methods=['GET'])
# def run_scraper():
#     try:
#         count = scrape_tenders()
#         return jsonify({"status": "success", "new_tenders_added": count})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500
#
#
# # Main entry
# if __name__ == '__main__':
#     import os
#
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port,debug=True)

# from flask import Flask, jsonify
# import requests
# from bs4 import BeautifulSoup
# from pymongo import MongoClient
# import datetime
#
# app = Flask(__name__)
#
# # MongoDB connection
# client = MongoClient("mongodb+srv://dinesh2003:7386531980@cluster0.gaw7dkr.mongodb.net/?retryWrites=true&w=majority")
# db = client["gov_tenders"]
# collection = db["eprocure_tenders"]
#
# # Helper to fix ObjectId issue
# def clean_mongo_ids(data):
#     for item in data:
#         item["_id"] = str(item["_id"])
#     return data
#
# # Scraper function
# def scrape_and_save_tenders():
#     all_data = []
#     page = 1
#
#     while True:
#         cookies = {
#             'cookieWorked': 'yes',
#             'SSESS4e4a4d945e1f90e996acd5fb569779de': '6dJ1kcF3FqZAMvAHtXpX_Vyv8XAkAjzA60YFZ9TSQ5w',
#         }
#
#         headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#             'Referer': 'https://eprocure.gov.in/',
#         }
#
#         params = {
#             'page': str(page),
#         }
#
#         response = requests.get(
#             'https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata',
#             params=params,
#             cookies=cookies,
#             headers=headers,
#         )
#
#         soup = BeautifulSoup(response.content, 'html.parser')
#         listing = soup.find_all('tbody')
#
#         if page == 5:
#             break
#
#         for data in listing:
#             try:
#                 publish_date = data.find_all('td')[1].text.strip()
#             except:
#                 publish_date = ''
#             try:
#                 close_date = data.find_all('td')[2].text.strip()
#             except:
#                 close_date = ''
#             try:
#                 opening_date = data.find_all('td')[3].text.strip()
#             except:
#                 opening_date = ''
#             try:
#                 tender_name = data.find('a', {'title': 'External Url'}).text.strip()
#             except:
#                 tender_name = ''
#             try:
#                 tender_url = data.find('a')['href']
#             except:
#                 tender_url = ''
#             try:
#                 org_name = data.find_all('td')[5].text.strip()
#             except:
#                 org_name = ''
#
#             record = {
#                 "tender_name": tender_name,
#                 "publish_date": publish_date,
#                 "closing_date": close_date,
#                 "opening_date": opening_date,
#                 "organisation": org_name,
#                 "url": tender_url,
#                 "scraped_at": datetime.datetime.now()
#             }
#
#             inserted = collection.insert_one(record)
#             record["_id"] = inserted.inserted_id
#             all_data.append(record)
#
#         page += 1
#
#     return jsonify(clean_mongo_ids(all_data))
#
# # Scrape and show data when hitting "/"
# @app.route("/", methods=["GET"])
# def home():
#     return scrape_and_save_tenders()
#
# # Optional status check
# @app.route("/status", methods=["GET"])
# def status():
#     return "✅ Tender API is Live with MongoDB. Go to `/` to scrape + store."
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import time  # Added missing import

# Initialize Flask app
app = Flask(__name__)

# Configure logging without emojis
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tender_scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Email configuration
EMAIL_SENDER = "gavinidineshkumar@gmail.com"
EMAIL_PASSWORD = "bmvg cggd yomw zmaf"  # App Password
EMAIL_RECEIVER = "gavinidineshkumar@gmail.com"


# Enhanced email function with debugging
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()

    # Try SSL first (port 465)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        logging.info("Email sent successfully via SSL!")
        return True
    except Exception as e:
        logging.error(f"SSL failed: {e}")

    # Try TLS as fallback (port 587)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        logging.info("Email sent successfully via TLS!")
        return True
    except Exception as e:
        logging.error(f"STARTTLS failed: {e}")
        return False


# MongoDB connection
client = MongoClient("mongodb+srv://dinesh2003:7386531980@cluster0.gaw7dkr.mongodb.net/?retryWrites=true&w=majority")
db = client["gov_tenders"]
collection = db["eprocure_tenders"]

# Keywords to filter tenders
FILTER_KEYWORDS = ['software', 'web development', 'web dev', 'AI', 'data entry', 'artificial intelligence']


# Helper to fix ObjectId issue
def clean_mongo_ids(data):
    for item in data:
        item["_id"] = str(item["_id"])
    return data


# Scraper function with email notifications
def scrape_and_save_tenders():
    all_data = []
    page = 1
    new_tenders = 0
    found_keyword_tenders = False

    # Test email before scraping
    logging.info("Testing email service...")
    if not send_email("TENDER SCRAPER STARTED", "Scraping process initiated successfully"):
        logging.error("Email test failed. Check credentials!")
    else:
        logging.info("Email test successful")

    while True:
        cookies = {
            'cookieWorked': 'yes',
            'SSESS4e4a4d945e1f90e996acd5fb569779de': '6dJ1kcF3FqZAMvAHtXpX_Vyv8XAkAjzA60YFZ9TSQ5w',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': 'https://eprocure.gov.in/',
        }

        params = {'page': str(page)}
        logging.info(f"Scraping page {page}...")

        try:
            response = requests.get(
                'https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata',
                params=params,
                cookies=cookies,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            # Save HTML for debugging
            with open(f"page_{page}.html", "w", encoding="utf-8") as f:
                f.write(response.text)

        except Exception as e:
            logging.error(f"Network error: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        listing = soup.find_all('tbody')

        if page == 5 or not listing:
            logging.info("Reached end of pages")
            break

        for data in listing:
            try:
                publish_date = data.find_all('td')[1].text.strip()
            except:
                publish_date = ''
            try:
                close_date = data.find_all('td')[2].text.strip()
            except:
                close_date = ''
            try:
                opening_date = data.find_all('td')[3].text.strip()
            except:
                opening_date = ''
            try:
                tender_name = data.find('a', {'title': 'External Url'}).text.strip()
            except:
                tender_name = ''
            try:
                tender_url = data.find('a')['href']
            except:
                tender_url = ''
            try:
                org_name = data.find_all('td')[5].text.strip()
            except:
                org_name = ''

            # Skip if tender exists
            if collection.find_one({"url": tender_url}):
                continue

            record = {
                "tender_name": tender_name,
                "publish_date": publish_date,
                "closing_date": close_date,
                "opening_date": opening_date,
                "organisation": org_name,
                "url": tender_url,
                "scraped_at": datetime.datetime.now()
            }

            # Check if tender matches keywords
            keyword_match = any(
                keyword.lower() in tender_name.lower()
                for keyword in FILTER_KEYWORDS
            ) if tender_name else False

            # Save to database
            inserted = collection.insert_one(record)
            record["_id"] = inserted.inserted_id
            all_data.append(record)
            new_tenders += 1

            # Send email for keyword matches
            if keyword_match:
                found_keyword_tenders = True
                subject = f"New Tender: {tender_name[:50]}"
                body = f"""New Government Tender Found:

Title: {tender_name}
Organisation: {org_name}
Publish Date: {publish_date}
Closing Date: {close_date}
URL: https://eprocure.gov.in{tender_url}
"""
                if not send_email(subject, body):
                    # Fallback: Save to file if email fails
                    with open("failed_emails.txt", "a") as f:
                        f.write(f"Subject: {subject}\n\n{body}\n\n")

        page += 1
        time.sleep(2)  # Respectful delay

    # Final report
    logging.info(f"Scraping complete. New tenders: {new_tenders}")
    if not found_keyword_tenders:
        send_email(
            "Tender Scraper Report",
            f"Scraped {new_tenders} new tenders but none matched your keywords."
        )

    return clean_mongo_ids(all_data)


# Scrape and show data when hitting "/"
@app.route("/", methods=["GET"])
def home():
    return jsonify(scrape_and_save_tenders())


# Optional status check
@app.route("/status", methods=["GET"])
def status():
    return "Tender API is Live with MongoDB. Go to `/` to scrape + store."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


