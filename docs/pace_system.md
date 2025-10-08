# Sistema de Pace Global - Guia de Uso 🎯

**Excelente ideia! O Sistema de Pace Global substitui todos os `sleep` hardcoded por um controle inteligente e configurável da velocidade da aplicação.**

## 🚀 **O que Mudou - Antes vs Agora**

### ❌ **ANTES - Sleeps Hardcoded**
```python
# Problemas do sistema antigo:
await asyncio.sleep(1.0)      # 😒 Tempo fixo
await asyncio.sleep(2.0)      # 😒 Sem contexto
await asyncio.sleep(0.5)      # 😒 Não configurável
```

### ✅ **AGORA - Pace Inteligente**  
```python
# Solução inteligente:
await wait_click("clique no botão")           # 🎯 Contextualizado
await wait_navigation("carregando página")    # 🎯 Por tipo de operação
await wait_extraction("extraindo dados")     # 🎯 Configurável globalmente
```

---

## 🎮 **Como Usar - Super Simples**

### **1. Configuração Global Básica**
```python
from dell.browser import configure_pace, PaceLevel

# Configurar velocidade da aplicação toda
configure_pace(PaceLevel.NORMAL)     # ⚡ Velocidade padrão
configure_pace(PaceLevel.CAREFUL)    # 🐌 Máxima confiabilidade  
configure_pace(PaceLevel.TURBO)      # 🚀 Máxima velocidade
configure_pace(PaceLevel.DEBUG)      # 🔍 Para desenvolvimento
configure_pace(PaceLevel.STEALTH)    # 🥷 Anti-detecção
```

### **2. Uso Automático nas Funções**
```python
# TODAS as funções já usam pace automático!
await safe_goto(page, "https://dell.com")     # ← Usa wait_navigation
await safe_click(page, "button")             # ← Usa wait_click  
await safe_fill(page, "input", "texto")      # ← Usa wait_fill
await extract_text(page, "h1")               # ← Usa wait_extraction
```

### **3. Controle Fino com Multiplicador**
```python
# Ajuste fino da velocidade
configure_pace(PaceLevel.NORMAL, multiplier=2.0)    # 2x mais lento
configure_pace(PaceLevel.NORMAL, multiplier=0.5)    # 2x mais rápido  
configure_pace(PaceLevel.NORMAL, multiplier=1.0)    # Velocidade normal
```

---

## 📊 **Níveis de Pace Disponíveis**

| Nível | Velocidade | Uso Ideal | Timing Médio |
|-------|------------|-----------|--------------|
| 🚀 **TURBO** | Máxima | Produção otimizada | 0.1s |
| ⚡ **NORMAL** | Padrão | Produção segura | 0.5s |
| 🐌 **CAREFUL** | Cuidadosa | Máxima confiabilidade | 1.0s |
| 🔍 **DEBUG** | Lenta | Desenvolvimento | 2.0s |
| 🥷 **STEALTH** | Discreta | Anti-detecção | 1.5s |

### **Configurações Detalhadas por Operação:**

```python
# Exemplo de timings (em segundos):
PaceLevel.NORMAL = {
    "navigation": 0.5,    # Navegação entre páginas
    "click": 0.3,         # Cliques em elementos  
    "fill": 0.2,          # Preenchimento de campos
    "scroll": 0.3,        # Operações de scroll
    "extraction": 0.1,    # Extração de dados
    "network": 1.0,       # Operações de rede
    "retry": 2.0,         # Delays entre retries
}
```

---

## 🎯 **Exemplos Práticos de Uso**

### **Scraping de Produção - Confiável**
```python
from dell.browser import browser_manager, configure_pace, PaceLevel

async def scrape_dell_produtos():
    # Configurar para máxima confiabilidade
    configure_pace(PaceLevel.CAREFUL)
    
    async with browser_manager as bm:
        page = await bm.get_page("produtos", "production")
        
        # Todas as operações usam timing CAREFUL automaticamente
        await safe_goto(page, "https://dell.com.br/notebooks")
        await safe_click(page, ".filtro-preco")  
        produtos = await extract_text(page, ".produto-titulo")
        
        return produtos
```

### **Desenvolvimento - Visual e Lento**
```python
async def debug_scraping():
    # Configurar para desenvolvimento
    configure_pace(PaceLevel.DEBUG)
    
    async with browser_manager as bm:
        # Browser visível + timing lento = fácil debug
        page = await bm.get_page("debug", "debug")
        
        await safe_goto(page, "https://dell.com.br")
        # Aguarda 2s entre cada ação - você vê tudo acontecendo
```

### **Performance - Velocidade Máxima**
```python
async def scrape_rapido():
    # Configurar para velocidade máxima
    configure_pace(PaceLevel.TURBO)
    
    async with browser_manager as bm:
        page = await bm.get_page("rapido", "production")
        
        # Executa com delays mínimos
        await safe_goto(page, "https://dell.com.br")
        # Apenas 0.1s entre ações
```

---

## 🔄 **Pace Dinâmico Durante Execução**

### **Mudança de Velocidade em Runtime**
```python
async def scraping_adaptativo():
    # Começar rápido para navegação inicial
    configure_pace(PaceLevel.TURBO) 
    await safe_goto(page, "https://dell.com.br")
    
    # Mudar para cuidadoso na parte crítica
    configure_pace(PaceLevel.CAREFUL)
    dados_importantes = await extract_text(page, ".preco")
    
    # Voltar para rápido para operações finais  
    configure_pace(PaceLevel.TURBO)
    await safe_click(page, ".proximo")
```

### **Pace Temporário com Context Manager**
```python
from dell.browser import TemporaryPace

async def scraping_com_pace_temporario():
    # Pace global NORMAL
    configure_pace(PaceLevel.NORMAL)
    
    await safe_goto(page, "https://dell.com.br")  # ⚡ NORMAL
    
    # Operação específica em modo STEALTH
    async with TemporaryPace(PaceLevel.STEALTH):
        # Dentro deste bloco = timing STEALTH 🥷
        dados_sensiveis = await extract_text(page, ".dados")
    
    # Automaticamente volta para NORMAL ⚡
    await safe_click(page, ".continuar") 
```

---

## 📈 **Monitoramento e Estatísticas**

### **Ver Estatísticas de Uso**
```python
from dell.browser import pace_manager

# Obter estatísticas detalhadas
stats = pace_manager.get_statistics()

print(f"Nível atual: {stats['pace_level']}")           # Ex: "normal"
print(f"Multiplicador: {stats['multiplier']}x")        # Ex: 1.0
print(f"Total operações: {stats['total_operations']}")  # Ex: 47

# Operações por tipo
for operacao, quantidade in stats['operations_by_type'].items():
    print(f"{operacao}: {quantidade} vezes")

# Delays atuais  
for operacao, delay in stats['current_delays'].items():
    print(f"{operacao}: {delay:.2f}s")
```

### **Comparar Performance de Diferentes Paces**
```python
import time

async def benchmark_pace():
    tempos = {}
    
    for pace in [PaceLevel.TURBO, PaceLevel.NORMAL, PaceLevel.CAREFUL]:
        configure_pace(pace)
        
        start = time.time()
        await executar_scraping()
        tempos[pace.value] = time.time() - start
    
    # Comparar resultados
    print(f"TURBO: {tempos['turbo']:.2f}s")
    print(f"NORMAL: {tempos['normal']:.2f}s") 
    print(f"CAREFUL: {tempos['careful']:.2f}s")
```

---

## 🛠️ **Integração com Profiles de Browser**

O sistema sincroniza automaticamente com os profiles do browser:

```python
# O pace afeta o slow_mo do Playwright automaticamente!

configure_pace(PaceLevel.CAREFUL)    # → slow_mo = 1000ms no browser
configure_pace(PaceLevel.DEBUG)      # → slow_mo = 2000ms no browser  
configure_pace(PaceLevel.TURBO)      # → slow_mo = 100ms no browser
```

---

## 🎯 **Recomendações de Uso**

### **🏭 Produção**
```python
# Para scraping confiável em produção
configure_pace(PaceLevel.CAREFUL, multiplier=1.0)
```

### **🔧 Desenvolvimento** 
```python
# Para debug visual e análise
configure_pace(PaceLevel.DEBUG, multiplier=1.0)
```

### **⚡ Testes Rápidos**
```python
# Para testes e prototipagem  
configure_pace(PaceLevel.TURBO, multiplier=1.0)
```

### **🥷 Sites Restritivos**
```python
# Para sites que detectam bots
configure_pace(PaceLevel.STEALTH, multiplier=1.5)  # Extra cuidadoso
```

---

## 🏆 **Vantagens do Sistema**

### ✅ **Para Você (Desenvolvedor):**
- **Uma linha** para controlar velocidade de tudo: `configure_pace(PaceLevel.CAREFUL)`
- **Sem mais sleeps mágicos** espalhados pelo código
- **Contexto claro** do que cada delay faz
- **Ajuste fino** com multiplicadores

### ✅ **Para a Aplicação:**
- **Velocidade adaptativa** por tipo de operação  
- **Timing inteligente** baseado no contexto
- **Configuração centralizada** e consistente
- **Estatísticas** para otimização

### ✅ **Para Produção:**
- **Confiabilidade configurável** por ambiente
- **Monitoring integrado** de performance  
- **Ajuste sem redeploy** (mudança de configuração)
- **Padrão consistente** em todo o sistema

---

## 🚀 **Migração do Código Antigo**

### **Antes (Hardcoded):**
```python
await page.goto(url)
await asyncio.sleep(2.0)                    # ❌ Tempo fixo

await element.click() 
await asyncio.sleep(1.5)                    # ❌ Sem contexto

await element.fill(value)
await asyncio.sleep(0.8)                    # ❌ Não configurável
```

### **Agora (Inteligente):**
```python
await safe_goto(page, url)                  # ✅ Pace automático
# Não precisa de sleep manual!

await safe_click(page, selector)            # ✅ Pace por operação  
# Timing perfeito automaticamente!

await safe_fill(page, selector, value)      # ✅ Contexto claro
# Sistema gerencia o timing!
```

**O sistema funciona transparentemente - você só precisa configurar o pace uma vez e tudo funciona! 🎉**

---

**Agora você tem controle TOTAL sobre a velocidade da aplicação com uma linha de código! 🎯⚡**