const { executarConsulta } = require("../database/connection");
const {
  queryBuscarProdutoPorId,
  queryInserirProduto,
  queryAtualizarProduto,
} = require("../database/queries/produtoQueries");

async function buscarProdutoPorId(id) {
  /**
   * Busca um produto pelo ID no banco de dados.
   *
   * @param {string} id - ID do produto
   * @returns {Promise<object|null>} Produto encontrado ou null
   */

  const resultado = await executarConsulta(queryBuscarProdutoPorId, [id]);

  if (resultado.rows.length === 0) {
    return null;
  }

  return resultado.rows[0];
}

async function inserirProduto(produto) {
  /**
   * Insere um novo produto no banco de dados.
   *
   * @param {object} produto - Produto normalizado recebido da fila
   * @returns {Promise<void>}
   */

  await executarConsulta(queryInserirProduto, [
    produto.id,
    produto.sku,
    produto.nome,
    produto.preco_lista,
    produto.preco_desconto,
    produto.categoria,
    produto.atualizado_em,
  ]);
}

async function atualizarProduto(produto) {
  /**
   * Atualiza um produto existente no banco de dados.
   *
   * @param {object} produto - Produto normalizado recebido da fila
   * @returns {Promise<void>}
   */

  await executarConsulta(queryAtualizarProduto, [
    produto.id,
    produto.sku,
    produto.nome,
    produto.preco_lista,
    produto.preco_desconto,
    produto.categoria,
    produto.atualizado_em,
  ]);
}

module.exports = {
  buscarProdutoPorId,
  inserirProduto,
  atualizarProduto,
};