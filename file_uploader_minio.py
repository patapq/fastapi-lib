from minio import Minio
from minio.error import S3Error

import os
from minio import Minio
import urllib3
from urllib.parse import urlparse
import certifi
from minio.commonconfig import REPLACE, CopySource

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def main():
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "https://192.168.1.110:9000")
    secure = False
    minio_endpoint = urlparse(minio_endpoint)

    if minio_endpoint.scheme == 'https':
        secure = True

    ok_http_client = urllib3.PoolManager(
                timeout=urllib3.util.Timeout(connect=10, read=10),
                maxsize=10,
                cert_reqs='CERT_NONE',
                ca_certs= os.environ.get('SSL_CERT_FILE') or certifi.where(),
                retries=urllib3.Retry(
                    total=5,
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504]
                )
            )

    minioClient = Minio(minio_endpoint.netloc,
                        access_key='minioadmin',
                        secret_key='minioadmin',
                        http_client=ok_http_client,
                        secure=secure)
    # The file to upload, change this path if needed
    dir_name = "/home/student/Desktop/Libcor_Dev/libcor/images/"
    files_list = [f for _,_,files in os.walk(dir_name) for f in files]
    #checking bucket if exists
    bucket_name = "books-images"
    found = minioClient.bucket_exists(bucket_name)
    if not found:
        minioClient.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")
    # file_name = '25.jpg'
    for f in files_list:
        source_file = dir_name + f
        # Upload the file, renaming it in the process
        minioClient.fput_object(bucket_name, f, source_file)
        print(source_file, "successfully uploaded as object", f, "to bucket", bucket_name)

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occured.", exc)
