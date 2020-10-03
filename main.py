"""
This file will loop and check for new cases
"""
from scraper import Scraper
from newSession import Session
from courier import Courier

session = Session()

# Soren's testing
session.scraper.scrape()
session.scraper.writeListsToGoogleSheet()
print(f'New Case?: {session.validator.checkForNewCase()}')

