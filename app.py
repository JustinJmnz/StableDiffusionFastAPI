import uvicorn
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlmodel import SQLModel
from DataAccess.DatabaseService import engine
from routers.content import router as contentRouter
from routers.web import router as webRouter


app = FastAPI(title='Diffusion')
app.include_router(contentRouter)
app.include_router(webRouter)

app.mount(
    "/Templates",
    StaticFiles(directory=Path(__file__).parent.absolute() / "Templates"),
    name="Templates",
)

@app.on_event('startup')
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.on_event('shutdown') 
def on_shutdown():
    SQLModel.metadata.drop_all(engine)

if __name__ == "__main__":
    uvicorn.run("app:app", log_level="info", reload=True)