from fastapi import FastAPI

app = FastAPI()


@app.get('/main')
async def main():
    return {"status": "ok"}
