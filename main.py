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
session.validator.getLastScrapeFromGoogleSheets()
session.validator.countScrapedCases()
session.validator.updateCasesInGoogleSheets()
session.validator.readPreviousCasesCount()

