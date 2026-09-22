const API_URL = "http://127.0.0.1:8000";

const loginForm = document.getElementById("loginForm");
const mensagem = document.getElementById("mensagem");


loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const usuario = document.getElementById("usuario").value.trim();
    const senha = document.getElementById("senha").value;

    mensagem.textContent = "AUTENTICANDO...";
    mensagem.className = "";

    try {

        const resposta = await fetch(`${API_URL}/login`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                usuario: usuario,
                senha: senha
            })

        });


        const dados = await resposta.json();


        if (!resposta.ok) {

            mensagem.textContent =
                dados.detail || "Falha na autenticação.";

            mensagem.className = "erro";

            return;
        }


        mensagem.textContent =
            `ACESSO AUTORIZADO — ${dados.usuario.toUpperCase()}`;

        mensagem.className = "sucesso";


        localStorage.setItem(
            "jarvis_usuario",
            dados.usuario
        );


        setTimeout(() => {

            window.location.href = "tarefas.html";

        }, 1000);


    } catch (erro) {

        console.error(erro);

        mensagem.textContent =
            "ERRO: NÃO FOI POSSÍVEL CONECTAR AO JARVIS.";

        mensagem.className = "erro";

    }

});