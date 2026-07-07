const { executarConsulta } = require("../database/connection");
const {
  queryBuscarProdutoPorId,
  queryInserirProduto,
  queryAtualizarProduto,
  queryListarProdutos,
  queryBuscarProdutoCompletoPorId,
  queryAtualizarImagemProduto,
  queryListarProdutosSemImagem,
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

async function listarProdutos(filtros = {}) {
  /**
   * Lista produtos cadastrados no banco de dados.
   *
   * @param {object} filtros - Filtros opcionais da consulta
   * @returns {Promise<Array>} Lista de produtos encontrados
   */

  const sku = filtros.sku || null;
  const categoria = filtros.categoria || null;

  const resultado = await executarConsulta(queryListarProdutos, [sku, categoria]);

  return resultado.rows;
}

async function buscarProdutoCompletoPorId(id) {
  /**
   * Busca um produto completo pelo ID.
   *
   * @param {string} id - ID do produto
   * @returns {Promise<object|null>} Produto encontrado ou null
   */

  const resultado = await executarConsulta(queryBuscarProdutoCompletoPorId, [id]);

  if (resultado.rows.length === 0) {
    return null;
  }

  return resultado.rows[0];
}

async function atualizarImagemProduto(id, imagemUrl) {
  /**
   * Atualiza a URL da imagem vinculada ao produto.
   *
   * @param {string} id - ID do produto
   * @param {string} imagemUrl - URL da imagem do produto
   * @returns {Promise<object|null>} Produto atualizado ou null
   */

  const resultado = await executarConsulta(queryAtualizarImagemProduto, [
    id,
    imagemUrl,
  ]);

  if (resultado.rows.length === 0) {
    return null;
  }

  return resultado.rows[0];
}

async function listarProdutosSemImagem() {
  /**
   * Lista produtos que ainda não possuem imagem vinculada.
   *
   * @returns {Promise<Array>} Lista de produtos sem imagem
   */

  const resultado = await executarConsulta(queryListarProdutosSemImagem);

  return resultado.rows;
}

module.exports = {
  buscarProdutoPorId,
  inserirProduto,
  atualizarProduto,
  listarProdutos,
  buscarProdutoCompletoPorId,
  atualizarImagemProduto,
  listarProdutosSemImagem
};