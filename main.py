import os
import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_url = "https://www.alphavantage.co/query?"

stock_api_key = os.environ.get("STOCK_API_KEY")

news_api_key = os.environ.get('NEWS_API_KEY')

auth_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

now = dt.datetime.now()
weekday = now.date().weekday()


def check_stock():
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": stock_api_key
    }

    response = requests.get(stock_url, stock_params)
    response.raise_for_status()
    data = response.json()
    time_series = data["Time Series (Daily)"]

    if weekday != 5 or weekday != 6:
        yesterday = time_series[str(now.date() - dt.timedelta(days=2))]
        day_before_yesterday = time_series[str(now.date() - dt.timedelta(days=3))]
        print(f"yesterday: {yesterday}")
        print(f"day before: {day_before_yesterday}")
        yesterday_closing_price = float(yesterday["4. close"])
        day_before_closing_price = float(day_before_yesterday["4. close"])
        # Check increase
        increase = yesterday_closing_price - day_before_closing_price
        fraction = increase / day_before_closing_price
        percentage_increase = fraction * 100

        decrease = day_before_closing_price - yesterday_closing_price
        fraction_decrease = decrease / yesterday_closing_price
        percentage_decrease = fraction_decrease * 100

        if True:

            new_url = f"http://newsapi.org/v2/everything?q={COMPANY_NAME}&from={str(now.date() - dt.timedelta(days=2))}&sortBy=popularity&apiKey={news_api_key}"

            news_response = requests.get(new_url)
            news_response.raise_for_status()
            news_data = news_response.json()
            articles = news_data["articles"]
            article1 = articles[0]
            article2 = articles[1]
            article3 = articles[2]

            client = Client(auth_sid, auth_token)

            message_string = f"""
                Tesla: {round(percentage_increase)} Increase \n
                Article 1: {article1["title"]} - {article1["url"]}\n
                Article 2: {article2["title"]} - {article2["url"]}\n
                Article 3: {article3["title"]} - {article3["url"]}\n
                """

            message = client.messages \
                .create(
                body=f"{message_string}",
                from_='+19494076520',
                to='+27727903376'
            )

            print(message.sid)


check_stock()

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
