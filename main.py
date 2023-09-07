from sched import scheduler
import time
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
def build_results():
    df = {"key":"value"}
    df = pandas.read_csv("api.csv").to_dict(orient='records')

    return df

if __name__ == "__main__":
    uvicorn.run("main:app",port=8001,reload=True)

@app.get("/buildtxt")
def check_for_new_files(): 
 def save_data_to_mongodb_and_remove(file_path):
    while True:
        scheduler.run_pending()
        time.sleep(1)
    

    




