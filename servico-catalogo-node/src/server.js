const express = require("express");

const env = require("./config/env");

const healthRoutes = require("./routes/healthRoutes");
const bancoRoutes = require("./routes/bancoRoutes");
const produtoRoutes = require("./routes/produtoRoutes");
const painelMidiaRoutes = require("./routes/painelmidiaRoutes");

const { iniciarConsumerProdutos } = require("./consumers/produtoConsumer");
const { inicializarBanco } = require("./database/inicializador");

const app = express();

let dependenciasInicializadas = false;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api/v1", healthRoutes);
app.use("/api/v1", bancoRoutes);
app.use("/api/v1", produtoRoutes);
app.use("/api/v1", painelMidiaRoutes);

async function iniciarDependencias() {
  /**
   * Inicializa as dependências principais da aplicação.
   * Ajuda quando PostgreSQL/RabbitMQ ainda estão iniciando no Docker.
   */

  if (dependenciasInicializadas) {
    return;
  }

  try {
    await inicializarBanco();

    dependenciasInicializadas = true;

    iniciarConsumerProdutos();
  } catch (erro) {
    console.error("Erro ao inicializar dependências:", erro.message);
    console.log("Tentando inicializar novamente em 9 segundos...");

    setTimeout(() => {
      iniciarDependencias();
    }, 9000);
  }
}

app.listen(env.porta, () => {
  console.log(`${env.nomeServico} rodando na porta ${env.porta}`);

  iniciarDependencias();
});