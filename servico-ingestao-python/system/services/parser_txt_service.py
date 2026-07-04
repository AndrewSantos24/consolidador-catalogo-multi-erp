import re
from datetime import datetime

from system.schemas.produto_schema import ProdutoNormalizado


def converter_valor_txt_para_float(valor: str) -> float:
    """Converte um valor monetário do TXT para float.

    :param str valor: Valor monetário em texto sem separador decimal
    :return: Valor convertido para float
    """

    valor_limpo = valor.strip()

    if not valor_limpo:
        return 0.0

    return int(valor_limpo) / 100


def converter_data_txt_para_datetime(valor: str) -> datetime:
    """Converte uma data do TXT para datetime.

    :param str valor: Data no formato YYYYMMDDHHMMSS
    :return: Data convertida para datetime
    """

    valor_limpo = valor.strip()

    return datetime.strptime(valor_limpo, "%Y%m%d%H%M%S")


def separar_sku_e_nome(valor: str) -> tuple[str, str]:
    """Separa o SKU e o nome do produto no trecho inicial do TXT.

    :param str valor: Texto contendo SKU e nome juntos
    :return: Tupla contendo SKU e nome
    """

    valor_limpo = valor.strip()

    resultado = re.match(
        r"^(?P<sku>[A-Z0-9-]+)\s*(?P<nome>[A-ZÁ-Ú][a-zá-ú].*)$",
        valor_limpo,
    )

    if not resultado:
        return valor_limpo, ""

    sku = resultado.group("sku").strip()
    nome = resultado.group("nome").strip()

    return sku, nome


def extrair_campos_linha_txt(linha: str) -> dict[str, str]:
    """Extrai os campos de uma linha TXT enviada pelo ERP.

    :param str linha: Linha do TXT em formato textual
    :return: Dicionário com os campos extraídos
    """

    resultado = re.match(
        r"^(?P<inicio>.*?)(?P<preco_lista>\d{10})(?P<preco_desconto>\d{10})(?P<categoria>[A-ZÇÃÉÍÓÚ ]+?)(?P<atualizado_em>\d{14})$",
        linha,
    )

    if not resultado:
        raise ValueError(f"Linha TXT inválida: {linha}")

    campos = resultado.groupdict()

    inicio = campos["inicio"]
    id_produto = inicio[0:10].strip().lstrip("0")
    sku, nome = separar_sku_e_nome(inicio[10:])

    return {
        "id": id_produto,
        "sku": sku,
        "nome": nome,
        "preco_lista": campos["preco_lista"],
        "preco_desconto": campos["preco_desconto"],
        "categoria": campos["categoria"].strip(),
        "atualizado_em": campos["atualizado_em"],
    }


def converter_linha_txt_para_produto(linha: str) -> ProdutoNormalizado:
    """Converte uma linha TXT do ERP para ProdutoNormalizado.

    :param str linha: Linha do TXT em formato textual
    :return: Produto no formato padrão da aplicação
    """

    campos = extrair_campos_linha_txt(linha)

    return ProdutoNormalizado(
        id=campos["id"],
        sku=campos["sku"],
        nome=campos["nome"],
        preco_lista=converter_valor_txt_para_float(campos["preco_lista"]),
        preco_desconto=converter_valor_txt_para_float(campos["preco_desconto"]),
        categoria=campos["categoria"],
        atualizado_em=converter_data_txt_para_datetime(campos["atualizado_em"]),
    )


def normalizar_produtos_txt(payload_txt: str) -> list[ProdutoNormalizado]:
    """Normaliza uma lista de produtos recebida via payload TXT.

    :param str payload_txt: Payload TXT enviado pelo ERP
    :return: Lista de produtos normalizados
    """

    linhas = payload_txt.splitlines()

    return [
        converter_linha_txt_para_produto(linha)
        for linha in linhas
        if linha.strip()
    ]