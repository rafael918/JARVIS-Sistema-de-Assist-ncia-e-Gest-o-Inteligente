from fastapi import APIRouter, HTTPException
from backend.database import conectar
from backend.models import Usuario

router = APIRouter()


@router.post("/login")
def login(usuario: Usuario):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, usuario
            FROM usuarios
            WHERE usuario = ? AND senha = ?
            """,
            (usuario.usuario, usuario.senha)
        )

        resultado = cursor.fetchone()

        if resultado is None:
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos"
            )

        return {
            "mensagem": "Login realizado com sucesso",
            "usuario": resultado["usuario"]
        }

    finally:
        conn.close()


@router.post("/usuarios")
def criar_usuario(usuario: Usuario):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = ?",
            (usuario.usuario,)
        )

        existente = cursor.fetchone()

        if existente is not None:
            raise HTTPException(
                status_code=409,
                detail="Este usuário já existe"
            )

        cursor.execute(
            """
            INSERT INTO usuarios (usuario, senha)
            VALUES (?, ?)
            """,
            (usuario.usuario, usuario.senha)
        )

        conn.commit()

        return {
            "mensagem": "Usuário criado com sucesso",
            "usuario": usuario.usuario
        }

    finally:
        conn.close()