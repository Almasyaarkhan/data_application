from sched import scheduler
import time,os,tempfile
from fastapi import FastAPI
import uvicorn
from dbmanager import db_connect 
import pandas
import boto3
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from botocore.exceptions import NoCredentialsError 

# app = FastAPI()
db = db_connect()


# @app.get("/data")
def import_data():
    pass


# @app.get("/build")
def build_results(new_file):
    df = pandas.read_csv(new_file).to_dict(orient='records')

    insert_data = db['mycollection'].insert_one(df)

    os.remove(new_file)
    return df
  
def check_and_process_files():
    
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".csv"):  # Change the file extension as needed
            print('newfile found')
            file_path = os.path.join(os.getcwd(), filename)
            build_results(file_path)



load_dotenv()

aws_access_key_id = os.getenv("Accesskey")
aws_secret_access_key = os.getenv("Secretaccesskey")
bucket_name = os.getenv("bucket_name")


# Function to check and process CSV files in an S3 bucket
def check_and_process_s3_files():
    print('s3 processing started')
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        
        # List files in the S3 bucket
        s3_files = s3.list_objects(Bucket=bucket_name)
        print(s3_files)
        for s3_file in s3_files.get('Contents', []):
            s3_file_key = s3_file['Key']
            
            # Check if the S3 object is a CSV file
            if s3_file_key.endswith(".csv"):
                # Download the S3 file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    s3.download_fileobj(Bucket=bucket_name, Key=s3_file_key, Fileobj=temp_file)
                    temp_file_path = temp_file.name
                
                # Process the downloaded CSV file
                with open(temp_file_path, 'rb') as local_file:
                    build_results(local_file)
                
                # Delete the processed file from the S3 bucket
                # s3.delete_object(Bucket=bucket_name, Key=s3_file_key)
                
                # Remove the temporary local file
                os.remove(temp_file_path)
    except NoCredentialsError:
        print("No AWS credentials found. Make sure to configure your AWS credentials.")

# Create a scheduler to run the S3 file checking function every 10 minutes
print('job started')
# scheduler = BackgroundScheduler()
# scheduler.add_job(check_and_process_s3_files, trigger=IntervalTrigger(minutes=1))
# scheduler.start()
   

while True:
    time.sleep(30)
    check_and_process_s3_files()













# if __name__ == "__main__":
#     uvicorn.run("main:app",port=8001,reload=True)



    




