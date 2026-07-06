const amqp = require("amqplib");

const env = require("../config/env");

async function iniciarConsumerProdutos() {
  /**
   * Inicia o consumer de produtos normalizados no RabbitMQ.
   *
   * O consumer fica escutando a fila de produtos normalizados.
   * Quando uma mensagem chega, ela é convertida de JSON para objeto.
   */

  try {
    const conexao = await amqp.connect(env.rabbitmqUrl);
    const canal = await conexao.createChannel();

    await canal.assertQueue(env.rabbitmqFilaProdutos, {
      durable: true,
    });

    console.log(`Escutando fila: ${env.rabbitmqFilaProdutos}`);

    canal.consume(env.rabbitmqFilaProdutos, async (mensagem) => {
        if (!mensagem) {
          return;
        }

        try {
          const conteudo = mensagem.content.toString("utf-8");
          const produto = JSON.parse(conteudo);

          console.log("Produto recebido da fila:");
          console.log(produto);

          canal.ack(mensagem);
        } catch (erro) {
          console.error("Erro ao processar mensagem da fila:", erro.message);

          canal.nack(mensagem, false, false);
        }
      },
      {
        consumerTag: "servico-catalogo-node-produtos",
      }
    );
  } catch (erro) {
    console.error("Erro ao conectar no RabbitMQ:", erro.message);
  }
}

module.exports = {
  iniciarConsumerProdutos,
};