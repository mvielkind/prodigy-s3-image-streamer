import boto3
import prodigy
import json
from prodigy.util import img_to_b64_uri


@prodigy.recipe("stream-from-s3")
def stream_from_s3(bucket, prefix=None):
    # Get all loaded images.
    s3 = boto3.client('s3')

    # Build a paginator for when there are a lot of objects.
    paginator = s3.get_paginator('list_objects')
    paginate_params = {
        'Bucket': bucket
    }

    # Check if only certain images from S3 should be loaded.
    if prefix is not None:
        paginate_params['Prefix'] = prefix

    page_iterator = paginator.paginate(**paginate_params)

    # Iterate through the pages.
    for page in page_iterator:
        # Iterate through items on the page.
        for obj in page['Contents']:
            img_key = obj['Key']

            # Read the image.
            img = s3.get_object(Bucket=bucket, Key=img_key).get('Body').read()

            # Provide response that Prodigy expects.
            print(json.dumps({'image': img_to_b64_uri(img, 'image/jpg')}))

