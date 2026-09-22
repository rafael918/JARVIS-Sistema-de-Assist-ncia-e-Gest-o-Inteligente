from pydantic import BaseModel, Field


class Usuario(BaseModel):
    usuario: str = Field(min_length=3, max_length=50)
    senha: str = Field(min_length=4, max_length=100)


class Tarefa(BaseModel):
    nome: str = Field(min_length=1, max_length=200)


class AtualizarTarefa(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=200)
    status: str | None = None