import boto3
from django.conf import settings

class Bucket:
    """CDN Bucket manager

    __init__ creates connection.

    NOTE:
        none of these methods are async. use public interface in tasks.py modules instead.
    """

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name='s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        results = self.conn.list_objects_v2(Bucket=settings.AWS_BUCKET_NAME)
        if results["KeyCount"]:
            return results["Contents"]
        return None

    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)
        return True

bucket = Bucket()