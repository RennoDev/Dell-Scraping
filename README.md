# 🖥️ Dell Products Scraper# 🖥️ Dell Products Scraper



> Professional web scraper for collecting and storing Dell products with complete data pipeline.> Professional web scraper for collecting and storing Dell products with complete data pipeline.



## 📋 About the Project## 📋 About the Project



Web scraping system developed to collect product information from Dell's official website, process the data, and store it in a PostgreSQL database with management interface.Web scraping system developed to collect product information from Dell's official website, process the data, and store it in a PostgreSQL database with management interface.



### 🎯 Objectives### 🎯 Objectives

- **Automated collection** of Dell products (model, price, links)- **Automated collection** of Dell products (model, price, links)

- **Structured storage** in PostgreSQL- **Structured storage** in PostgreSQL

- **Robust pipeline** for data processing- **Robust pipeline** for data processing

- **Scalable architecture** with containerization- **Scalable architecture** with containerization



## 🛠️ Technology Stack## 🛠️ Technology Stack



### **Core Technologies**### **Core Technologies**

- **Python 3.13** - Main programming language- **Python 3.13** - Main programming language

- **PostgreSQL 16** - Relational database- **PostgreSQL 16** - Relational database

- **Docker & Docker Compose** - Containerization- **Docker & Docker Compose** - Containerization



### **Web Scraping**### **Web Scraping**

- **Playwright 1.55+** - Modern web automation- **Playwright 1.55+** - Modern web automation

- **Rich 14.1+** - Professional CLI interface- **Rich 14.1+** - Professional CLI interface



### **Database & ORM**### **Database & ORM**

- **SQLAlchemy 2.0+** - ORM and data abstraction- **SQLAlchemy 2.0+** - ORM and data abstraction

- **Alembic 1.16+** - Schema migrations- **Alembic 1.16+** - Schema migrations

- **psycopg2-binary 2.9+** - PostgreSQL driver- **psycopg2-binary 2.9+** - PostgreSQL driver



### **Configuration & Data**### **Configuration & Data**

- **Dynaconf 3.2+** - Configuration management- **Dynaconf 3.2+** - Configuration management

- **Pydantic 2.11+** - Data validation- **Pydantic 2.11+** - Data validation

- **Pandas 2.3+** - Data processing- **Pandas 2.3+** - Data processing



### **Development Tools**### **Development Tools**

- **uv** - Modern dependency manager- **uv** - Modern dependency manager

- **Structlog 25.4+** - Structured logging- **Structlog 25.4+** - Structured logging

- **Tenacity 9.1+** - Automatic retry- **Tenacity 9.1+** - Automatic retry

- **pgAdmin 4** - Database administration interface- **pgAdmin 4** - Database administration interface



## 🏗️ System Architecture## 🏗️ System Architecture



```mermaid```mermaid

graph TBgraph TB

    A[Dell Website] --> B[Playwright Scraper]    A[Dell Website] --> B[Playwright Scraper]

    B --> C[Data Processor]    B --> C[Data Processor]

    C --> D[Pydantic Validator]    C --> D[Pydantic Validator]

    D --> E[SQLAlchemy Models]    D --> E[SQLAlchemy Models]

    E --> F[PostgreSQL]    E --> F[PostgreSQL]

    F --> G[pgAdmin Interface]    F --> G[pgAdmin Interface]

        

    H[Dynaconf] --> B    H[Dynaconf] --> B

    H --> E    H --> E

    I[Rich CLI] --> B    I[Rich CLI] --> B

    J[Alembic] --> F    J[Alembic] --> F

``````



### **Separation of Concerns**### **Separation of Concerns**

``````

📁 src/dell/📁 src/dell/

├── 📂 config/          # Configurations (Dynaconf)├── 📂 config/          # Configurations (Dynaconf)

├── 📂 models/          # SQLAlchemy Models├── 📂 models/          # SQLAlchemy Models

├── 📂 scraper/         # Web scraping logic├── 📂 scraper/         # Web scraping logic

├── 📂 services/        # Business rules  ├── 📂 services/        # Business rules  

├── 📂 repositories/    # Data access├── 📂 repositories/    # Data access

└── 📂 utils/           # General utilities└── 📂 utils/           # General utilities

``````



## 🗄️ Database Schema## 🗄️ Database Schema



### **Main Tables**### **Main Tables**



#### **Categories**#### **Categories**

- `id` (PK) - Unique identifier- `id` (PK) - Unique identifier

- `name` - Category name (e.g., "Laptops")- `name` - Category name (e.g., "Laptops")

- `slug` - URL-friendly identifier- `slug` - URL-friendly identifier

- `created_at`, `updated_at`, `is_active` - Audit fields- `created_at`, `updated_at`, `is_active` - Audit fields



#### **Products**  #### **Products**  

- `id` (PK) - Unique identifier- `id` (PK) - Unique identifier

- `model` - Dell product model- `model` - Dell product model

- `price` - Price (DECIMAL 10,2)- `price` - Price (DECIMAL 10,2)

- `link` - Product URL on Dell website- `link` - Product URL on Dell website

- `category_id` (FK) - Reference to Categories- `category_id` (FK) - Reference to Categories

- `created_at`, `updated_at`, `is_active` - Audit fields- `created_at`, `updated_at`, `is_active` - Audit fields



### **Relationships**### **Relationships**

- **1:N** - One category can have multiple products- **1:N** - One category can have multiple products

- **Foreign Key** with referential integrity- **Foreign Key** with referential integrity



## ⚙️ Secure Configuration## ⚙️ Secure Configuration



### **Multi-Environment**### **Multi-Environment**

```toml```toml

# settings.toml# settings.toml

[development][development]

debug = truedebug = true

scraping_delay = 1scraping_delay = 1



[production]  [production]  

debug = falsedebug = false

scraping_delay = 3scraping_delay = 3

``````



### **Secrets Management**### **Secrets Management**

```toml```toml

# .secrets.toml (git ignored)# .secrets.toml (git ignored)

[default][default]

POSTGRES_PASSWORD = "secure_password"POSTGRES_PASSWORD = "secure_password"

POSTGRES_USER = "dell_user"POSTGRES_USER = "dell_user"

``````



### **Environment Variables**### **Environment Variables**

```bash```bash

# .env (git ignored)# .env (git ignored)

ENV_FOR_DYNACONF=developmentENV_FOR_DYNACONF=development

POSTGRES_DB=dell_dbPOSTGRES_DB=dell_db

POSTGRES_USER=dell_userPOSTGRES_USER=dell_user

POSTGRES_PASSWORD=dev_password_123POSTGRES_PASSWORD=dev_password_123

``````



## 🐳 Containerization## 🐳 Containerization



### **Docker Compose Services**### **Docker Compose Services**

- **PostgreSQL 16-Alpine** - Main database- **PostgreSQL 16-Alpine** - Main database

- **pgAdmin 4** - Web administration interface- **pgAdmin 4** - Web administration interface

- **Persistent volumes** - Data preservation- **Persistent volumes** - Data preservation

- **Isolated network** - Container communication- **Isolated network** - Container communication



## 🚀 Setup and Installation## 🚀 Setup and Installation



### **Prerequisites**### **Prerequisites**

- Python 3.13+- Python 3.13+

- Docker & Docker Compose- Docker & Docker Compose

- uv package manager- uv package manager



### **1. Clone and Setup**### **1. Clone and Setup**

```bash```bash

git clone <repository>git clone <repository>

cd dellcd dell

cp .env.example .envcp .env.example .env

# Edit credentials in .env# Edit credentials in .env

``````



### **2. Install Dependencies**### **2. Install Dependencies**

```bash```bash

uv syncuv sync

uv run playwright install chromiumuv run playwright install chromium

``````



### **3. Start Infrastructure**### **3. Start Infrastructure**

```bash```bash

docker-compose up -d postgresdocker-compose up -d postgres

docker-compose up -d pgadmin  # Optionaldocker-compose up -d pgadmin  # Optional

``````



### **4. Setup Database**### **4. Setup Database**

```bash```bash

# Apply migrations# Apply migrations

uv run alembic upgrade headuv run alembic upgrade head



# Verify created tables# Verify created tables

docker exec -it dell_postgres psql -U dell_user -d dell_db -c "\dt"docker exec -it dell_postgres psql -U dell_user -d dell_db -c "\dt"

``````



### **5. Access pgAdmin (Optional)**### **5. Access pgAdmin (Optional)**

- **URL:** http://localhost:8080- **URL:** http://localhost:8080

- **Email:** admin@dell.com- **Email:** admin@dell.com

- **Password:** admin_dev_123- **Password:** admin_dev_123



**Configure connection:****Configure connection:**

- **Host:** postgres- **Host:** postgres

- **Port:** 5432- **Port:** 5432

- **Database:** dell_db- **Database:** dell_db

- **Username:** dell_user  - **Username:** dell_user  

- **Password:** [your_password_from_.env]- **Password:** [your_password_from_.env]



## 📊 Development Methodology## 📊 Metodologia de Desenvolvimento



### **Bottom-Up Approach**### **Abordagem Bottom-Up**

1. **🏗️ Infrastructure First** - Docker, PostgreSQL, configurations1. **🏗️ Infrastructure First** - Docker, PostgreSQL, configurações

2. **🗄️ Database Layer** - Models, relationships, migrations  2. **🗄️ Database Layer** - Models, relacionamentos, migrações  

3. **⚙️ Configuration Management** - Dynaconf, secrets, environments3. **⚙️ Configuration Management** - Dynaconf, secrets, ambientes

4. **🕸️ Business Logic** - Scrapers, services, pipeline4. **🕸️ Business Logic** - Scrapers, services, pipeline

5. **💻 User Interface** - CLI, commands, feedback5. **💻 User Interface** - CLI, comandos, feedback

6. **🧪 Testing & Quality** - Tests, validations6. **🧪 Testing & Quality** - Testes, validações

7. **🐳 Deployment** - Complete containerization7. **🐳 Deployment** - Containerização completa



### **Applied Principles**### **Princípios Aplicados**

- **Separation of Concerns** - Each layer has single responsibility- **Separation of Concerns** - Cada camada tem responsabilidade única

- **Database First** - Well-defined schema before logic- **Database First** - Schema bem definido antes da lógica

- **Configuration Management** - Organized environments and secrets- **Configuration Management** - Ambientes e secrets organizados

- **Containerization** - Reproducible infrastructure- **Containerization** - Infraestrutura reproduzível

- **Type Safety** - Pydantic + SQLAlchemy for validation- **Type Safety** - Pydantic + SQLAlchemy para validação



## 🔄 Database Migrations## 🔄 Database Migrations



```bash```bash

# Generate new migration# Generate new migration

uv run alembic revision --autogenerate -m "Description of change"uv run alembic revision --autogenerate -m "Description of change"



# Apply migrations# Apply migrations

uv run alembic upgrade headuv run alembic upgrade head



# View history# View history

uv run alembic historyuv run alembic history



# Rollback if needed  # Rollback if needed  

uv run alembic downgrade -1uv run alembic downgrade -1

``````



## 📈 Project Status## 📈 Project Status



### **✅ Implemented**### **✅ Implemented**

- ✅ Complete Docker infrastructure- ✅ Complete Docker infrastructure

- ✅ SQLAlchemy models with relationships- ✅ SQLAlchemy models with relationships

- ✅ Alembic migrations system- ✅ Alembic migrations system

- ✅ Secure multi-environment configuration- ✅ Secure multi-environment configuration

- ✅ Functional PostgreSQL database- ✅ Functional PostgreSQL database

- ✅ Configured pgAdmin interface- ✅ Configured pgAdmin interface



### **🔄 In Development**### **🔄 In Development**

- 🔄 Playwright web scraper- 🔄 Playwright web scraper

- 🔄 Processing pipeline- 🔄 Processing pipeline

- 🔄 Rich CLI interface- 🔄 Rich CLI interface

- 🔄 Structured logging system- 🔄 Structured logging system



### **⏳ Planned**### **⏳ Planned**

- ⏳ Automated testing- ⏳ Automated testing

- ⏳ Application containerization- ⏳ Application containerization

- ⏳ CI/CD pipeline- ⏳ CI/CD pipeline

- ⏳ Monitoring and alerts- ⏳ Monitoring and alerts



## 👨‍💻 Development## 👨‍💻 Desenvolvimento



### **Useful Commands**### **Comandos Úteis**

```bash```bash

# Development environment# Ambiente desenvolvimento

uv syncuv sync

export ENV_FOR_DYNACONF=developmentexport ENV_FOR_DYNACONF=development



# Start infrastructure# Subir infraestrutura

docker-compose up -ddocker-compose up -d



# Apply migrations# Aplicar migrações

uv run alembic upgrade headuv run alembic upgrade head



# View logs# Ver logs

docker-compose logs postgresdocker-compose logs postgres

docker-compose logs pgadmindocker-compose logs pgadmin

``````



## 📄 License## 📄 Licença



This project is developed for educational and technical demonstration purposes.Este projeto é desenvolvido para fins educacionais e de demonstração técnica.



------



**Developed with enterprise-grade methodology to demonstrate software architecture and data engineering best practices.** 🏆**Desenvolvido com metodologia enterprise-grade para demonstrar boas práticas de arquitetura de software e engenharia de dados.** 🏆