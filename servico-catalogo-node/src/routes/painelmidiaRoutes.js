const express = require("express");
const path = require("path");

const {
  consultarProdutosSemImagem,
  vincularImagemProduto,
} = require("../services/produtoService");

const router = express.Router();

router.get("/painel-midias", (req, res) => {
  /**
   * Exibe um painel simples para vincular imagem a um produto.
   */

  const caminhoTemplate = path.join(
    __dirname,
    "..",
    "templates",
    "painelmidias.html"
  );

  return res.sendFile(caminhoTemplate);
});

router.get("/painel-midias/produtos-sem-imagem", async (req, res) => {
  /**
   * Exibe produtos que ainda não possuem imagem vinculada.
   */

  try {
    const produtos = await consultarProdutosSemImagem();

    let conteudoProdutos = "<p>Nenhum produto sem imagem encontrado.</p>";

    if (produtos.length > 0) {
      const linhasTabela = produtos
        .map((produto) => {
          return `
            <tr>
              <td>${produto.id}</td>
              <td>${produto.sku}</td>
              <td>${produto.nome}</td>
              <td>${produto.categoria}</td>
            </tr>
          `;
        })
        .join("");

      conteudoProdutos = `
        <table border="1" cellpadding="8" cellspacing="0">
          <thead>
            <tr>
              <th>ID</th>
              <th>SKU</th>
              <th>Nome</th>
              <th>Categoria</th>
            </tr>
          </thead>
          <tbody>
            ${linhasTabela}
          </tbody>
        </table>
      `;
    }

    return res.send(`
      <!DOCTYPE html>
      <html lang="pt-BR">
        <head>
          <meta charset="UTF-8" />
          <title>Produtos sem imagem</title>
        </head>
        <body>
          <h1>Produtos sem imagem</h1>

          <p>Copie o ID do produto e use no painel de mídias para vincular uma imagem.</p>

          ${conteudoProdutos}

          <br />

          <a href="/api/v1/painel-midias">Voltar para o painel</a>
        </body>
      </html>
    `);
  } catch (erro) {
    return res.status(500).send(`
      <!DOCTYPE html>
      <html lang="pt-BR">
        <head>
          <meta charset="UTF-8" />
          <title>Erro</title>
        </head>
        <body>
          <h1>Erro ao consultar produtos sem imagem</h1>

          <p>${erro.message}</p>

          <br />

          <a href="/api/v1/painel-midias">Voltar para o painel</a>
        </body>
      </html>
    `);
  }
});

router.post("/painel-midias", async (req, res) => {
  /**
   * Recebe os dados do formulário e vincula a imagem ao produto.
   */

  try {
    const { produto_id, imagem_url } = req.body;

    const produto = await vincularImagemProduto(produto_id, imagem_url);

    return res.send(`
    <!DOCTYPE html>
    <html lang="pt-BR">
        <head>
        <meta charset="UTF-8" />
        <title>Imagem vinculada</title>

        <style>
            * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            }

            body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;

            padding: 20px;
            }

            .container {
            width: 100%;
            max-width: 520px;
            background: #ffffff;
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            text-align: center;
            }

            .icone-sucesso {
            width: 64px;
            height: 64px;
            background: #dcfce7;
            color: #16a34a;
            border-radius: 50%;

            display: flex;
            justify-content: center;
            align-items: center;

            font-size: 34px;
            font-weight: bold;
            margin: 0 auto 18px;
            }

            h1 {
            color: #166534;
            font-size: 26px;
            margin-bottom: 12px;
            }

            .descricao {
            color: #6b7280;
            font-size: 15px;
            margin-bottom: 26px;
            }

            .dados-produto {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 18px;
            text-align: left;
            margin-bottom: 24px;
            }

            .dados-produto p {
            color: #374151;
            font-size: 15px;
            margin-bottom: 12px;
            word-break: break-word;
            }

            .dados-produto p:last-child {
            margin-bottom: 0;
            }

            .dados-produto strong {
            color: #111827;
            }

            .link-voltar {
            display: inline-block;
            width: 100%;
            padding: 13px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.2s, transform 0.1s;
            }

            .link-voltar:hover {
            background: #1d4ed8;
            }

            .link-voltar:active {
            transform: scale(0.98);
            }
        </style>
        </head>

        <body>
        <div class="container">
            <div class="icone-sucesso">✓</div>

            <h1>Imagem vinculada com sucesso!</h1>

            <p class="descricao">
            A imagem foi associada ao produto informado.
            </p>

            <div class="dados-produto">
            <p><strong>Produto:</strong> ${produto.nome}</p>
            <p><strong>ID:</strong> ${produto.id}</p>
            <p><strong>Imagem:</strong> ${produto.imagem_url}</p>
            </div>

            <a class="link-voltar" href="/api/v1/painel-midias">
            Voltar para o painel
            </a>
        </div>
        </body>
    </html>
`);
  } catch (erro) {
  return res.status(400).send(`
    <!DOCTYPE html>
    <html lang="pt-BR">
      <head>
        <meta charset="UTF-8" />
        <title>Erro ao vincular imagem</title>

        <style>
          * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
          }

          body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;

            padding: 20px;
          }

          .container {
            width: 100%;
            max-width: 520px;
            background: #ffffff;
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            text-align: center;
          }

          .icone-erro {
            width: 64px;
            height: 64px;
            background: #fee2e2;
            color: #dc2626;
            border-radius: 50%;

            display: flex;
            justify-content: center;
            align-items: center;

            font-size: 34px;
            font-weight: bold;
            margin: 0 auto 18px;
          }

          h1 {
            color: #991b1b;
            font-size: 26px;
            margin-bottom: 12px;
          }

          .descricao {
            color: #6b7280;
            font-size: 15px;
            margin-bottom: 20px;
          }

          .mensagem-erro {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #7f1d1d;
            border-radius: 10px;
            padding: 16px;
            text-align: left;
            margin-bottom: 24px;
            word-break: break-word;
          }

          .mensagem-erro strong {
            display: block;
            margin-bottom: 8px;
          }

          .link-voltar {
            display: inline-block;
            width: 100%;
            padding: 13px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.2s, transform 0.1s;
          }

          .link-voltar:hover {
            background: #1d4ed8;
          }

          .link-voltar:active {
            transform: scale(0.98);
          }
        </style>
      </head>

      <body>
        <div class="container">
          <div class="icone-erro">!</div>

          <h1>Erro ao vincular imagem</h1>

          <p class="descricao">
            Não foi possível associar a imagem ao produto informado.
          </p>

          <div class="mensagem-erro">
            <strong>Detalhes do erro:</strong>
            ${erro.message}
          </div>

          <a class="link-voltar" href="/api/v1/painel-midias">
            Voltar para o painel
          </a>
        </div>
      </body>
    </html>
  `);
  }
});

module.exports = router;