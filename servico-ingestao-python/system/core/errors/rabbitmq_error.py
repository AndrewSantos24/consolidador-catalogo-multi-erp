from system.core.errors.app_error import AppError


class RabbitMQError(AppError):
    """Representa um erro de comunicação com o RabbitMQ."""

    def __init__(self) -> None:
        """Inicializa o erro de indisponibilidade do RabbitMQ."""

        super().__init__(
            mensagem=(
                "Não foi possível conectar ao RabbitMQ. "
                "Verifique se o container está rodando e se as configurações estão corretas."
            ),
            status_code=503,
        )