from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import urllib.parse as up
import psycopg2

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

@app.get("/get-count")
def getC():
    cur = conn.cursor()
    cur.execute("SELECT count FROM count;")
    c = cur.fetchone()[0]
    cur.close()
    return c

@app.get("/increment-count")
def incrementC():
    cur = conn.cursor()
    cur.execute("UPDATE count SET count = count + 1")
    cur.close()
    cur = conn.cursor()
    cur.execute("SELECT count FROM count;")
    c = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return c
