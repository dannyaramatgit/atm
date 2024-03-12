from fastapi import FastAPI
from routers import actions, admin
from database import models
from database import database

# models.Base.metadata.drop_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
app.include_router(actions.router)
app.include_router(admin.router)
database.init_db()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
