import boto3
import os
import traceback

# AWS Credentials (set these in the environment or directly in the script)
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# S3 Bucket and Directory Details
bucket_name = 'npmrd-curator-output'

local_directory = './submissions/'  # Directory containing files to upload

def upload_directory_to_s3(local_directory, bucket_name):
    # Create an S3 client
    s3 = boto3.client('s3', 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    # Get a list of all files in the directory
    files = [os.path.join(root, file) for root, dirs, files in os.walk(local_directory) for file in files]
    total_files = len(files)
    
    if total_files == 0:
        print("No files to upload.")
        return

    print_threshold = total_files // 10
    num_pushed = 0
    
    for file_path in files:
        # Create a relative path for the S3 object key
        relative_path = os.path.relpath(file_path, local_directory)
        s3_key = relative_path

        try:
            s3.upload_file(file_path, bucket_name, s3_key)
            num_pushed += 1

            # Delete the file after successful upload
            os.remove(file_path)

            # Print progress message
            if num_pushed % print_threshold == 0:
                print(f"Completed {num_pushed / total_files * 100:.0f}% of the uploads.")

        except Exception as e:
            print(f"Failed to upload {file_path} to S3: {traceback.print_exc()}")
            
    print(f"Finished pushing {num_pushed} entries!")

if __name__ == "__main__":
    upload_directory_to_s3(local_directory, bucket_name)
