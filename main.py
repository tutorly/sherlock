# Imports
import requests
import json
from lxml import html
import sys
from datetime import date
import os
import time
import smtplib
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import numpy as np

"""
This file will loop and check for new cases
"""
from session import Session

session = Session()
session.run()
