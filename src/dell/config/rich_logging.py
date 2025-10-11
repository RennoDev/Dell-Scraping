import logging

from rich.theme import Theme

# Tema customizado para diferentes tipos de log
RICH_THEME = Theme(
    {
        "logging.level.debug": "dim blue",
        "logging.level.info": "green",
        "logging.level.warning": "yellow",
        "logging.level.error": "red",
        "logging.level.critical": "bold red on white",
        "logging.keyword": "bold magenta",
        "logging.string": "green",
        "logging.number": "blue",
    }
)

# Mapeamento de ícones por nível
LOG_ICONS = {
    "DEBUG": "🔍",
    "INFO": "ℹ️ ",
    "WARNING": "⚠️ ",
    "ERROR": "❌",
    "CRITICAL": "🚨",
}

# Configurações por ambiente
RICH_CONFIG = {
    "development": {
        "console_level": "DEBUG",
        "file_level": "DEBUG",
        "show_time": True,
        "show_path": True,
        "rich_tracebacks": True,
        "markup": True,
        "highlighter": True,
    },
    "production": {
        "console_level": "INFO",
        "file_level": "DEBUG",
        "show_time": False,
        "show_path": False,
        "rich_tracebacks": False,
        "markup": False,
        "highlighter": False,
    },
}


class RichFormatter(logging.Formatter):
    """
    Formatter customizado que adiciona ícones aos logs.
    """

    def format(self, record):
        # Adicionar ícone baseado no level
        icon = LOG_ICONS.get(record.levelname, "📝")

        # Personalizar mensagem baseada no módulo
        if "browser" in record.name:
            icon = "🌐" if record.levelname == "INFO" else icon
        elif "pace" in record.name:
            icon = "⚡" if record.levelname == "INFO" else icon
        elif "workflow" in record.name:
            icon = "🔄" if record.levelname == "INFO" else icon
        elif "database" in record.name:
            icon = "🗄️" if record.levelname == "INFO" else icon

        # Formatear mensagem com ícone
        record.msg = f"{icon} {record.msg}"

        return super().format(record)


def setup_rich_logging(
    environment: str = "development",
    console_output: bool = True,
    file_output: bool = True,
    log_file: Optional[str] = None,
) -> Console:
    """
    Configura sistema de logging bonito com Rich.

    Args:
        environment: 'development' ou 'production'
        console_output: Se deve mostrar logs no terminal
        file_output: Se deve salvar logs em arquivo
        log_file: Caminho do arquivo de log (opcional)

    Returns:
        Console: Instância do Rich Console configurada
    """

    # Obter configuração do ambiente
    config = RICH_CONFIG.get(environment, RICH_CONFIG["development"])

    # Criar console com tema personalizado
    console = Console(
        theme=RICH_THEME,
        force_terminal=True,  # Força cores mesmo se redirected
        width=120,  # Largura consistente
    )

    # Instalar tracebacks bonitos (se habilitado)
    if config["rich_tracebacks"]:
        install_rich_traceback(
            console=console, show_locals=environment == "development"
        )

    # Limpar handlers existentes para evitar duplicação
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Configurar handler do console (se habilitado)
    if console_output:
        console_handler = RichHandler(
            console=console,
            level=getattr(logging, config["console_level"]),
            rich_tracebacks=config["rich_tracebacks"],
            markup=config["markup"],
            show_time=config["show_time"],
            show_path=config["show_path"],
            highlighter=None if not config["highlighter"] else RichHandler._highlighter,
        )

        # Aplicar formatter customizado
        console_handler.setFormatter(RichFormatter())
        root_logger.addHandler(console_handler)

    # Configurar handler de arquivo (se habilitado)
    if file_output:
        file_path = log_file or "logs/debug/rich_app.log"

        # Handler de arquivo SEM Rich (para compatibilidade)
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, config["file_level"]))

        # Formatter simples para arquivo
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Configurar nível do logger raiz
    root_logger.setLevel(logging.DEBUG)

    return console


def get_rich_console() -> Console:
    """
    Retorna instância do Rich Console para uso em outros módulos.

    Por que essa função?
    - Reutilizar a mesma instância configurada
    - Consistência visual em todo projeto
    - Evitar reconfiguração desnecessária
    """
    return Console(theme=RICH_THEME)


# Função de conveniência para configuração rápida
def quick_setup(environment: str = "development") -> None:
    """
    Configuração rápida com padrões sensatos.

    Para usar no início da aplicação:
    >>> from dell.config.rich_logging import quick_setup
    >>> quick_setup("development")
    """
    setup_rich_logging(environment)


# Decorator para logs automáticos de função
def log_function_calls(level: str = "DEBUG"):
    """
    Decorator que automaticamente loga entrada/saída de funções.

    Uso:
    >>> @log_function_calls("INFO")
    >>> async def scrape_dell():
    >>>     pass
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            logger.log(getattr(logging, level), f"🔄 Iniciando {func.__name__}")

            try:
                result = func(*args, **kwargs)
                logger.log(getattr(logging, level), f"✅ Concluído {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"❌ Falha em {func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator
