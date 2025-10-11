# Arquitetura do Sistema Dell Scraper

## 🏗️ Visão Geral da Arquitetura

```
dell-scraper/
├── 🎯 Core System
│   ├── models/          # SQLAlchemy ORM & Database
│   ├── config/          # Dynaconf Configuration  
│   └── main.py          # Application Entry Point
│
├── 🌐 Browser Management (NEW!)
│   ├── browser_manager.py   # Factory Pattern + Context Management
│   ├── utils.py            # Safe Operations & Helpers
│   └── profiles/           # Production/Debug/Stealth Profiles
│
├── 🔄 Workflow System (COMING NEXT)
│   ├── workflow_manager.py # RPA Workflow Orchestration
│   ├── tasks/             # Modular Task Components
│   └── schemas/           # Data Validation & Schemas
│
├── 📊 Database Layer
│   ├── PostgreSQL 16      # Primary Database
│   ├── Alembic Migrations # Schema Versioning
│   └── pgAdmin Interface  # Web Management
│
└── 🛠️ Infrastructure
    ├── Docker Compose     # Container Orchestration
    ├── Logging System     # Structured Logs (success/failed)
    └── Configuration      # Multi-environment Settings
```

## 🎯 Design Principles

### 1. **Máxima Confiabilidade > Velocidade**
- Timeouts conservadores (30s)
- Retry automático com backoff exponencial  
- Validação robusta de elementos
- Health checks preventivos

### 2. **Arquitetura Enterprise**
- Factory Pattern para browser management
- Singleton pattern para reutilização de recursos
- Context managers para cleanup automático
- Separação clara de responsabilidades

### 3. **Padrões RPA Profissionais**
- Workflow + Tasks approach
- Modularidade e reutilização
- Logging estruturado por categoria
- Profiles configuráveis por ambiente

## 🌐 Browser Management System

### Arquitetura do Browser Layer

```python
# Factory Pattern + Context Management
BrowserManager
├── initialize()          # Playwright startup com retry
├── create_context()      # Context factory com profiles
├── get_page()           # Page factory com context pooling
├── health_check()       # System health validation
└── cleanup()            # Resource cleanup automático

# Profiles System
ProfileManager
├── production_profile   # Máxima confiabilidade
├── debug_profile       # Development & debugging  
├── stealth_profile     # Discrete scraping
└── get_profile()       # Profile factory function

# Safe Operations
Utils
├── safe_goto()         # Navigation com retry
├── wait_for_element()  # Smart element waiting
├── safe_click()        # Validated interactions
├── extract_text()      # Safe data extraction
└── take_screenshot()   # Debug & monitoring
```

### Context Management Strategy

```python
# Singleton Pattern - Instância global
browser_manager = BrowserManager()

# Context Pooling - Múltiplos contextos simultâneos
contexts = {
    "search_context": BrowserContext,    # Para busca de produtos
    "detail_context": BrowserContext,    # Para detalhes de produto
    "debug_context": BrowserContext      # Para debugging
}

# Resource Lifecycle
async with browser_manager as bm:       # Auto-cleanup
    page = await bm.get_page("main", "production")
    # ... operations
# Cleanup automático ao sair
```

## 🔄 Workflow System (Coming Next)

### Planejamento da Arquitetura de Workflows

```python
# Workflow Manager - Orquestração principal
WorkflowManager
├── register_task()      # Registro de tasks
├── execute_workflow()   # Execução sequencial/paralela  
├── handle_errors()      # Error recovery & retry
└── generate_report()    # Success/failure reporting

# Base Task - Interface comum
BaseTask
├── validate_inputs()    # Input validation
├── execute()           # Core task logic
├── handle_failure()    # Error handling
└── cleanup()          # Resource cleanup

# Task Examples
SearchTask              # Buscar produtos na Dell
ProductDetailTask       # Extrair detalhes de produto
DataValidationTask      # Validar dados coletados
DatabaseSaveTask        # Persistir no PostgreSQL
```

## 📊 Database Architecture

### Current Schema

```sql
-- Categories (1:N relationship)
categories
├── id (BIGSERIAL PK)
├── name (VARCHAR UNIQUE)
├── slug (VARCHAR UNIQUE) 
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── products[] (FOREIGN KEY)

-- Products (N:1 relationship)
products  
├── id (BIGSERIAL PK)
├── name (TEXT)
├── model (VARCHAR)
├── price (DECIMAL)
├── url (TEXT)
├── category_id (BIGINT FK → categories.id)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── category (RELATIONSHIP)
```

### Migration System

```bash
# Alembic versioning
alembic/
├── versions/
│   ├── 001_initial_migration.py     # Initial schema
│   └── 002_add_products_table.py   # Products table
├── alembic.ini                      # Configuration
└── env.py                          # Runtime environment
```

## 🛠️ Infrastructure Layer

### Docker Architecture

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=dell_products
      - POSTGRES_USER=dell_user  
      - POSTGRES_PASSWORD=***
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@dell.com
      - PGADMIN_DEFAULT_PASSWORD=***
    ports:
      - "8080:80"
    depends_on:
      - postgres
```

### Configuration Management

```python
# Dynaconf multi-environment
settings.toml
├── [default]           # Base configuration
├── [development]       # Dev overrides
├── [production]        # Prod overrides
└── [testing]          # Test configuration

# Environment-specific
.env                    # Local development
.env.production         # Production secrets
.secrets/              # Sensitive configuration
```

## 📁 Logging Architecture

### Structured Logging System

```
logs/
├── success/           # Successful operations
│   └── success_dd.MM.yyyy_hh.mm.log
└── failed/            # Failed operations  
    └── failed_dd.MM.yyyy_hh.mm.log
```

### Log Categories

```python
# Structured logging com contexto
logger.info("Navigation successful", extra={
    "url": target_url,
    "response_time": elapsed_time,
    "profile": "production"
})

logger.error("Element not found", extra={
    "selector": css_selector,
    "timeout": timeout_ms,
    "retry_count": current_retry
})
```

## 🚀 Deployment Strategy

### Development Environment

```bash
# Local development
uv venv                          # Virtual environment
uv sync                          # Install dependencies  
docker-compose up -d postgres    # Database only
python -m dell.main             # Run application
```

### Production Environment

```bash
# Full containerized deployment
docker-compose up -d            # All services
docker-compose logs -f app      # Monitor logs
docker-compose exec app bash    # Shell access
```

## 📈 Scalability Considerations

### Horizontal Scaling

- **Multi-context browsing**: Parallel product scraping
- **Database connection pooling**: SQLAlchemy engine optimization
- **Task queue integration**: Future Celery/RQ integration
- **Load balancing**: Multiple scraper instances

### Performance Optimizations

- **Browser instance reuse**: Singleton pattern implementation
- **Context pooling**: Avoid repeated browser launches
- **Selective data extraction**: Only required fields
- **Batch database operations**: Bulk inserts/updates

## 🔒 Security & Compliance

### Data Protection

- **Environment secrets**: Secure configuration management
- **Database encryption**: PostgreSQL with TLS
- **Access logging**: Comprehensive audit trail
- **Rate limiting**: Respectful scraping practices

### Browser Security

- **Stealth profiles**: Anti-detection configurations
- **Proxy support**: IP rotation capability (future)
- **User agent rotation**: Natural browsing patterns
- **Request throttling**: Avoid aggressive scraping

## 🔄 Next Implementation Steps

### Phase 1: Workflow System (Next)
1. ✅ **Browser Management** (Completed)
2. 🔄 **WorkflowManager** (In Progress)
3. ⏳ **BaseTask** interface
4. ⏳ **Dell-specific tasks**
5. ⏳ **Error handling & retry**

### Phase 2: Production Features
1. ⏳ **Configuration validation**
2. ⏳ **Monitoring & alerting** 
3. ⏳ **Performance metrics**
4. ⏳ **Database optimization**
5. ⏳ **CI/CD pipeline**

### Phase 3: Advanced Features
1. ⏳ **Task queue integration**
2. ⏳ **Proxy rotation**
3. ⏳ **Real-time monitoring**
4. ⏳ **API endpoints**
5. ⏳ **Web dashboard**

---

Esta arquitetura garante **máxima confiabilidade**, **escalabilidade enterprise** e **padrões RPA profissionais** para o sistema de scraping da Dell.