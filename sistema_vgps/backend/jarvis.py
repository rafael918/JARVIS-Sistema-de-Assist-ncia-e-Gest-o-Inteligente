import os
import subprocess
import webbrowser

from backend.database import conectar


def processar_comando(comando: str):
    texto = comando.lower().strip()

    # =========================
    # SAUDAÇÕES
    # =========================

    if texto in ["olá", "ola", "oi", "jarvis"]:
        return {
            "resposta": "Olá, Rafael. JARVIS operacional.",
            "acao": "resposta"
        }

    # =========================
    # CRIAR TAREFA
    # =========================

    prefixos_tarefa = [
        "crie uma tarefa ",
        "criar tarefa ",
        "adicione uma tarefa ",
        "adicionar tarefa "
    ]

    for prefixo in prefixos_tarefa:

        if texto.startswith(prefixo):

            nome = comando[len(prefixo):].strip()

            if not nome:
                return {
                    "resposta": "Informe o nome da tarefa.",
                    "acao": "erro"
                }

            conn = conectar()

            try:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO tarefas (nome, status)
                    VALUES (?, ?)
                    """,
                    (nome, "pendente")
                )

                conn.commit()

            finally:
                conn.close()

            return {
                "resposta": f"Tarefa criada: {nome}",
                "acao": "tarefa_criada"
            }

    # =========================
    # LISTAR TAREFAS
    # =========================

    if (
        "minhas tarefas" in texto
        or "listar tarefas" in texto
        or "mostre as tarefas" in texto
        or "quais são as tarefas" in texto
        or "quais sao as tarefas" in texto
    ):

        conn = conectar()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT nome
                FROM tarefas
                WHERE status = 'pendente'
                ORDER BY id DESC
                """
            )

            tarefas = cursor.fetchall()

        finally:
            conn.close()

        if not tarefas:
            return {
                "resposta": "Você não possui tarefas pendentes.",
                "acao": "tarefas"
            }

        nomes = [tarefa["nome"] for tarefa in tarefas]

        return {
            "resposta":
                "Tarefas pendentes: " + "; ".join(nomes),
            "acao": "tarefas"
        }

    # =========================
    # GOOGLE
    # =========================

    if (
        texto == "abra o google"
        or texto == "abrir google"
        or texto == "abra google"
    ):

        webbrowser.open("https://www.google.com")

        return {
            "resposta": "Abrindo o Google.",
            "acao": "abrir_programa"
        }

    # =========================
    # CALCULADORA
    # =========================

    if (
        texto == "abra a calculadora"
        or texto == "abrir calculadora"
        or texto == "abra calculadora"
    ):

        subprocess.Popen(["calc.exe"])

        return {
            "resposta": "Abrindo a calculadora.",
            "acao": "abrir_programa"
        }

    # =========================
    # BLOCO DE NOTAS
    # =========================

    if (
        texto == "abra o bloco de notas"
        or texto == "abrir bloco de notas"
        or texto == "abra bloco de notas"
    ):

        subprocess.Popen(["notepad.exe"])

        return {
            "resposta": "Abrindo o Bloco de Notas.",
            "acao": "abrir_programa"
        }

    # =========================
    # POWER BI
    # =========================

    if (
        texto == "abra o power bi"
        or texto == "abrir power bi"
        or texto == "abra power bi"
    ):

        caminhos = [
            os.path.expandvars(
                r"%ProgramFiles%\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles%\Microsoft Power BI Desktop RS\bin\PBIDesktop.exe"
            )
        ]

        for caminho in caminhos:

            if os.path.exists(caminho):

                subprocess.Popen([caminho])

                return {
                    "resposta": "Abrindo o Power BI.",
                    "acao": "abrir_programa"
                }

        return {
            "resposta":
                "Não encontrei a instalação do Power BI neste computador.",
            "acao": "erro"
        }

    # =========================
    # STATUS
    # =========================

    if (
        "status do sistema" in texto
        or texto == "status"
    ):

        return {
            "resposta":
                "Backend online, banco de dados online e núcleo JARVIS ativo.",
            "acao": "status"
        }

    # =========================
    # COMANDO NÃO RECONHECIDO
    # =========================

    return {
        "resposta":
            "Ainda não reconheço esse comando.",
        "acao": "desconhecida"
    }