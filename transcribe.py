from genericpath import exists
import time
import boto3
import os
import logging
from botocore.exceptions import ClientError
import sys


file_name = sys.argv[1]
if not os.path.exists(file_name):
    logging.error('Please supply a filename to transcribe')
    sys.exit(1)

transcribe = boto3.client('transcribe')
object_name = os.path.basename(file_name)
job_name = f"{object_name}-transcription"
s3 = boto3.client('s3')
bucket = "roystranscriptionbucket"

logging.info('Sending audio file to S3')
try:
    response = s3.upload_file(file_name, bucket, object_name)
except ClientError as e:
    logging.error(e)
    exit(1)

try:
    logging.info('Transcribing...')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f"s3://{bucket}/{object_name}"},
        MediaFormat='wav',
        LanguageCode='he-IL',
        OutputBucketName=bucket,
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        logging.info("Not ready yet...")
        time.sleep(5)

    logging.info('Transcription finished. Download')
    transcription_file = job_name + '.json'
    s3.download_file(bucket, transcription_file, transcription_file)
    logging.info('Cleaning up resources')
    s3.delete_object(Bucket=bucket, Key=transcription_file)
    transcribe.delete_transcription_job(TranscriptionJobName=job_name)
except Exception as e:
    logging.error(e)
finally:
    logging.info('Delete audio file from S3')
    s3.delete_object(Bucket=bucket, Key=object_name)

logging.info('Done. Result in ')
