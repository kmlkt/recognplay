import easyocr
import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()
reader = easyocr.Reader(["en", "ru"])


@app.post("/files/")
async def create_file(request: Request):
    body = await request.body()
    result = reader.readtext(body, detail=0)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
