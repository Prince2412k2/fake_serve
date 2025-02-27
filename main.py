import json
import time
from fastapi import FastAPI, Header, HTTPException
import uvicorn
from pydantic import BaseModel, model_validator, Field
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

    @model_validator(mode="before")
    def check_length(cls, values):
        val = values.get("content", "")
        input_token = count_tokens(str(val))  # Ensure it works with dict
        if input_token > 32000:
            raise ValueError(f"TOEKN EXCEEDED LIMIT {input_token=} > 32000")
        return values


class PayloadSchema(BaseModel):
    model: str
    messages: List[MessageSchema]
    max_tokens: Optional[int] = 32000
    stream: Optional[bool] = False
    temprature: Optional[float] = 0.0
    top_p: Optional[float] = 0.0


class ChoiceSchema(BaseModel):
    index: uuid.UUID = Field(default_factory=uuid.uuid4)
    messages: MessageSchema


class SummaryResponseSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    object_type: str = "chat.completions"
    created: int = int(time.time())
    model: str
    choices: ChoiceSchema
    usage: UsageSchema


@app.get("/")
async def main() -> dict[str, str]:
    return {"hello": "world"}


@app.post("/completions/")
async def instruct_response(
    payload: PayloadSchema,
    authorization: str = Header(...),
    Content_Type: str = Header(None),
):
    if authorization != "FAKETOKEN":
        raise HTTPException(status_code=401, detail="Wrong api key")
    model = payload.model
    prompt = ""
    for msg in payload.messages:
        if msg.role == "User":
            prompt = msg.content

        elif msg.role == "System":
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
    return SummaryResponseSchema(
        model=model,
        choices=ChoiceSchema(
            messages=MessageSchema(role="Assistant", content=json.dumps(merged_output))
        ),
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
        port=8000,
        log_level="debug",
        reload=True,
    )
