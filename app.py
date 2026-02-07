import edge_tts
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


app = FastAPI()


class TTSRequest(BaseModel):
    text: str



@app.post("/tts-stream")
async def tts_stream(req: TTSRequest):

    async def audio_generator():
        communicate = edge_tts.Communicate(
            req.text,
            voice="en-US-AriaNeural",
            rate="+15%"
        )

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    return StreamingResponse(
        audio_generator(),
        media_type="audio/mpeg",
        headers={
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)