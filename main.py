from fastapi import FastAPI
import uvicorn
from dbmanager import db_connect 

app = FastAPI()
db = db_connect()


@app.get("/data")
def import_data():
    pass





if __name__ == "__main__":
    uvicorn.run("main:app",port=8001,reload=True)
