const API_URL = "http://127.0.0.1:8000";


// ==============================
// USUÁRIO LOGADO
// ==============================

const usuario = localStorage.getItem("jarvis_usuario");

if (!usuario) {
    window.location.href = "index.html";
} else {
    document.getElementById("usuarioLogado").textContent =
        usuario.toUpperCase();
}


// ==============================
// SAIR DO SISTEMA
// ==============================

function sair() {
    localStorage.removeItem("jarvis_usuario");
    window.location.href = "index.html";
}


// ==============================
// CARREGAR TAREFAS
// ==============================

async function carregarTarefas() {

    const lista = document.getElementById("listaTarefas");

    try {

        const resposta = await fetch(`${API_URL}/tarefas`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar tarefas");
        }

        const tarefas = await resposta.json();

        lista.innerHTML = "";

        if (tarefas.length === 0) {
            lista.innerHTML = `
                <p class="sem-tarefas">
                    Nenhuma tarefa cadastrada.
                </p>
            `;
            return;
        }

        tarefas.forEach(tarefa => {

            const item = document.createElement("div");
            item.className = "tarefa-item";

            if (tarefa.status === "concluida") {
                item.classList.add("tarefa-concluida");
            }

            const nome = document.createElement("span");
            nome.textContent = tarefa.nome;

            const acoes = document.createElement("div");
            acoes.className = "tarefa-acoes";

            if (tarefa.status !== "concluida") {

                const concluir = document.createElement("button");

                concluir.textContent = "✓";
                concluir.title = "Concluir tarefa";

                concluir.onclick = () =>
                    concluirTarefa(tarefa.id);

                acoes.appendChild(concluir);
            }

            const excluir = document.createElement("button");

            excluir.textContent = "×";
            excluir.title = "Excluir tarefa";

            excluir.onclick = () =>
                excluirTarefa(tarefa.id);

            acoes.appendChild(excluir);

            item.appendChild(nome);
            item.appendChild(acoes);

            lista.appendChild(item);
        });

    } catch (erro) {

        console.error(erro);

        lista.innerHTML = `
            <p class="erro">
                Não foi possível carregar as tarefas.
            </p>
        `;
    }
}


// ==============================
// CRIAR TAREFA
// ==============================

async function adicionarTarefa() {

    const campo = document.getElementById("novaTarefa");
    const nome = campo.value.trim();

    if (!nome) {
        return;
    }

    try {

        const resposta = await fetch(`${API_URL}/tarefas`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                nome: nome
            })
        });

        if (!resposta.ok) {
            throw new Error("Erro ao criar tarefa");
        }

        campo.value = "";

        await carregarTarefas();

    } catch (erro) {

        console.error(erro);
        alert("Não foi possível criar a tarefa.");
    }
}


// ==============================
// CONCLUIR TAREFA
// ==============================

async function concluirTarefa(id) {

    try {

        const resposta = await fetch(
            `${API_URL}/tarefas/${id}/concluir`,
            {
                method: "PATCH"
            }
        );

        if (!resposta.ok) {
            throw new Error("Erro ao concluir tarefa");
        }

        await carregarTarefas();

    } catch (erro) {

        console.error(erro);
        alert("Não foi possível concluir a tarefa.");
    }
}


// ==============================
// EXCLUIR TAREFA
// ==============================

async function excluirTarefa(id) {

    const confirmar = confirm(
        "Deseja realmente excluir esta tarefa?"
    );

    if (!confirmar) {
        return;
    }

    try {

        const resposta = await fetch(
            `${API_URL}/tarefas/${id}`,
            {
                method: "DELETE"
            }
        );

        if (!resposta.ok) {
            throw new Error("Erro ao excluir tarefa");
        }

        await carregarTarefas();

    } catch (erro) {

        console.error(erro);
        alert("Não foi possível excluir a tarefa.");
    }
}


// ==============================
// COMANDOS REAIS DO JARVIS
// ==============================

async function processarComando() {

    const campo =
        document.getElementById("comandoJarvis");

    const resposta =
        document.getElementById("respostaJarvis");

    const comando = campo.value.trim();

    if (!comando) {
        return;
    }

    resposta.textContent = "PROCESSANDO...";

    campo.disabled = true;

    try {

        const requisicao = await fetch(
            `${API_URL}/jarvis/comando`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    comando: comando
                })
            }
        );

        const dados = await requisicao.json();

        if (!requisicao.ok) {
            throw new Error(
                dados.detail || "Erro ao processar comando"
            );
        }

        resposta.textContent = dados.resposta;

        if (dados.acao === "tarefa_criada") {
            await carregarTarefas();
        }

        campo.value = "";

    } catch (erro) {

        console.error(erro);

        resposta.textContent =
            "Não foi possível comunicar com o núcleo JARVIS.";

    } finally {

        campo.disabled = false;
        campo.focus();
    }
}


// ==============================
// EVENTOS
// ==============================

document
    .getElementById("btnAdicionar")
    .addEventListener(
        "click",
        adicionarTarefa
    );


document
    .getElementById("novaTarefa")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {
                adicionarTarefa();
            }
        }
    );


document
    .getElementById("btnComando")
    .addEventListener(
        "click",
        processarComando
    );


document
    .getElementById("comandoJarvis")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {
                processarComando();
            }
        }
    );


// ==============================
// INICIALIZAÇÃO
// ==============================

carregarTarefas();

// ==============================
// RECONHECIMENTO DE VOZ
// ==============================

const btnMicrofone = document.getElementById("btnMicrofone");
const statusVoz = document.getElementById("statusVoz");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (SpeechRecognition) {

    const reconhecimento = new SpeechRecognition();

    reconhecimento.lang = "pt-BR";
    reconhecimento.continuous = false;
    reconhecimento.interimResults = false;

    statusVoz.textContent = "DISPONÍVEL";
    statusVoz.classList.remove("aguardando");
    statusVoz.classList.add("online");


    btnMicrofone.addEventListener("click", () => {

        try {
            reconhecimento.start();
        } catch (erro) {
            console.log("Reconhecimento já iniciado.");
        }

    });


    reconhecimento.onstart = () => {

        btnMicrofone.classList.add("ouvindo");

        statusVoz.textContent = "OUVINDO...";

        const resposta =
            document.getElementById("respostaJarvis");

        resposta.textContent =
            "Estou ouvindo, Rafael...";
    };


    reconhecimento.onresult = async (event) => {

        const comando =
            event.results[0][0].transcript;

        const campo =
            document.getElementById("comandoJarvis");

        campo.value = comando;

        const resposta =
            document.getElementById("respostaJarvis");

        resposta.textContent =
            `Você disse: "${comando}"`;

        await processarComando();
    };


    reconhecimento.onerror = (event) => {

        console.error(
            "Erro no reconhecimento de voz:",
            event.error
        );

        const resposta =
            document.getElementById("respostaJarvis");

        if (event.error === "not-allowed") {

            resposta.textContent =
                "O acesso ao microfone foi bloqueado pelo navegador.";

        } else if (event.error === "no-speech") {

            resposta.textContent =
                "Não consegui ouvir nenhum comando.";

        } else {

            resposta.textContent =
                "Não consegui reconhecer sua voz.";
        }
    };


    reconhecimento.onend = () => {

        btnMicrofone.classList.remove("ouvindo");

        statusVoz.textContent = "DISPONÍVEL";
    };

} else {

    statusVoz.textContent = "NÃO SUPORTADO";

    btnMicrofone.disabled = true;

    document.getElementById("respostaJarvis").textContent =
        "Este navegador não oferece reconhecimento de voz.";
}