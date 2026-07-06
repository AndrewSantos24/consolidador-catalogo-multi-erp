const {
  atualizarProduto,
  buscarProdutoPorId,
  inserirProduto,
  listarProdutos,
  buscarProdutoCompletoPorId,
  atualizarImagemProduto,
} = require("../repositories/produtoRepository");

function produtoRecebidoEhMaisNovo(produtoRecebido, produtoSalvo) {
  /**
   * Verifica se o produto recebido é mais novo que o produto salvo.
   *
   * @param {object} produtoRecebido - Produto recebido da fila
   * @param {object} produtoSalvo - Produto salvo no banco
   * @returns {boolean} True quando o produto recebido for mais novo
   */

  const dataRecebida = new Date(produtoRecebido.atualizado_em);
  const dataSalva = new Date(produtoSalvo.atualizado_em);

  return dataRecebida > dataSalva;
}

async function salvarOuAtualizarProduto(produto) {
  /**
   * Salva ou atualiza um produto respeitando a regra de atualizado_em.
   *
   * @param {object} produto - Produto normalizado recebido da fila
   * @returns {Promise<object>} Resultado do processamento
   */

  const produtoSalvo = await buscarProdutoPorId(produto.id);

  if (!produtoSalvo) {
    await inserirProduto(produto);

    return {
      acao: "CRIADO",
      mensagem: "Produto criado com sucesso.",
      produto_id: produto.id,
    };
  }

  if (produtoRecebidoEhMaisNovo(produto, produtoSalvo)) {
    await atualizarProduto(produto);

    return {
      acao: "ATUALIZADO",
      mensagem: "Produto atualizado com sucesso.",
      produto_id: produto.id,
    };
  }

  return {
    acao: "IGNORADO",
    mensagem: "Produto ignorado porque a atualização recebida não é mais recente.",
    produto_id: produto.id,
  };
}

async function consultarProdutos(filtros = {}) {
  /**
   * Consulta produtos cadastrados no catálogo.
   *
   * @param {object} filtros - Filtros opcionais da consulta
   * @returns {Promise<Array>} Lista de produtos
   */

  return listarProdutos(filtros);
}

async function consultarProdutoPorId(id) {
  /**
   * Consulta um produto pelo ID.
   *
   * @param {string} id - ID do produto
   * @returns {Promise<object|null>} Produto encontrado ou null
   */

  return buscarProdutoCompletoPorId(id);
}

async function vincularImagemProduto(id, imagemUrl) {
  /**
   * Vincula uma URL de imagem a um produto.
   *
   * @param {string} id - ID do produto
   * @param {string} imagemUrl - URL da imagem
   * @returns {Promise<object>} Produto atualizado
   */

  if (!id || !imagemUrl) {
    throw new Error("ID do produto e URL da imagem são obrigatórios.");
  }

  const produtoAtualizado = await atualizarImagemProduto(id, imagemUrl);

  if (!produtoAtualizado) {
    throw new Error("Produto não encontrado.");
  }

  return produtoAtualizado;
}

module.exports = {
  salvarOuAtualizarProduto,
  consultarProdutos,
  consultarProdutoPorId,
  vincularImagemProduto,
};