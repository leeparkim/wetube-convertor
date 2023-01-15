import os
import shlex
import subprocess
import boto3
from s3_const import S3_BUCKET_NAME, S3_BUCKET_URL
from directory import create_dir


def upload_video(video_path: str, video_id: int, filename: str):
    s3_client = boto3.client('s3')
    upload_file_names = []
    for (sourceDir, dirname, now_file) in os.walk(video_path):
        upload_file_names.extend(now_file)
        break

    for now_file in upload_file_names:
        source_path = os.path.join(video_path, now_file)
        s3_path = os.path.join(f"{video_id}", now_file)
        s3_client.upload_file(source_path, S3_BUCKET_NAME, s3_path)

    return f"{S3_BUCKET_URL}/{video_id}/{filename}.m3u8"


def convert_video(video_url: str, video_id: int, filename: str):
    video_path = f"/tmp/{video_id}"
    create_dir(video_path)
    
    ffmpeg_cmd = f"ffmpeg -i \"{video_url}\" -codec: copy -start_number 0 -hls_time 10 " \
                 f"-hls_list_size 0 -hls_segment_filename \'{video_path}/{filename}_%d.ts\' " \
                 f"-f hls {video_path}/{filename}.m3u8"

    command1 = shlex.split(ffmpeg_cmd)
    subprocess.run(command1)
    
    return video_path


def update_video_info(conn, video_id: int, file_url: str):
    cursor = conn.cursor()
    sql = "update video set file_url = %s, video_status = %s where id = %s"
    cursor.execute(sql, (file_url, "COMPLETE", video_id))
    conn.commit()
