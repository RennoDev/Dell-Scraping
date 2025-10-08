"""
Pace Manager - Sistema de controle de velocidade global da aplicação.
Substitui sleeps hardcoded por estratégias configuráveis e inteligentes.
"""

import asyncio
import logging
from enum import Enum
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class PaceLevel(Enum):
    """Níveis de velocidade da aplicação."""

    TURBO = "turbo"  # 🚀 Máxima velocidade (produção otimizada)
    NORMAL = "normal"  # ⚡ Velocidade padrão (produção segura)
    CAREFUL = "careful"  # 🐌 Velocidade cuidadosa (máxima confiabilidade)
    DEBUG = "debug"  # 🔍 Velocidade debug (desenvolvimento)
    STEALTH = "stealth"  # 🥷 Velocidade stealth (anti-detecção)


class OperationType(Enum):
    """Tipos de operação com diferentes necessidades de timing."""

    NAVIGATION = "navigation"  # Navegação entre páginas
    CLICK = "click"  # Cliques em elementos
    FILL = "fill"  # Preenchimento de campos
    SCROLL = "scroll"  # Operações de scroll
    EXTRACTION = "extraction"  # Extração de dados
    NETWORK = "network"  # Operações de rede
    RETRY = "retry"  # Delays entre retries


class PaceManager:
    """
    Gerenciador global de velocidade da aplicação.
    Controla timing inteligente baseado no contexto.
    """

    # Configurações de timing (em segundos)
    PACE_CONFIGS = {
        PaceLevel.TURBO: {
            OperationType.NAVIGATION: 0.1,
            OperationType.CLICK: 0.05,
            OperationType.FILL: 0.02,
            OperationType.SCROLL: 0.1,
            OperationType.EXTRACTION: 0.01,
            OperationType.NETWORK: 0.5,
            OperationType.RETRY: 1.0,
        },
        PaceLevel.NORMAL: {
            OperationType.NAVIGATION: 0.5,
            OperationType.CLICK: 0.3,
            OperationType.FILL: 0.2,
            OperationType.SCROLL: 0.3,
            OperationType.EXTRACTION: 0.1,
            OperationType.NETWORK: 1.0,
            OperationType.RETRY: 2.0,
        },
        PaceLevel.CAREFUL: {
            OperationType.NAVIGATION: 1.0,
            OperationType.CLICK: 0.8,
            OperationType.FILL: 0.5,
            OperationType.SCROLL: 0.5,
            OperationType.EXTRACTION: 0.2,
            OperationType.NETWORK: 2.0,
            OperationType.RETRY: 3.0,
        },
        PaceLevel.DEBUG: {
            OperationType.NAVIGATION: 2.0,
            OperationType.CLICK: 1.5,
            OperationType.FILL: 1.0,
            OperationType.SCROLL: 1.0,
            OperationType.EXTRACTION: 0.5,
            OperationType.NETWORK: 2.0,
            OperationType.RETRY: 4.0,
        },
        PaceLevel.STEALTH: {
            OperationType.NAVIGATION: 1.5,
            OperationType.CLICK: 1.2,
            OperationType.FILL: 0.8,
            OperationType.SCROLL: 0.8,
            OperationType.EXTRACTION: 0.3,
            OperationType.NETWORK: 3.0,
            OperationType.RETRY: 5.0,
        },
    }

    def __init__(self, pace_level: PaceLevel = PaceLevel.NORMAL):
        self.pace_level = pace_level
        self.custom_multiplier = 1.0
        self.operation_counts: Dict[OperationType, int] = {}

        logger.info(f"PaceManager inicializado com nível: {pace_level.value}")

    def set_pace_level(self, pace_level: PaceLevel) -> None:
        """
        Define o nível de velocidade global.

        Args:
            pace_level: Novo nível de velocidade
        """
        old_level = self.pace_level
        self.pace_level = pace_level
        logger.info(f"Pace alterado de {old_level.value} → {pace_level.value}")

    def set_multiplier(self, multiplier: float) -> None:
        """
        Define multiplicador customizado para ajuste fino.

        Args:
            multiplier: Multiplicador (1.0 = normal, 2.0 = 2x mais lento)
        """
        self.custom_multiplier = multiplier
        logger.info(f"Multiplicador de pace definido: {multiplier}x")

    async def wait(
        self,
        operation_type: OperationType,
        custom_delay: Optional[float] = None,
        reason: str = "",
    ) -> None:
        """
        Executa delay inteligente baseado no tipo de operação.

        Args:
            operation_type: Tipo da operação
            custom_delay: Delay customizado (sobrescreve configuração)
            reason: Motivo do delay (para logging)
        """
        if custom_delay is not None:
            delay = custom_delay
        else:
            base_delay = self.PACE_CONFIGS[self.pace_level][operation_type]
            delay = base_delay * self.custom_multiplier

        # Contador de operações para estatísticas
        self.operation_counts[operation_type] = (
            self.operation_counts.get(operation_type, 0) + 1
        )

        if delay > 0:
            logger.debug(f"Pace wait: {delay:.2f}s ({operation_type.value}) - {reason}")
            await asyncio.sleep(delay)

    def get_delay(self, operation_type: OperationType) -> float:
        """
        Obtém o delay configurado para um tipo de operação.

        Args:
            operation_type: Tipo da operação

        Returns:
            float: Delay em segundos
        """
        base_delay = self.PACE_CONFIGS[self.pace_level][operation_type]
        return base_delay * self.custom_multiplier

    def get_statistics(self) -> Dict[str, any]:
        """
        Retorna estatísticas de uso do pace manager.
        """
        total_operations = sum(self.operation_counts.values())

        return {
            "pace_level": self.pace_level.value,
            "multiplier": self.custom_multiplier,
            "total_operations": total_operations,
            "operations_by_type": {
                op_type.value: count for op_type, count in self.operation_counts.items()
            },
            "current_delays": {
                op_type.value: self.get_delay(op_type) for op_type in OperationType
            },
        }

    def reset_statistics(self) -> None:
        """Reseta contadores de operações."""
        self.operation_counts.clear()
        logger.info("Estatísticas de pace resetadas")


# Instância global do pace manager
pace_manager = PaceManager()


# Funções de conveniência para uso direto
async def wait_navigation(reason: str = "") -> None:
    """Aguarda timing de navegação."""
    await pace_manager.wait(OperationType.NAVIGATION, reason=reason)


async def wait_click(reason: str = "") -> None:
    """Aguarda timing de clique."""
    await pace_manager.wait(OperationType.CLICK, reason=reason)


async def wait_fill(reason: str = "") -> None:
    """Aguarda timing de preenchimento."""
    await pace_manager.wait(OperationType.FILL, reason=reason)


async def wait_scroll(reason: str = "") -> None:
    """Aguarda timing de scroll."""
    await pace_manager.wait(OperationType.SCROLL, reason=reason)


async def wait_extraction(reason: str = "") -> None:
    """Aguarda timing de extração."""
    await pace_manager.wait(OperationType.EXTRACTION, reason=reason)


async def wait_network(reason: str = "") -> None:
    """Aguarda timing de rede."""
    await pace_manager.wait(OperationType.NETWORK, reason=reason)


async def wait_retry(reason: str = "") -> None:
    """Aguarda timing entre retries."""
    await pace_manager.wait(OperationType.RETRY, reason=reason)


# Função para configuração rápida
def configure_pace(
    level: PaceLevel = PaceLevel.NORMAL, multiplier: float = 1.0
) -> None:
    """
    Configuração rápida do pace global.

    Args:
        level: Nível de velocidade
        multiplier: Multiplicador adicional
    """
    pace_manager.set_pace_level(level)
    pace_manager.set_multiplier(multiplier)

    logger.info(f"Pace configurado: {level.value} (x{multiplier})")


# Context manager para pace temporário
class TemporaryPace:
    """Context manager para pace temporário."""

    def __init__(self, level: PaceLevel, multiplier: float = 1.0):
        self.temp_level = level
        self.temp_multiplier = multiplier
        self.original_level = None
        self.original_multiplier = None

    async def __aenter__(self):
        self.original_level = pace_manager.pace_level
        self.original_multiplier = pace_manager.custom_multiplier

        pace_manager.set_pace_level(self.temp_level)
        pace_manager.set_multiplier(self.temp_multiplier)

        return pace_manager

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pace_manager.set_pace_level(self.original_level)
        pace_manager.set_multiplier(self.original_multiplier)
