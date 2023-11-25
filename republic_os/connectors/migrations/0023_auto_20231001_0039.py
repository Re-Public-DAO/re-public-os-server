import glob
import os
import shutil

from django.db import migrations
from django.conf import settings


def add_connector_records(apps, schema_editor):
    # Get the model from the versioned app registry to ensure the
    # migration happens against the correct version of the model.
    Connector = apps.get_model('connectors', 'Connector')

    # Define a list of connectors to add. Replace these example records
    # with your actual data.
    connectors_to_add = [
        {
            'name': 'Email',
            'republic_id': 'io.re-public.connector.email',
            'is_installed': True,
            'svg': 'connectors/email.svg',
            'description': 'Email connector'
        },
        {
            'name': 'Google',
            'republic_id': 'io.re-public.connector.google',
            'is_installed': True,
            'svg': 'connectors/google.svg',
            'description': 'Google connector'
        },
        {
            'name': 'Banking',
            'republic_id': 'io.re-public.connector.banking',
            'is_installed': True,
            'svg': 'connectors/money.svg',
            'description': 'Banking connector'
        },
        {
            'name': 'Spotify',
            'republic_id': 'io.re-public.connector.spotify',
            'is_installed': True,
            'svg': 'connectors/spotify.svg',
            'description': 'Spotify connector'
        },
        {
            'name': 'Twitter',
            'republic_id': 'io.re-public.connector.twitter',
            'is_installed': True,
            'svg': 'connectors/twitter.svg',
            'description': 'Twitter connector'
        },
        {
            'name': 'Facebook',
            'republic_id': 'io.re-public.connector.facebook',
            'is_installed': True,
            'svg': 'connectors/facebook.svg',
            'description': 'Facebook connector'
        },
        {
            'name': 'Amazon',
            'republic_id': 'io.re-public.connector.amazon',
            'is_installed': True,
            'svg': 'connectors/amazon.svg',
            'description': 'Amazon connector'
        },
        {
            'name': 'Fitbit',
            'republic_id': 'io.re-public.connector.fitbit',
            'is_installed': True,
            'svg': 'connectors/fitbit.svg',
            'description': 'Fitbit connector'
        },
        {
            'name': 'iCloud',
            'republic_id': 'io.re-public.connector.icloud',
            'is_installed': True,
            'svg': 'connectors/icloud.svg',
            'description': 'iCloud connector'
        },
        {
            'name': 'Strava',
            'republic_id': 'io.re-public.connector.strava',
            'is_installed': True,
            'svg': 'connectors/strava.svg',
            'description': 'Strava connector'
        },
        {
            'name': 'Ethereum',
            'republic_id': 'io.re-public.connector.ethereum',
            'is_installed': True,
            'svg': 'connectors/ethereum.svg',
            'description': 'Ethereum connector'
        }
    ]

    for connector_data in connectors_to_add:
        # Check whether the connector already exists
        if not Connector.objects.filter(republic_id=connector_data['republic_id']).exists():
            # Add the connector if it does not exist
            Connector.objects.create(**connector_data)

    #Copy image files from static folder to media folder
    static_image_dir = os.path.join(settings.BASE_DIR, 'myapp/static/myapp/connectors/')

    for static_image_path in glob.glob(os.path.join(static_image_dir, '*.svg')):
        # Extract image name from the path.
        img_name = os.path.basename(static_image_path)

        # Define where the image should be copied in the media directory.
        media_image_path = os.path.join(settings.MEDIA_ROOT, 'connectors/', img_name)

        # Ensure the media directory exists.
        os.makedirs(os.path.dirname(media_image_path), exist_ok=True)

        # Copy the image file to the media directory.
        shutil.copy2(static_image_path, media_image_path)


class Migration(migrations.Migration):

    dependencies = [
        ('connectors', '0022_remove_oauthstate_connector_id_connector_description_and_more'),
    ]

    operations = [
        migrations.RunPython(add_connector_records),
    ]
