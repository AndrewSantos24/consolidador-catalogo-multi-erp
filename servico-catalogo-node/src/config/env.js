require("dotenv").config();

const env = {
  porta: process.env.PORTA || 3000,
  nomeServico: process.env.NOME_SERVICO || "Serviço de Catálogo - Multi-ERP",
  ambiente: process.env.AMBIENTE || "desenvolvimento",
};

module.exports = env;