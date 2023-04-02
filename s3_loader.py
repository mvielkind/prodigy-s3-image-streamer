from typing import Text, Dict, Any, List
from collections.abc import Generator

import boto3
import prodigy
import json
from prodigy.util import img_to_b64_uri
from prodigy.components.db import connect


s3 = boto3.client('s3')


@prodigy.recipe("stream-from-s3")
def stream_from_s3(dataset: Text, bucket: Text, prefix: Text=None) -> Dict[Text, Any]:

    def before_db(examples: List) -> List[Dict[Text, Any]]:
        '''
        Replaces the raw image data with the S3 key of the image before writing to the Prodigy DB.
        '''
        for eg in examples:
            eg["image"] = eg["meta"]["key"]
        return examples

    def get_stream() -> Generator:
        # Build paginator for S3 objects.
        paginator = s3.get_paginator('list_objects')
        paginate_params = {
            'Bucket': bucket
        }

        if prefix:
            paginate_params['Prefix'] = prefix
        
        page_iterator = paginator.paginate(**paginate_params)

        # Iterate through the pages.
        for page in page_iterator:
            # Iterate through items on the page.
            for obj in page['Contents']:
                img_key = obj['Key']

                # Skip the record if equal to the prefix.
                if img_key == f"{prefix}/":
                    continue

                # Check if the key exists in the database. If so, skip the record.
                if in_db:
                    if img_key in in_db:
                        continue

                # Read the image.
                _img_bytes = s3.get_object(Bucket=bucket, Key=img_key).get('Body').read()

                yield {'image': img_to_b64_uri(_img_bytes, 'image/jpg'), "meta": {"key": img_key}}


    # Load the dataset examples so keys already loaded can be skipped.
    db = connect()
    annotated_examples = db.get_dataset(dataset)
    if annotated_examples:
        in_db = [d['image'] for d in annotated_examples]
    else:
        in_db = None

    # Setup the stream.
    stream = get_stream()

    # Set your Prodigy interface.
    return {
        "view_id": "",
        "dataset": dataset,
        "stream": stream,
        "before_db": before_db,
        "config": {}
    }

