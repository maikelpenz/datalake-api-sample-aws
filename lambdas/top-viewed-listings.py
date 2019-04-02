import athenahelper
import json
import os
import sys
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUERY_BUCKET = os.environ['QUERY_BUCKET']
DATABASE_NAME = os.environ["DATABASE_NAME"]

def lambda_handler(event, context):
    
    query = """
        SELECT listingid, listingtitle, count(*) as views
        FROM "top_viewed_listings"
        group by listingid, listingtitle
        order by count(*) desc
        limit 5
    """
    db = DATABASE_NAME
    output = QUERY_BUCKET

    try:
        query = athenahelper.AthenaHelper(query, db, output)
        result = query.get_results()

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        logger.warn(e)
        message = "Error: {}".format(str(e))
        raise Exception(message)