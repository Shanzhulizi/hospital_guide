import uvicorn
from app.agent.guide_agent import symptom_to_department_tool
from app.chains.rag_chain import get_navigation_answer, get_medical_qa_answer
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.voice.stt import transcribe_audio
app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定 ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    type: str  # symptom / navigate / qa
    input: str

class ChatResponse(BaseModel):
    role: str = "assistant"
    content: str


@app.post("/chat")
def dispatch_chat(request: ChatRequest):
    if request.type == "symptom":
        dept = symptom_to_department_tool(request.input)
        # return {"role": "assistant", "content": f"建议您前往{dept}就诊"}
        return {"role": "assistant", "content": dept}

    elif request.type == "navigate":
        answer = get_navigation_answer(request.input)
        return {"role": "assistant", "content": answer}

    elif request.type == "qa":
        answer = get_medical_qa_answer(request.input)
        return {"role": "assistant", "content": answer}

    else:
        return {"role": "assistant", "content": "无效请求类型，请检查参数"}


from app.voice.tts import stream_text_to_speech

@app.get("/tts")
def tts(text: str):
    return stream_text_to_speech(text)



@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    text = await transcribe_audio(file)
    return {"text": text}



# 添加服务器启动代码
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
