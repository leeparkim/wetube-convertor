import json
import os
import subprocess
import shlex
import boto3

S3_DESTINATION_BUCKET = "wetube-eunseo"


def handler(event, context):
    video_id = event['video_id']
    filename = event['filename']
    file_ext = event['file_ext']
    s3_source_signed_url = f"https://wetube-eunseo.s3.ap-northeast-2.amazonaws.com/{video_id}/{filename}.{file_ext}"

    os.makedirs(f"/tmp/{video_id}", exist_ok=True)

    s3_client = boto3.client('s3')
    ffmpeg_cmd = f"ffmpeg -i \"{s3_source_signed_url}\" -codec: copy -start_number 0 -hls_time 10 " \
                 f"-hls_list_size 0 -hls_segment_filename \'/tmp/{video_id}/{filename}_%d.ts\' " \
                 f"-f hls /tmp/{video_id}/{filename}.m3u8"

    command1 = shlex.split(ffmpeg_cmd)
    p1 = subprocess.run(command1)

    upload_file_names = []
    for (sourceDir, dirname, filename) in os.walk(f"/tmp/{video_id}"):
        upload_file_names.extend(filename)
        break

    for filename in upload_file_names:
        source_path = os.path.join(f"/tmp/{video_id}", filename)
        s3_path = os.path.join(f"{video_id}", filename)
        s3_client.upload_file(source_path, S3_DESTINATION_BUCKET, s3_path)

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }


