"""
Exemplo de uso do Sistema de Logging Contextual.
Demonstra como logs de sucesso e erro são automaticamente separados.
"""

import logging

from dell.config.rich_logging import setup_rich_logging

# Configurar sistema de logging
setup_rich_logging("development")

# Obter logger para este módulo
logger = logging.getLogger(__name__)


def exemplo_logs_sucesso():
    """
    Exemplo de logs que vão para logs/success/success_dd.MM.yyyy_hh.mm.log
    """
    logger.info("🚀 Iniciando exemplo de logs de sucesso")
    logger.info("📊 Processando dados...")
    logger.info("✅ Operação concluída com sucesso")
    logger.info("📈 Estatísticas: 150 itens processados")


def exemplo_logs_erro():
    """
    Exemplo de logs que vão para logs/failed/failed_dd.MM.yyyy_hh.mm.log
    """
    logger.error("❌ Erro de conexão com o banco de dados")
    logger.error("🚨 Falha crítica no sistema")
    logger.error("⚠️ Timeout na operação de rede")


def exemplo_mixed_logs():
    """
    Exemplo mostrando como logs da mesma execução são separados automaticamente.
    """
    # Este vai para success
    logger.info("🔄 Iniciando operação complexa")

    try:
        # Simular algum processamento
        logger.info("📁 Processando arquivo 1/3")
        logger.info("📁 Processando arquivo 2/3")

        # Simular um erro
        raise ValueError("Erro simulado no arquivo 3")

    except Exception as e:
        # Este vai para failed
        logger.error(f"❌ Erro ao processar arquivo 3: {str(e)}")
        logger.error("🔄 Tentando recuperação...")

        try:
            # Simular recuperação
            logger.info("✅ Recuperação bem-sucedida")  # Volta para success

        except Exception as recovery_error:
            logger.error(f"🚨 Falha na recuperação: {str(recovery_error)}")  # failed


if __name__ == "__main__":
    print("🎯 Testando Sistema de Logging Contextual")
    print("📁 Verifique os arquivos em logs/success/ e logs/failed/")
    print()

    exemplo_logs_sucesso()
    print("✅ Logs de sucesso gerados")

    exemplo_logs_erro()
    print("❌ Logs de erro gerados")

    exemplo_mixed_logs()
    print("🔄 Logs mistos gerados")

    print()
    print("🎉 Teste concluído! Verifique os arquivos:")
    print("📁 logs/success/success_DD.MM.YYYY_HH.MM.log")
    print("📁 logs/failed/failed_DD.MM.YYYY_HH.MM.log")
