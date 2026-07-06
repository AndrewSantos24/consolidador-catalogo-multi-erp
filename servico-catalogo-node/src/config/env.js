require("dotenv").config();

const env = {
  porta: process.env.PORTA || 3000,
  nomeServico: process.env.NOME_SERVICO || "Serviço de Catálogo - Multi-ERP",
  ambiente: process.env.AMBIENTE || "desenvolvimento",
  databaseUrl: process.env.DATABASE_URL,
  rabbitmqUrl: process.env.RABBITMQ_URL,
  rabbitmqFilaProdutos:
    process.env.RABBITMQ_FILA_PRODUTOS || "catalogo.produtos.normalizados",
};

module.exports = env;