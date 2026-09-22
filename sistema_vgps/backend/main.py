from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import login, tarefas, respostas


app = FastAPI(
    title="JARVIS / VGPS",
    description="Backend do assistente JARVIS",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login.router)
app.include_router(tarefas.router)
app.include_router(respostas.router)


@app.get("/")
def inicio():
    return {
        "sistema": "JARVIS / VGPS",
        "status": "online",
        "mensagem": "Backend funcionando corretamente"
    }