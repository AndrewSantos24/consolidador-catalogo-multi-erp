const { executarConsulta } = require("./connection");

async function criarTabelaProdutos() {
  /**
   * Cria a tabela de produtos caso ela ainda não exista.
   */

  const sql = `
    CREATE TABLE IF NOT EXISTS produtos (
      id VARCHAR(100) PRIMARY KEY,
      sku VARCHAR(100) NOT NULL,
      nome VARCHAR(255) NOT NULL,
      preco_lista NUMERIC(12, 2) NOT NULL,
      preco_desconto NUMERIC(12, 2) NOT NULL,
      categoria VARCHAR(150) NOT NULL,
      imagem_url TEXT,
      atualizado_em TIMESTAMP NOT NULL,
      criado_em TIMESTAMP NOT NULL DEFAULT NOW()
    );
  `;

  await executarConsulta(sql);
}

async function inicializarBanco() {
  /**
   * Inicializa as tabelas necessárias do serviço de catálogo.
   */

  await criarTabelaProdutos();

  console.log("Banco do serviço de catálogo inicializado.");
}

module.exports = {
  inicializarBanco,
};