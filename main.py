from fastapi import FastAPI
from routers.tasks_router import router as tasks_router
from routers.auth_router import router as auth_router
from database.database import init_db
from exception_handlers import integrity_error_handler, generic_error_handler
import sqlite3



app = FastAPI()
app.add_exception_handler (sqlite3.IntegrityError, integrity_error_handler)
app.add_exception_handler (Exception, generic_error_handler)

init_db()

app.include_router(tasks_router)
app.include_router(auth_router)


