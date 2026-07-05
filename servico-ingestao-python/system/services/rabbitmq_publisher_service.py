import json

import pika

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


def publicar_produto_normalizado(produto: ProdutoNormalizado) -> None:
    """Publica um produto normalizado na fila do RabbitMQ.

    :param ProdutoNormalizado produto: Produto normalizado que será publicado
    """

    conexao = criar_conexao_rabbitmq()
    canal = conexao.channel()

    canal.queue_declare(
        queue=configuracoes.rabbitmq_fila_produtos,
        durable=True,
    )

    mensagem = json.dumps(
        produto.model_dump(mode="json"),
        ensure_ascii=False,
    )

    canal.basic_publish(
        exchange="",
        routing_key=configuracoes.rabbitmq_fila_produtos,
        body=mensagem.encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json",
        ),
    )

    conexao.close()


def publicar_produtos_normalizados(produtos: list[ProdutoNormalizado]) -> int:
    """Publica uma lista de produtos normalizados na fila do RabbitMQ.

    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :return: Quantidade de produtos publicados
    """

    for produto in produtos:
        publicar_produto_normalizado(produto)

    return len(produtos)