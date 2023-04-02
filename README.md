# prodigy-s3-image-streamer
I had a use case where I wanted to annotate images in Prodigy that were stored in a S3 bucket. I couldn't find a great example of how to do this so I put together a snippet of how I was able to stream images from S3 to Prodigy for annotation. While this isn't fully featured by any means it worked for my basic use case and figured since I had trouble finding a code example that I'd share this for the benefit of others who have this problem as a template to get started.

The loader accepts three parameters, name of the Prodigy dataset, a S3 bucket name and an optional prefix to filter S3 objects. Based on those parameters a paginator is built to iterate through your S3 objects.

By default when working with images Prodigy will save the raw image to the database. Since images are being streamed from S3 storing them in the Prodigy database is redundant. The `before_db` function will replace the raw image data with the name of the S3 key when the data is saved to the Prodigy database.

A secondary benefit is these keys can be used to speed up streaming of images. The S3 paginator that gets objects in the `get_stream` function checks if a key exists in the Prodigy databse and only load and serve the image if the key isn't in the database.

## Usage

To use the example function you can first update the Prodigy interface at the end of the `s3_loader.py` file to define your Prodigy task.

Then you can call the function with the following command with the following parameters:

- `DATASET`: Name of the Prodigy dataset.
- `BUCKET`: Name of the S3 bucket to load images from.
- `PREFIX`: (Optional) Prefix to limit the objects to load from your Bucket.

```bash
prodigy stream_from_s3 DATASET BUCKET PREFIX -F s3_loader.py
```

## Note:

One assumption in this example is that the objects in the S3 bucket will consist of images. If your S3 bucket has image and non-image data then you will have to adjust the `get_stream` function to skip non-image files.