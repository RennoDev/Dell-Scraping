"""
Browser profiles configuration for Dell scraping automation.
Following RPA standards with maximum reliability approach.
"""

# Production Profile - Maximum Reliability
PRODUCTION_PROFILE = {
    "headless": True,
    "timeout": 30000,  # 30s - tempo suficiente sempre
    "navigation_timeout": 45000,  # 45s - para páginas pesadas
    "slow_mo": 1000,  # 1s entre ações (cuidadoso)
    "wait_for_load_state": "networkidle",  # Garante carregamento completo
    "viewport": {"width": 1920, "height": 1080},
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "extra_http_headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    },
    "ignore_https_errors": True,
    "java_script_enabled": True,
    "bypass_csp": True,  # Bypass Content Security Policy se necessário
    "locale": "pt-BR",
    "timezone_id": "America/Sao_Paulo",
    "geolocation": {"latitude": -23.5505, "longitude": -46.6333},  # São Paulo
    "permissions": ["geolocation"],
    "color_scheme": "light",
    "reduced_motion": "no-preference",
}

# Debug Profile - Para desenvolvimento e análise de elementos
DEBUG_PROFILE = {
    **PRODUCTION_PROFILE,  # Herda configurações de produção
    "headless": False,  # 👀 Ver o browser
    "slow_mo": 2000,  # 2s entre ações (mais lento)
    "devtools": True,  # 🔧 DevTools aberto automaticamente
    "timeout": 60000,  # Timeout maior para debug
    "args": [
        "--start-maximized",
        "--disable-blink-features=AutomationControlled",
        "--disable-web-security",
        "--allow-running-insecure-content",
    ],
}

# Stealth Profile - Para casos que precisam de mais discrição
STEALTH_PROFILE = {
    **PRODUCTION_PROFILE,
    "slow_mo": 1500,  # Mais lento ainda
    "extra_http_headers": {
        **PRODUCTION_PROFILE["extra_http_headers"],
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    },
    "args": [
        "--no-first-run",
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--no-sandbox",
    ],
}

# Mapeamento de perfis disponíveis
AVAILABLE_PROFILES = {
    "production": PRODUCTION_PROFILE,
    "debug": DEBUG_PROFILE,
    "stealth": STEALTH_PROFILE,
}


def get_profile(profile_name: str = "production") -> dict:
    """
    Retorna configuração do perfil especificado.

    Args:
        profile_name: Nome do perfil ('production', 'debug', 'stealth')

    Returns:
        dict: Configuração do perfil

    Raises:
        ValueError: Se o perfil não existe
    """
    if profile_name not in AVAILABLE_PROFILES:
        raise ValueError(
            f"Perfil '{profile_name}' não encontrado. Disponíveis: {list(AVAILABLE_PROFILES.keys())}"
        )

    return AVAILABLE_PROFILES[profile_name].copy()
