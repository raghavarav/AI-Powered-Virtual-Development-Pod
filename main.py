from fastapi import FastAPI
from fastapi import File, UploadFile, HTTPException, Form
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import BAagent, CoderAgent, DesignerAgent, ManagerAgent, TestAgent
import asyncio
import uvicorn
import json

app = FastAPI()
RETRY_DELAY = 20

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_outputs = {
    "user_story" : None,
    "design" : None,
    "code" : None,
    "test_case" : None
}

conversational_history = []

@app.post("/run_agents/", response_class=PlainTextResponse)
async def upload_txt_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed.")
    contents = await file.read()
    InputData = contents.decode("utf-8")

    user_stories = await BAagent.generate_user_stories(InputData)
    agent_outputs["user_story"] = user_stories
    await asyncio.sleep(RETRY_DELAY)

    design = await DesignerAgent.generate_design(user_stories)
    agent_outputs["design"] = design
    await asyncio.sleep(RETRY_DELAY)

    code = await CoderAgent.generate_code(design)
    agent_outputs["code"] = code
    await asyncio.sleep(RETRY_DELAY)

    test_cases = await TestAgent.generate_test_cases(code, design, user_stories)
    agent_outputs["test_case"] = test_cases
    await asyncio.sleep(RETRY_DELAY)

    result = {
        "user_story": user_stories,
        "design": design,
        "code": code,
        "test_case": test_cases
    }

    return json.dumps(result, indent=2)

@app.post("/manager_chat/")
async def manager_conversation(query: str = Form(...)):
    conversation = await ManagerAgent.manager_chat(agent_outputs["user_story"], agent_outputs["design"], agent_outputs["code"], agent_outputs["test_case"], query, conversational_history)
    conversational_history.append({"query" : query, "response" : conversation})

    return conversation

if __name__ == "__main__":
    uvicorn.run("main:app")
