# Sherlock
A webscraping python bot that pulls data from SPU's "covid cases" site and notifies students when there are updates.

**NOTICE:** Project Sherlock stopped running in December 2020 due to SPU changing their website to a dynamic Tableau dashboard. However, our team is commited to notifying students. We will continue sending notifications until the administration decides to do it themselves. To sign up for notifications, visit this [link](https://tutorly.com/covid).

### How do I start the bot?
run `python main.py`.

### What credentials will I need?
If you want to run the bot, you'll need our `creds.json` file as well as an environment variable that contains credentials to send emails. Send an email to soren@tutorly.app if you are interested in getting these.

### Program Files
main.py -> Runs the program.

bot.py -> Contains the `Bot` class that manages the program as it loops through the three stages (Scrape, Validate, Communicate).

    1. scraper.py -> scrapes the SPU webpage, handles server errors, formats data, and pushes result to sheets.
    
    2. validator.py -> pulls data from sheets, determines if the scraper has picked up a new case or not and returns the decision (boolean).
    
    3. courier.py -> pulls email list from sheets and sends each person an email notification of a new covid case at SPU.
