"""
This file will loop and check for new cases
"""
from scraper import Scraper
from session import Session
from courier import Courier

session = Session()

# Soren's testing
session.scraper.scrape()
newCase = session.validator.checkForNewCase()
print(f'New Case?: {newCase}')

