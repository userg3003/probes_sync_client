import os
import json
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from fastapi import FastAPI
from fastapi import File
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.responses import JSONResponse
import uvicorn


src_path = Path.cwd()
load_dotenv(dotenv_path=src_path.joinpath(".deploy", ".envs", "local.env"))
token = os.environ.get("TOKEN")
port = os.environ.get("PORT")
host = os.environ.get("HOST")
schema = os.environ.get("SCHEMA")

logger.info(f"schema: {schema} host: {host}  port: {port}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": f"Hello from probe FastApi upload files !!! "}


class Message(BaseModel):
    message: str


@app.post("/onefile/")
async def parser(file: bytes = File(...)):
    logger.debug(f"FILE ----------------------:\n{file}\n   =========================")
    file_src = file.decode("utf-8-sig")
    logger.debug(f"FILE --------- decoded -------------:\n{file_src}\n   ============= decoded ============")
    if file is None:
        # error = json.dumps(blocks[0])
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content="File is None")
    return JSONResponse(status_code=HTTP_200_OK, content=file)


if __name__ == "__main__":
    logger.info(f'START Service')
    uvicorn.run(app, host="0.0.0.0", port=int(port))
