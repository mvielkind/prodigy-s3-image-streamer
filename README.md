# prodigy-s3-image-streamer
I had a use case where I wanted to annotate images in Prodigy that were stored in a S3 bucket. I couldn't find a great example of how to do this so I put together a snippet of how I was able to stream images from S3 to Prodigy for annotation. While this isn't fully featured by any means it worked for my basic use case and figured since I had trouble finding a code example that I'd share this for the benefit of others who have this problem as a template to get started.

If you have any issues or suggestions for improvement let me know!

The loader accepts two parameters, a S3 bucket name and an optional prefix to filter S3 objects. Based on those parameters a paginator is built to iterate through your S3 objects. Each object is then returned in the JSON `Image` format expected by Prodigy.

An example binary classification task in Prodigy would look like this where the results of the loader are piped to the classification task where you can substitute details for your 

```bash
prodigy stream_from_s3 BUCKET PREFIX -F s3_loader.py | prodigy mark DATASET - --label LABEL --view-id classification
```
