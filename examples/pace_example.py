"""
Exemplo de uso do Sistema de Pace Global.
Demonstra como controlar a velocidade da aplicação de forma inteligente.
"""

import asyncio
import logging

from dell.browser import (
    PaceLevel,
    TemporaryPace,
    browser_manager,
    configure_pace,
    extract_text,
    pace_manager,
    safe_click,
    safe_goto,
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def exemplo_pace_basico():
    """
    Exemplo básico: diferentes níveis de pace.
    """
    logger.info("=== Exemplo de Pace Básico ===")

    # Configurar pace para modo CAREFUL (muito cuidadoso)
    configure_pace(PaceLevel.CAREFUL)

    async with browser_manager as bm:
        page = await bm.get_page("pace_example", "production")

        logger.info("🐌 Navegando com pace CAREFUL (lento e seguro)")
        await safe_goto(page, "https://httpbin.org/html")

        # Extrair título - vai usar timing de extração do pace
        title = await extract_text(page, "h1")
        logger.info(f"Título extraído: {title}")


async def exemplo_pace_dinamico():
    """
    Demonstra mudança dinâmica de pace durante execução.
    """
    logger.info("=== Exemplo de Pace Dinâmico ===")

    async with browser_manager as bm:
        page = await bm.get_page("dynamic_pace", "production")

        # Começar no modo NORMAL
        configure_pace(PaceLevel.NORMAL)
        logger.info("⚡ Iniciando com pace NORMAL")
        await safe_goto(page, "https://httpbin.org/forms/post")

        # Mudar para DEBUG para análise detalhada
        configure_pace(PaceLevel.DEBUG)
        logger.info("🔍 Mudando para pace DEBUG (muito lento para análise)")

        # Simular interações com timing debug
        try:
            await safe_click(page, "input[name='custname']")
            logger.info("✅ Clique executado com timing DEBUG")
        except Exception as e:
            logger.warning(f"Elemento não encontrado: {e}")

        # Voltar para TURBO para operações rápidas
        configure_pace(PaceLevel.TURBO)
        logger.info("🚀 Mudando para pace TURBO (máxima velocidade)")


async def exemplo_pace_temporario():
    """
    Demonstra uso de pace temporário com context manager.
    """
    logger.info("=== Exemplo de Pace Temporário ===")

    # Configurar pace global como NORMAL
    configure_pace(PaceLevel.NORMAL)

    async with browser_manager as bm:
        page = await bm.get_page("temp_pace", "production")

        logger.info("⚡ Operação com pace NORMAL")
        await safe_goto(page, "https://httpbin.org/json")

        # Usar pace temporário STEALTH para operação específica
        async with TemporaryPace(PaceLevel.STEALTH):
            logger.info("🥷 Entrando em modo STEALTH temporário")

            content = await extract_text(page, "body")
            logger.info(f"Conteúdo extraído em modo stealth: {len(content)} chars")

            # Aqui dentro, tudo usa timing STEALTH

        logger.info("⚡ Voltou automaticamente para pace NORMAL")

        # Verificar que voltou ao pace original
        stats = pace_manager.get_statistics()
        logger.info(f"Pace atual: {stats['pace_level']}")


async def exemplo_pace_com_multiplicador():
    """
    Demonstra uso de multiplicador para ajuste fino.
    """
    logger.info("=== Exemplo de Multiplicador de Pace ===")

    async with browser_manager as bm:
        page = await bm.get_page("multiplier_pace", "production")

        # Pace NORMAL padrão
        configure_pace(PaceLevel.NORMAL, multiplier=1.0)
        logger.info("⚡ Pace NORMAL com multiplicador 1.0x")
        await safe_goto(page, "https://httpbin.org/xml")

        # Pace NORMAL mais lento (2x)
        configure_pace(PaceLevel.NORMAL, multiplier=2.0)
        logger.info("🐌 Pace NORMAL com multiplicador 2.0x (dobro do tempo)")

        content = await extract_text(page, "body")
        logger.info(f"Conteúdo: {content[:100]}...")

        # Pace NORMAL mais rápido (0.5x)
        configure_pace(PaceLevel.NORMAL, multiplier=0.5)
        logger.info("🚀 Pace NORMAL com multiplicador 0.5x (metade do tempo)")


async def exemplo_estatisticas_pace():
    """
    Demonstra coleta de estatísticas de uso do pace.
    """
    logger.info("=== Exemplo de Estatísticas de Pace ===")

    # Resetar estatísticas
    pace_manager.reset_statistics()
    configure_pace(PaceLevel.NORMAL)

    async with browser_manager as bm:
        page = await bm.get_page("stats_pace", "production")

        # Executar várias operações
        await safe_goto(page, "https://httpbin.org/html")
        await extract_text(page, "h1")
        await extract_text(page, "p")

        try:
            await safe_click(page, "a")  # Pode não existir
        except:
            pass

        # Obter estatísticas
        stats = pace_manager.get_statistics()

        logger.info("📊 Estatísticas de Pace:")
        logger.info(f"   Nível atual: {stats['pace_level']}")
        logger.info(f"   Multiplicador: {stats['multiplier']}x")
        logger.info(f"   Total de operações: {stats['total_operations']}")

        logger.info("📈 Operações por tipo:")
        for op_type, count in stats["operations_by_type"].items():
            if count > 0:
                logger.info(f"   {op_type}: {count} vezes")

        logger.info("⏰ Delays atuais:")
        for op_type, delay in stats["current_delays"].items():
            logger.info(f"   {op_type}: {delay:.2f}s")


async def exemplo_comparacao_velocidades():
    """
    Compara diferentes níveis de pace cronometrando execução.
    """
    import time

    logger.info("=== Comparação de Velocidades ===")

    async def medir_tempo(pace_level: PaceLevel, descricao: str):
        """Helper para medir tempo de execução."""
        configure_pace(pace_level)

        start_time = time.time()

        async with browser_manager as bm:
            page = await bm.get_page(f"speed_test_{pace_level.value}", "production")
            await safe_goto(page, "https://httpbin.org/json")
            await extract_text(page, "body")

        elapsed = time.time() - start_time
        logger.info(f"⏱️  {descricao}: {elapsed:.2f}s")
        return elapsed

    # Testar diferentes velocidades
    turbo_time = await medir_tempo(PaceLevel.TURBO, "TURBO (máxima velocidade)")
    normal_time = await medir_tempo(PaceLevel.NORMAL, "NORMAL (padrão)")
    careful_time = await medir_tempo(PaceLevel.CAREFUL, "CAREFUL (cuidadoso)")

    # Comparar resultados
    logger.info("📊 Comparação de Performance:")
    logger.info(f"   TURBO vs NORMAL: {normal_time / turbo_time:.1f}x mais lento")
    logger.info(f"   NORMAL vs CAREFUL: {careful_time / normal_time:.1f}x mais lento")
    logger.info(f"   TURBO vs CAREFUL: {careful_time / turbo_time:.1f}x mais lento")


async def main():
    """
    Executa todos os exemplos do sistema de pace.
    """
    logger.info("🎯 Iniciando exemplos do Sistema de Pace Global")

    try:
        await exemplo_pace_basico()
        await asyncio.sleep(1)

        await exemplo_pace_dinamico()
        await asyncio.sleep(1)

        await exemplo_pace_temporario()
        await asyncio.sleep(1)

        await exemplo_pace_com_multiplicador()
        await asyncio.sleep(1)

        await exemplo_estatisticas_pace()
        await asyncio.sleep(1)

        await exemplo_comparacao_velocidades()

    except Exception as e:
        logger.error(f"Erro durante execução: {str(e)}")

    logger.info("✅ Exemplos de pace concluídos")


if __name__ == "__main__":
    # Executar exemplos
    asyncio.run(main())
