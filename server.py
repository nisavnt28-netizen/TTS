from fastapi import FastAPI
from fastapi.responses import FileResponse
import edge_tts
import uuid

app = FastAPI()

@app.get("/tts")
async def tts(text: str):

    filename = f"{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice="hi-IN-SwaraNeural"
    )

    await communicate.save(filename)

    return FileResponse(filename)
