"""
BrowserManager - Factory Pattern para gerenciamento do Playwright.
Implementação enterprise com máxima confiabilidade e padrão RPA.
"""

import logging
from typing import Dict, Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)
from tenacity import retry, stop_after_attempt, wait_exponential

from dell.browser.profiles.browser_profiles import get_profile
from dell.config.settings import settings

logger = logging.getLogger(__name__)


class BrowserManager:
    """
    Gerenciador central do Playwright com padrão Factory.
    Foco em confiabilidade máxima e reutilização de recursos.
    """

    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.contexts: Dict[str, BrowserContext] = {}
        self.is_initialized = False

    async def __aenter__(self):
        """Context manager para uso com async with"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup automático ao sair do context"""
        await self.cleanup()

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def initialize(self, browser_type: str = "chromium") -> None:
        """
        Inicializa o Playwright e browser com retry automático.

        Args:
            browser_type: Tipo do browser ('chromium', 'firefox', 'webkit')
        """
        try:
            logger.info(f"Inicializando BrowserManager com {browser_type}")

            if self.is_initialized:
                logger.warning("BrowserManager já está inicializado")
                return

            # Inicializar Playwright
            self.playwright = await async_playwright().start()
            logger.debug("Playwright iniciado com sucesso")

            # Configurações base do browser
            browser_config = {
                "headless": not settings.debug if hasattr(settings, "debug") else True,
                "args": [
                    "--disable-blink-features=AutomationControlled",
                    "--no-first-run",
                    "--disable-dev-shm-usage",
                ],
            }

            # Lançar browser
            browser_launcher = getattr(self.playwright, browser_type)
            self.browser = await browser_launcher.launch(**browser_config)

            self.is_initialized = True
            logger.info(f"Browser {browser_type} inicializado com sucesso")

        except Exception as e:
            logger.error(f"Erro ao inicializar browser: {str(e)}")
            await self.cleanup()
            raise

    async def create_context(
        self, profile_name: str = "production", context_id: str = "default", **kwargs
    ) -> BrowserContext:
        """
        Cria um novo contexto de browser com perfil específico.

        Args:
            profile_name: Nome do perfil ('production', 'debug', 'stealth')
            context_id: ID único para o contexto
            **kwargs: Configurações adicionais para sobrescrever perfil

        Returns:
            BrowserContext: Contexto configurado e pronto para uso
        """
        if not self.is_initialized:
            await self.initialize()

        # Se contexto já existe, retorna o existente
        if context_id in self.contexts:
            logger.info(f"Reutilizando contexto existente: {context_id}")
            return self.contexts[context_id]

        try:
            # Carregar configurações do perfil
            profile_config = get_profile(profile_name)

            # Sincronizar com pace manager
            profile_config = self._sync_pace_with_profile(profile_name, profile_config)

            # Aplicar kwargs customizados (sobrescreve perfil)
            profile_config.update(kwargs)

            logger.info(f"Criando contexto '{context_id}' com perfil '{profile_name}'")

            # Criar contexto com configurações
            context = await self.browser.new_context(**profile_config)

            # Configurações extras pós-criação
            await self._setup_context_extras(context, profile_name)

            # Armazenar referência
            self.contexts[context_id] = context

            logger.info(f"Contexto '{context_id}' criado com sucesso")
            return context

        except Exception as e:
            logger.error(f"Erro ao criar contexto '{context_id}': {str(e)}")
            raise

    async def _setup_context_extras(
        self, context: BrowserContext, profile_name: str
    ) -> None:
        """
        Configurações extras aplicadas após criação do contexto.
        """
        try:
            # Interceptar e logar requests se em debug
            if profile_name == "debug":
                context.on(
                    "request",
                    lambda request: logger.debug(
                        f"Request: {request.method} {request.url}"
                    ),
                )
                context.on(
                    "response",
                    lambda response: logger.debug(
                        f"Response: {response.status} {response.url}"
                    ),
                )

            # Stealth mode - remover indicadores de automação
            if profile_name in ["production", "stealth"]:
                await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    window.chrome = {
                        runtime: {},
                    };
                    
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['pt-BR', 'pt', 'en-US', 'en'],
                    });
                """)

        except Exception as e:
            logger.warning(f"Erro ao aplicar configurações extras: {str(e)}")

    async def get_page(
        self, context_id: str = "default", profile_name: str = "production"
    ) -> Page:
        """
        Obtém uma nova página do contexto especificado.

        Args:
            context_id: ID do contexto
            profile_name: Perfil a usar se contexto não existir

        Returns:
            Page: Nova página pronta para uso
        """
        # Garantir que contexto existe
        if context_id not in self.contexts:
            await self.create_context(profile_name, context_id)

        context = self.contexts[context_id]
        page = await context.new_page()

        logger.debug(f"Nova página criada no contexto '{context_id}'")
        return page

    async def close_context(self, context_id: str) -> None:
        """
        Fecha um contexto específico e libera recursos.
        """
        if context_id in self.contexts:
            try:
                await self.contexts[context_id].close()
                del self.contexts[context_id]
                logger.info(f"Contexto '{context_id}' fechado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao fechar contexto '{context_id}': {str(e)}")

    async def cleanup(self) -> None:
        """
        Cleanup completo - fecha todos os recursos.
        """
        logger.info("Iniciando cleanup do BrowserManager")

        # Fechar todos os contextos
        for context_id in list(self.contexts.keys()):
            await self.close_context(context_id)

        # Fechar browser
        if self.browser:
            try:
                await self.browser.close()
                logger.debug("Browser fechado")
            except Exception as e:
                logger.warning(f"Erro ao fechar browser: {str(e)}")

        # Parar Playwright
        if self.playwright:
            try:
                await self.playwright.stop()
                logger.debug("Playwright parado")
            except Exception as e:
                logger.warning(f"Erro ao parar Playwright: {str(e)}")

        # Reset estado
        self.playwright = None
        self.browser = None
        self.contexts = {}
        self.is_initialized = False

        logger.info("Cleanup concluído")

    async def health_check(self) -> bool:
        """
        Verifica se o browser está funcionando corretamente.

        Returns:
            bool: True se saudável, False caso contrário
        """
        try:
            if not self.is_initialized:
                return False

            # Criar contexto temporário para teste
            test_context = await self.browser.new_context()
            test_page = await test_context.new_page()

            # Teste básico - navegar para página simples
            await test_page.goto("data:text/html,<html><body>OK</body></html>")
            content = await test_page.content()

            # Cleanup do teste
            await test_context.close()

            return "OK" in content

        except Exception as e:
            logger.error(f"Health check falhou: {str(e)}")
            return False


# Instância global para reutilização (Singleton pattern)
browser_manager = BrowserManager()
