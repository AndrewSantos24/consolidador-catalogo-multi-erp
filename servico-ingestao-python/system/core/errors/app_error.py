class AppError(Exception):
    """Representa um erro esperado da aplicação.

    :param str mensagem: Mensagem amigável do erro
    :param int status_code: Código HTTP relacionado ao erro
    """

    def __init__(self, mensagem: str, status_code: int = 400) -> None:
        """Inicializa o erro da aplicação.

        :param str mensagem: Mensagem amigável do erro
        :param int status_code: Código HTTP relacionado ao erro
        """

        self.mensagem = mensagem
        self.status_code = status_code

        super().__init__(mensagem)