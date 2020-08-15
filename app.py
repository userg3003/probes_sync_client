import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import uvicorn

from fastapi import Depends, File, UploadFile, HTTPException, Security
from fastapi.security import APIKeyHeader

from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.responses import JSONResponse

src_path = Path.cwd()
load_dotenv(dotenv_path=src_path.joinpath(".deploy", ".envs", "local.env"))
token = os.environ.get("TOKEN")
port = os.environ.get("PORT")
host = os.environ.get("HOST")
schema = os.environ.get("SCHEMA")

logger.info(f"schema: {schema} host: {host}  port: {port}")

app = FastAPI()

api_token = APIKeyHeader(name="token")


class Token(BaseModel):
    value: str


def get_current_token(oauth_header: str = Security(api_token)):
    # logger.debug(f"oauth_header {oauth_header}")
    token = Token(value=oauth_header)
    # logger.debug(f"token {token}")
    return token


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
async def onefile(file: bytes = File(...)):
    logger.debug(f"FILE ----------------------:\n{file}\n   =========================")
    file_src = file.decode("utf-8-sig")
    logger.debug(f"FILE --------- decoded -------------:\n{file_src}\n   ============= decoded ============")
    if file is None:
        # error = json.dumps(blocks[0])
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content="File is None")
    return JSONResponse(status_code=HTTP_200_OK, content=file_src)


@app.post("/onefile_auth/")
async def onefile_auth(file: bytes = File(...), token_: Token = Depends(get_current_token)):
    logger.debug(f"FILE ----------------------:\n{file}\n   =========================")
    file_src = file.decode("utf-8-sig")
    logger.debug(f"FILE --------- decoded -------------:\n{file_src}\n   ============= decoded ============")
    if file is None:
        # error = json.dumps(blocks[0])
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content="File is None")
    return JSONResponse(status_code=HTTP_200_OK, content=file_src)


@app.post("/severalfiles/")
async def severalfiles(files: List[UploadFile] = File(...)):
    logger.debug(f"FILES ----------------------:  {len(files)}  :=========================")
    if files is None:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content="Files is None")
    content = {"count_files": len(files), 'files': [{'name': file.filename} for file in files]}
    return JSONResponse(status_code=HTTP_200_OK, content=content)


@app.post("/severalfiles_auth_token/")
async def severalfiles_auth_token(files: List[UploadFile] = File(...), token_: Token = Depends(get_current_token)):
    logger.debug(f"token {token_}")
    if files is None:
        # error = json.dumps(blocks[0])
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content="Files is None")
    content = {"count_files": len(files), 'files': [{'name': file.filename} for file in files]}

    return JSONResponse(status_code=HTTP_200_OK, content=content)


if __name__ == "__main__":
    logger.info(f'START Service')
    uvicorn.run(app, host="0.0.0.0", port=int(port))
