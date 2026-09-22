import os
import sqlite3

CAMINHO_BANCO = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "banco",
        "banco.db"
    )
)


def conectar():
    os.makedirs(os.path.dirname(CAMINHO_BANCO), exist_ok=True)

    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente'
        )
    """)

    conn.commit()

    return conn