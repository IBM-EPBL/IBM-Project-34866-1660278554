import ibm_boto3
from ibm_botocore.client import Config, ClientError
import uuid
from flask import current_app


def get_uuid():
    return str(uuid.uuid4().hex)


def multi_part_upload(file_path):
    COS_ENDPOINT = "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints"
    COS_API_KEY_ID = "9GB6cjqiwqHEtoqRJn-mq9y_bcq3AXSSYu3mWFE-Nw84"
    COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/edd8f023f2a14c8c916fd81fc75075b7:369cde2c-0c33-434c-aad5-1e6561504ffc::"
    COS_BUCKET_NAME = "cloud-object-storage-3j-cos-standard-7ip"
    # Create resource
    cos = ibm_boto3.resource("s3",
                             ibm_api_key_id=COS_API_KEY_ID,
                             ibm_service_instance_id=COS_INSTANCE_CRN,
                             config=Config(signature_version="oauth"),
                             endpoint_url=COS_ENDPOINT
                             )
    item_name = get_uuid() + '.' + get_extension(file_path)
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(
            item_name, COS_BUCKET_NAME))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(COS_BUCKET_NAME, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
        return item_name  # send object name
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
        return 'none'  # no file
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))
        return 'none'  # no file


def get_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1]


def get_signed_url(receipt):

    bucket_name = "cloud-object-storage-3j-cos-standard-7ip"
    key_name = receipt
    http_method = 'get_object'
    expiration = 60  # time in seconds, default:600

    access_key = "3424bba80001451588bd8fc42b0aabb0"
    secret_key = "86d24d4f84255aa59e13241c82cfa567113815487e1a589f"
    # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
    cos_service_endpoint = "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints"

    cos = ibm_boto3.client("s3",
                           aws_access_key_id=access_key,
                           aws_secret_access_key=secret_key,
                           endpoint_url=cos_service_endpoint
                           )

    signedUrl = cos.generate_presigned_url(http_method, Params={
        'Bucket': bucket_name, 'Key': key_name}, ExpiresIn=expiration)
    return signedUrl