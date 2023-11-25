from celery import shared_task
from datetime import datetime

from .models import ConnectorSync
from .utils import get_connector_action

from republic_os.oauth.models import OAuthState


@shared_task(bind=True)
def sync_connector_data(self, republic_id):

    print(f'sync_connector_data')
    print(self.request.id)

    oauth = OAuthState.objects.filter(
        connector__republic_id=republic_id
    ).first()

    if not oauth:
        return 'No OAuthState found'

    sync_tracker = ConnectorSync.objects.filter(
        connector__republic_id=republic_id,
        task_id=self.request.id
    ).first()

    if not sync_tracker:
        return 'No sync tracker found'

    sync_tracker.status = 'Fetching task from connector files'
    sync_tracker.save()

    task = get_connector_action(republic_id, 'sync')

    sync_tracker.status = 'Running task'
    sync_tracker.save()

    task(republic_id, self.request.id)

    sync_tracker.status = 'Done with task'
    sync_tracker.save()

    return 'Success'


@shared_task(bind=True)
def ingest_data_from_files(self, app):

    print('called ingest_data_from_files()')

    # Look in the raw data directory and input any new files from last run

    # For each file, find the database it belongs to and read in the new data
