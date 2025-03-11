import json
import time
from fastapi import FastAPI, Header, HTTPException
import uvicorn
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from utils import count_tokens, get_chars, get_places, get_summary, load
import uuid

app = FastAPI()


class UsageSchema(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class MessageSchema(BaseModel):
    role: str
    content: str


class GrammarSchema(BaseModel):
    type_: str = Field(alias="type", default="json")
    value: dict = Field(default_factory=dict)

    class Config:
        population_by_name = True


class ParameterSchema(BaseModel):
    repetition_penalty: Optional[float] = 1.3
    grammar: GrammarSchema


class PayloadSchema(BaseModel):
    model: str
    messages: List[MessageSchema]
    max_tokens: Optional[int] = 32000
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.0
    parameters: ParameterSchema


class ChoiceSchema(BaseModel):
    index: uuid.UUID = Field(default_factory=uuid.uuid4)
    message: MessageSchema


class SummaryResponseSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    object_type: str = "chat.completions"
    created: int = int(time.time())
    model: str
    choices: List[ChoiceSchema]
    usage: UsageSchema


@app.get("/")
async def main() -> dict[str, str]:
    return {"hello": "world"}


@app.post("/completions/")
async def instruct_response(
    payload: PayloadSchema,
    authorization: str = Header(...),
    content_Type: str = Header(None),
):
    if authorization != "Bearer FAKETOKEN":
        raise HTTPException(status_code=401, detail="Wrong api key")
    model = payload.model
    prompt = ""
    for msg in payload.messages:
        if msg.role == "user":
            prompt = msg.content

        elif msg.role == "system":
            pass
        else:
            raise HTTPException(
                status_code=400, detail="Missing the User atribute messages in payload"
            )
    model = payload.model
    summary = await get_summary(prompt)
    characters = await get_chars()
    places = await get_places()
    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(summary["summary"])
    merged_output = {**summary, **characters, **places}
    time.sleep(2)
    return SummaryResponseSchema(
        model=model,
        choices=[
            ChoiceSchema(
                message=MessageSchema(
                    role="assistant", content=json.dumps(merged_output)
                )
            )
        ],
        usage=UsageSchema(
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
        ),
    )


if __name__ == "__main__":
    load()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        reload=True,
    )
