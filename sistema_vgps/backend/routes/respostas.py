from fastapi import APIRouter
from pydantic import BaseModel

from backend.jarvis import processar_comando


router = APIRouter()


class ComandoJarvis(BaseModel):
    comando: str


@router.post("/jarvis/comando")
def executar_comando(dados: ComandoJarvis):

    resultado = processar_comando(dados.comando)

    return resultado


@router.get("/respostas")
def listar_respostas():

    return {
        "mensagem": "Núcleo JARVIS operacional"
    }