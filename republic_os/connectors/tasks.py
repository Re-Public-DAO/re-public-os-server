from celery import shared_task
from datetime import datetime

from republic_os.connectors.models import OAuthState


@shared_task(bind=True)
def sync_connector_data(self,):

    print(f'[{datetime.now().isoformat()}] sync_connector_data')

    # Find all active connectors
    active_connectors = OAuthState.objects.filter(access_token__isnull=False)

    # For each connector
    for connector in active_connectors:

        # Get the API Url
        connector.sync_data()


@shared_task(bind=True)
def ingest_data_from_files(self, app):

    print('called ingest_data_from_files()')

    # Look in the raw data directory and input any new files from last run

    # For each file, find the database it belongs to and read in the new data
