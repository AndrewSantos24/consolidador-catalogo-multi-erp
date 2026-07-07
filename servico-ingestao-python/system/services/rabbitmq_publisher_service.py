import json

import pika
from pika.exceptions import AMQPConnectionError
from system.core.errors import RabbitMQError

from system.core.config import configuracoes
from system.schemas.produto_schema import ProdutoNormalizado


def criar_conexao_rabbitmq() -> pika.BlockingConnection:
    """Cria uma conexão com o RabbitMQ.

    :return: Conexão ativa com o RabbitMQ
    """

    credenciais = pika.PlainCredentials(
        username=configuracoes.rabbitmq_usuario,
        password=configuracoes.rabbitmq_senha,
    )

    parametros = pika.ConnectionParameters(
        host=configuracoes.rabbitmq_host,
        port=configuracoes.rabbitmq_porta,
        credentials=credenciais,
    )

    return pika.BlockingConnection(parametros)


def converter_produto_para_mensagem(produto: ProdutoNormalizado) -> bytes:
    """Converte um produto normalizado para mensagem JSON em bytes.

    :param ProdutoNormalizado produto: Produto normalizado que será convertido
    :return: Mensagem JSON em bytes
    """

    mensagem = json.dumps(
        produto.model_dump(mode="json"),
        ensure_ascii=False,
    )

    return mensagem.encode("utf-8")


def publicar_produtos_normalizados(produtos: list[ProdutoNormalizado]) -> int:
    """Publica uma lista de produtos normalizados na fila do RabbitMQ.

    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :return: Quantidade de produtos publicados
    """

    conexao = criar_conexao_rabbitmq()

    try:
        canal = conexao.channel()

        canal.queue_declare(
            queue=configuracoes.rabbitmq_fila_produtos,
            durable=True,
        )

        for produto in produtos:
            mensagem = converter_produto_para_mensagem(produto)

            canal.basic_publish(
                exchange="",
                routing_key=configuracoes.rabbitmq_fila_produtos,
                body=mensagem,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                ),
            )

        return len(produtos)

    finally:
        if conexao and conexao.is_open:
            conexao.close()


def publicar_produtos_rbmq(produtos: list[ProdutoNormalizado]) -> int:
    """Publica produtos normalizados tratando falhas de conexão com RabbitMQ.

    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :return: Quantidade de produtos publicados
    :raises RuntimeError: Quando não for possível conectar ao RabbitMQ
    """

    try:
        return publicar_produtos_normalizados(produtos)

    except AMQPConnectionError as erro:
        raise RabbitMQError() from erro