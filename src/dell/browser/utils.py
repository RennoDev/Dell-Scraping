import asyncio
import logging
from typing import Any, Dict, Optional

from playwright.async_api import ElementHandle, Page

from .pace_manager import (
    wait_click,
    wait_fill,
    wait_scroll,
)

logger = logging.getLogger(__name__)


class PageWaitTimeout(Exception):
    """Exceção customizada para timeouts de espera."""

    pass


class ElementNotFoundError(Exception):
    """Exceção para elementos não encontrados."""

    pass


async def safe_goto(
    page: Page,
    url: str,
    wait_until: str = "networkidle",
    timeout: float = 30000,
    max_retries: int = 3,
) -> bool:
    """
    Navega para URL com retry automático e tratamento de erros.

    Args:
        page: Página do Playwright
        url: URL de destino
        wait_until: Estratégia de espera ('load', 'networkidle', 'commit')
        timeout: Timeout em ms
        max_retries: Máximo de tentativas

    Returns:
        bool: True se navegação foi bem-sucedida

    Raises:
        PageWaitTimeout: Se timeout for atingido
    """
    for attempt in range(max_retries):
        try:
            logger.debug(f"Navegando para {url} (tentativa {attempt + 1})")

            response = await page.goto(url, wait_until=wait_until, timeout=timeout)

            if response and response.status < 400:
                logger.info(f"Navegação bem-sucedida para {url}")
                return True

            logger.warning(
                f"Resposta HTTP {response.status if response else 'None'} para {url}"
            )

        except Exception as e:
            logger.warning(f"Tentativa {attempt + 1} falhou: {str(e)}")
            if attempt == max_retries - 1:
                raise PageWaitTimeout(
                    f"Falha na navegação após {max_retries} tentativas: {str(e)}"
                )
            await asyncio.sleep(2**attempt)  # Backoff exponencial

    return False


async def wait_for_element(
    page: Page, selector: str, timeout: float = 10000, state: str = "visible"
) -> Optional[ElementHandle]:
    """
    Espera por elemento com timeout customizado.

    Args:
        page: Página do Playwright
        selector: Seletor CSS/XPath
        timeout: Timeout em ms
        state: Estado desejado ('visible', 'attached', 'detached', 'hidden')

    Returns:
        ElementHandle ou None se não encontrado

    Raises:
        ElementNotFoundError: Se elemento não for encontrado no tempo
    """
    try:
        logger.debug(f"Aguardando elemento: {selector} (state: {state})")

        await page.wait_for_selector(selector, timeout=timeout, state=state)

        element = await page.query_selector(selector)
        if element:
            logger.debug(f"Elemento encontrado: {selector}")
            return element

    except Exception as e:
        logger.error(f"Elemento não encontrado '{selector}': {str(e)}")
        raise ElementNotFoundError(f"Elemento '{selector}' não encontrado: {str(e)}")

    return None


async def safe_click(
    page: Page,
    selector: str,
    timeout: float = 10000,
    force: bool = False,
    wait_after: float = 1.0,
) -> bool:
    """
    Clique seguro com validações e retry.

    Args:
        page: Página do Playwright
        selector: Seletor do elemento
        timeout: Timeout para encontrar elemento
        force: Forçar clique mesmo se elemento não estiver visível
        wait_after: Espera após clique (segundos)

    Returns:
        bool: True se clique foi bem-sucedido
    """
    try:
        # Aguardar elemento estar disponível
        element = await wait_for_element(page, selector, timeout)
        if not element:
            return False

        # Scroll para elemento se necessário
        await element.scroll_into_view_if_needed()

        # Executar clique
        await element.click(force=force)
        logger.debug(f"Clique executado: {selector}")

        # Aguardar após clique usando pace inteligente
        if wait_after > 0:
            await wait_click(f"Pós-clique em {selector}")
        else:
            await wait_click(f"Clique em {selector}")

        return True

    except Exception as e:
        logger.error(f"Erro no clique '{selector}': {str(e)}")
        return False


async def safe_fill(
    page: Page,
    selector: str,
    value: str,
    clear_first: bool = True,
    timeout: float = 10000,
) -> bool:
    """
    Preenchimento seguro de campo de texto.

    Args:
        page: Página do Playwright
        selector: Seletor do campo
        value: Valor a preencher
        clear_first: Limpar campo antes de preencher
        timeout: Timeout para encontrar elemento

    Returns:
        bool: True se preenchimento foi bem-sucedido
    """
    try:
        element = await wait_for_element(page, selector, timeout)
        if not element:
            return False

        # Limpar campo se solicitado
        if clear_first:
            await element.fill("")

        # Preencher valor
        await element.fill(value)
        logger.debug(f"Campo preenchido: {selector} = '{value[:50]}...'")

        # Aguardar após preenchimento
        await wait_fill(f"Preenchimento de {selector}")

        return True

    except Exception as e:
        logger.error(f"Erro ao preencher '{selector}': {str(e)}")
        return False


async def extract_text(
    page: Page, selector: str, timeout: float = 5000, default: str = ""
) -> str:
    """
    Extrai texto de elemento com fallback.

    Args:
        page: Página do Playwright
        selector: Seletor do elemento
        timeout: Timeout para encontrar elemento
        default: Valor padrão se elemento não encontrado

    Returns:
        str: Texto extraído ou valor padrão
    """
    try:
        element = await page.wait_for_selector(selector, timeout=timeout)
        if element:
            text = await element.text_content()
            return text.strip() if text else default

    except Exception as e:
        logger.debug(f"Texto não encontrado '{selector}': {str(e)}")

    return default


async def extract_attribute(
    page: Page, selector: str, attribute: str, timeout: float = 5000, default: str = ""
) -> str:
    """
    Extrai atributo de elemento.

    Args:
        page: Página do Playwright
        selector: Seletor do elemento
        attribute: Nome do atributo
        timeout: Timeout para encontrar elemento
        default: Valor padrão se não encontrado

    Returns:
        str: Valor do atributo ou padrão
    """
    try:
        element = await page.wait_for_selector(selector, timeout=timeout)
        if element:
            value = await element.get_attribute(attribute)
            return value or default

    except Exception as e:
        logger.debug(f"Atributo não encontrado '{selector}.{attribute}': {str(e)}")

    return default


async def scroll_to_bottom(
    page: Page, delay: float = 1.0, max_scrolls: int = 10
) -> None:
    """
    Scroll até o final da página com controle de velocidade.

    Args:
        page: Página do Playwright
        delay: Delay entre scrolls
        max_scrolls: Máximo de scrolls para evitar loop infinito
    """
    try:
        logger.debug("Iniciando scroll até o final da página")

        for i in range(max_scrolls):
            # Obter altura atual
            prev_height = await page.evaluate("document.body.scrollHeight")

            # Scroll para baixo
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # Aguardar carregamento com pace inteligente
            await wait_scroll(f"Scroll {i + 1}/{max_scrolls}")

            # Verificar se altura mudou (novo conteúdo carregou)
            new_height = await page.evaluate("document.body.scrollHeight")

            if new_height == prev_height:
                logger.debug(f"Final da página atingido após {i + 1} scrolls")
                break

        logger.debug("Scroll concluído")

    except Exception as e:
        logger.error(f"Erro durante scroll: {str(e)}")


async def take_screenshot(
    page: Page, path: str, full_page: bool = True, quality: Optional[int] = 80
) -> bool:
    """
    Captura screenshot da página.

    Args:
        page: Página do Playwright
        path: Caminho do arquivo
        full_page: Capturar página inteira
        quality: Qualidade JPEG (1-100)

    Returns:
        bool: True se screenshot foi salvo
    """
    try:
        await page.screenshot(path=path, full_page=full_page, quality=quality)
        logger.info(f"Screenshot salvo: {path}")
        return True

    except Exception as e:
        logger.error(f"Erro ao salvar screenshot: {str(e)}")
        return False


async def get_page_info(page: Page) -> Dict[str, Any]:
    """
    Coleta informações básicas da página atual.

    Returns:
        dict: Informações da página
    """
    try:
        return {
            "url": page.url,
            "title": await page.title(),
            "viewport": await page.viewport_size(),
            "user_agent": await page.evaluate("navigator.userAgent"),
            "cookies_count": len(await page.context.cookies()),
            "local_storage_keys": await page.evaluate(
                "Object.keys(localStorage).length"
            ),
        }
    except Exception as e:
        logger.error(f"Erro ao coletar informações da página: {str(e)}")
        return {}


async def wait_for_network_idle(
    page: Page, timeout: float = 30000, idle_time: float = 500
) -> bool:
    """
    Aguarda a rede ficar idle (sem requests pendentes).

    Args:
        page: Página do Playwright
        timeout: Timeout total
        idle_time: Tempo de idle necessário (ms)

    Returns:
        bool: True se rede ficou idle
    """
    try:
        await page.wait_for_load_state("networkidle", timeout=timeout)
        await asyncio.sleep(idle_time / 1000)  # Aguardar extra
        logger.debug("Rede está idle")
        return True

    except Exception as e:
        logger.warning(f"Timeout aguardando network idle: {str(e)}")
        return False
