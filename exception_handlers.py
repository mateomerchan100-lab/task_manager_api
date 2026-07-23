from fastapi import Request
from fastapi.responses import JSONResponse
import sqlite3

def integrity_error_handler(request: Request, exc: sqlite3.IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"data":None, "error": "Task already exists"}
    )



def generic_error_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={"data": None, "error": "An internal error has occurred"}
    )