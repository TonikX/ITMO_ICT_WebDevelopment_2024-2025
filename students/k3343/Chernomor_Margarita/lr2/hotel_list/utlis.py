import datetime
from dateutil import parser

def parse_or_return(dirty_date):
    if type(dirty_date) == datetime.date:
        return dirty_date
    return parser.parse(dirty_date)
