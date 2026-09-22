from fastapi import APIRouter, HTTPException
from backend.database import conectar
from backend.models import Tarefa, AtualizarTarefa

router = APIRouter()


@router.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tarefas (nome, status) VALUES (?, ?)",
            (tarefa.nome, "pendente")
        )

        conn.commit()

        tarefa_id = cursor.lastrowid

        return {
            "mensagem": "Tarefa criada com sucesso",
            "id": tarefa_id,
            "nome": tarefa.nome,
            "status": "pendente"
        }

    finally:
        conn.close()


@router.get("/tarefas")
def listar_tarefas():
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome, status
            FROM tarefas
            ORDER BY id DESC
        """)

        tarefas = cursor.fetchall()

        return [dict(tarefa) for tarefa in tarefas]

    finally:
        conn.close()


@router.get("/tarefas/{tarefa_id}")
def buscar_tarefa(tarefa_id: int):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, status FROM tarefas WHERE id = ?",
            (tarefa_id,)
        )

        tarefa = cursor.fetchone()

        if tarefa is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
            )

        return dict(tarefa)

    finally:
        conn.close()


@router.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, dados: AtualizarTarefa):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, status FROM tarefas WHERE id = ?",
            (tarefa_id,)
        )

        tarefa = cursor.fetchone()

        if tarefa is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
            )

        novo_nome = (
            dados.nome
            if dados.nome is not None
            else tarefa["nome"]
        )

        novo_status = (
            dados.status
            if dados.status is not None
            else tarefa["status"]
        )

        status_permitidos = ["pendente", "concluida"]

        if novo_status not in status_permitidos:
            raise HTTPException(
                status_code=400,
                detail="Status deve ser 'pendente' ou 'concluida'"
            )

        cursor.execute("""
            UPDATE tarefas
            SET nome = ?, status = ?
            WHERE id = ?
        """, (novo_nome, novo_status, tarefa_id))

        conn.commit()

        return {
            "mensagem": "Tarefa atualizada com sucesso",
            "id": tarefa_id,
            "nome": novo_nome,
            "status": novo_status
        }

    finally:
        conn.close()


@router.patch("/tarefas/{tarefa_id}/concluir")
def concluir_tarefa(tarefa_id: int):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM tarefas WHERE id = ?",
            (tarefa_id,)
        )

        tarefa = cursor.fetchone()

        if tarefa is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
            )

        cursor.execute("""
            UPDATE tarefas
            SET status = 'concluida'
            WHERE id = ?
        """, (tarefa_id,))

        conn.commit()

        return {
            "mensagem": "Tarefa concluída com sucesso",
            "id": tarefa_id,
            "status": "concluida"
        }

    finally:
        conn.close()


@router.delete("/tarefas/{tarefa_id}")
def excluir_tarefa(tarefa_id: int):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM tarefas WHERE id = ?",
            (tarefa_id,)
        )

        tarefa = cursor.fetchone()

        if tarefa is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
            )

        cursor.execute(
            "DELETE FROM tarefas WHERE id = ?",
            (tarefa_id,)
        )

        conn.commit()

        return {
            "mensagem": "Tarefa excluída com sucesso",
            "id": tarefa_id
        }

    finally:
        conn.close()
