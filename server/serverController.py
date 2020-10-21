import schedule
import time

from client import chatController
from server.webScrapingController import run_web_scraping

schedule.every().day.at("02:00").do(run_web_scraping)
schedule.every().seconds.do(chatController.run_telegram_chat)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__=="__main__":
    main()