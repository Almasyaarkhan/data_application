from sched import scheduler
import time,os
from fastapi import FastAPI
import uvicorn
from dbmanager import db_connect 
import pandas

app = FastAPI()
db = db_connect()


@app.get("/data")
def import_data():
    pass


@app.get("/build")
def build_results(new_file):
    df = pandas.read_csv(new_file).to_dict(orient='records')

    insert_data = db['mycollection'].insert_one(dict(df))

    os.remove(new_file)
    return df
  
def check_and_process_files():
    
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".csv"):  # Change the file extension as needed
            print('newfile found')
            file_path = os.path.join(os.getcwd(), filename)
            build_results(file_path)



while True:
    time.sleep(300)
    check_and_process_files()

        










if __name__ == "__main__":
    uvicorn.run("main:app",port=8001,reload=True)



    




