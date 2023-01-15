import json
import db
from directory import delete_dir
from video import upload_video, convert_video, update_video_info
from s3_const import S3_BUCKET_URL 


def handler(event, context):
    video_id = event['video_id']
    filename = event['filename']
    file_ext = event['file_ext']
    s3_source_signed_url = f"{S3_BUCKET_URL}/{video_id}/{filename}.{file_ext}"

    video_path = convert_video(s3_source_signed_url, video_id, filename)
    print("convert done")
    s3_video_url = upload_video(video_path, video_id, filename)
    print("video upload done")

    conn = db.connect()
    print("Database connected")
    update_video_info(conn, video_id, s3_video_url)
    print("change database status")
    
    delete_dir(video_path)
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }


