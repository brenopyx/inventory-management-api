import { login } from "./api.js";
import { salvarToken } from "./auth.js";
const form = document.getElementById("login-form");
form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    try {
        const resultado = await login(email, senha);
        salvarToken(resultado.access_token);
        window.location.href = "dashboard.html";
    }
    catch (erro) {
        const mensagemErro = document.getElementById("error-message");
        if (mensagemErro) {
            mensagemErro.textContent = "Email ou senha incorretos";
        }
    }
});
