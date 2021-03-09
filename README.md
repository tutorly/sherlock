# Sherlock
A webscraping python bot that pulls data from SPU's "covid cases" site and notifies students when there are updates.

**NOTICE:** Project Sherlock stopped running in December 2020 because SPU changed their website to a dynamic Tableau dashboard. Since our team has moved onto other projects, we will no longer support this. If you are interested in bringing Sherlock back to life (could probably get it working with Tesseract-OCR, for starters), please contact Soren at sorenrood@gmail.com.

### How do I start the bot?
run `python main.py`

### What credentials will I need?
To run the bot, you'll need our `creds.json` file as well as an environment variable that contains credentials to send emails.

### Program Files
main.py -> Runs the program.

bot.py -> Contains the `Bot` class that manages the program as it loops through the three stages (Scrape, Validate, Communicate).

    1. scraper.py -> scrapes the SPU webpage, handles server errors, formats data, and pushes result to sheets.
    
    2. validator.py -> pulls data from sheets, determines if the scraper has picked up a new case or not and returns the decision (boolean).
    
    3. courier.py -> pulls email list from sheets and sends each person an email notification of a new covid case at SPU.
