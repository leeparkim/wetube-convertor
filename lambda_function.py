import json
import os
import subprocess
import shlex
import boto3

S3_DESTINATION_BUCKET = "wetube-eunseo"


def handler(event, context):
    s3_source_signed_url = "https://wetube-eunseo.s3.ap-northeast-2.amazonaws.com/17011557.mp4"

    s3_client = boto3.client('s3')
    ffmpeg_cmd = "ffmpeg -i \"" + s3_source_signed_url + "\" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls /tmp/filename.m3u8"
    command1 = shlex.split(ffmpeg_cmd)
    p1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    resp = s3_client.put_object(Body=p1.stdout, Bucket=S3_DESTINATION_BUCKET, Key="filename.m3u8")

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }
