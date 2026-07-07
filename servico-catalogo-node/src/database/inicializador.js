const { executarConsulta } = require("./connection");
const {
  queryCriarTabelaProdutos,
} = require("./queries/queryCriarTabelaProdutos");

async function criarTabelaProdutos() {
  /**
   * Cria a tabela de produtos caso ela ainda não exista.
   */
  await executarConsulta(queryCriarTabelaProdutos);
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