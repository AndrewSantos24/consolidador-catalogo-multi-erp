from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from system.services.parser_json_service import normalizar_produtos_json
from system.services.parser_txt_service import normalizar_produtos_txt
from system.services.parser_xml_service import normalizar_produtos_xml


router = APIRouter(prefix="/ingestao", tags=["Ingestão"])


@router.post("/json")
def receber_produtos_json(payload: dict = Body(...)) -> dict:
    """Recebe produtos em JSON e retorna os produtos normalizados.

    Exemplo de payload recebido:

    {

        "items": [
            {
                "productCode": "A-778",
                "skuCode": "NB-DELL-INS-15",
                "description": "Notebook Dell Inspiron 15",
                "value": 3500.90,
                "discountValue": 3200.00,
                "department": "TI",
                "updated_at": "2026-01-10T10:14:30Z"
            }
        ]

    }

    :param dict payload: Payload JSON enviado pelo ERP
    :return: Quantidade e lista de produtos normalizados
    """

    produtos = normalizar_produtos_json(payload)

    return {
        "mensagem": "Produtos JSON normalizados com sucesso.",
        "quantidade": len(produtos),
        "produtos": jsonable_encoder(produtos),
    }


@router.post("/xml")
def receber_produtos_xml(payload_xml: str = Body(..., media_type="application/xml")) -> dict:
    """Recebe produtos em XML e retorna os produtos normalizados.

    Exemplo de payload recebido:


    <products>
        <product>
            <id>1001</id>
            <sku>NB-DELL-INS-15</sku>
            <name>Notebook Dell Inspiron 15</name>
            <price>
                <list>3500.90</list>
                <discount>3200.00</discount>
            </price>
            <category>Informática</category>
            <lastUpdate>2026-01-10T10:15:00</lastUpdate>
        </product>
    </products>
    

    :param str payload_xml: Payload XML enviado pelo ERP
    :return: Quantidade e lista de produtos normalizados
    """

    produtos = normalizar_produtos_xml(payload_xml)

    return {
        "mensagem": "Produtos XML normalizados com sucesso.",
        "quantidade": len(produtos),
        "produtos": jsonable_encoder(produtos),
    }


@router.post("/txt")
def receber_produtos_txt(payload_txt: str = Body(..., media_type="text/plain")) -> dict:
    """Recebe produtos em TXT e retorna os produtos normalizados.

    Exemplo de payload recebido:

    0000001001NB-DELL-INS-15Notebook Dell Inspiron 15        00003500900000320000INFORMATICA       20260110101500

    Layout esperado:

    - ID no início da linha
    - SKU e nome no trecho inicial
    - preço lista com 10 dígitos
    - preço desconto com 10 dígitos
    - categoria em texto
    - data final no formato YYYYMMDDHHMMSS

    :param str payload_txt: Payload TXT enviado pelo ERP
    :return: Quantidade e lista de produtos normalizados
    """

    produtos = normalizar_produtos_txt(payload_txt)

    return {
        "mensagem": "Produtos TXT normalizados com sucesso.",
        "quantidade": len(produtos),
        "produtos": jsonable_encoder(produtos),
    }