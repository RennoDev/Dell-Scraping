# 🖥️ Dell Products Scraper# 🖥️ Dell Products Scraper# 🖥️ Dell Products Scraper



> Professional web scraper for collecting and storing Dell products with complete data pipeline.



## 📋 About the Project> Professional web scraper for collecting and storing Dell products with complete data pipeline.> Professional web scraper for collecting and storing Dell products with complete data pipeline.



Web scraping system developed to collect product information from Dell's official website, process the data, and store it in a PostgreSQL database with management interface.



### 🎯 Objectives## 📋 About the Project## 📋 About the Project

- **Automated collection** of Dell products (model, price, links)

- **Structured storage** in PostgreSQL

- **Robust pipeline** for data processing

- **Scalable architecture** with containerizationWeb scraping system developed to collect product information from Dell's official website, process the data, and store it in a PostgreSQL database with management interface.Web scraping system developed to collect product information from Dell's official website, process the data, and store it in a PostgreSQL database with management interface.



## 🛠️ Technology Stack



### **Core Technologies**### 🎯 Objectives### 🎯 Objectives

- **Python 3.13** - Main programming language

- **PostgreSQL 16** - Relational database- **Automated collection** of Dell products (model, price, links)- **Automated collection** of Dell products (model, price, links)

- **Docker & Docker Compose** - Containerization

- **Structured storage** in PostgreSQL- **Structured storage** in PostgreSQL

### **Web Scraping**

- **Playwright 1.55+** - Modern web automation- **Robust pipeline** for data processing- **Robust pipeline** for data processing

- **Rich 14.1+** - Professional CLI interface

- **Scalable architecture** with containerization- **Scalable architecture** with containerization

### **Database & ORM**

- **SQLAlchemy 2.0+** - ORM and data abstraction

- **Alembic 1.16+** - Schema migrations

- **psycopg2-binary 2.9+** - PostgreSQL driver## 🛠️ Technology Stack## 🛠️ Technology Stack



### **Configuration & Data**

- **Dynaconf 3.2+** - Configuration management

- **Pydantic 2.11+** - Data validation### **Core Technologies**### **Core Technologies**

- **Pandas 2.3+** - Data processing

- **Python 3.13** - Main programming language- **Python 3.13** - Main programming language

### **Development Tools**

- **uv** - Modern dependency manager- **PostgreSQL 16** - Relational database- **PostgreSQL 16** - Relational database

- **Structlog 25.4+** - Structured logging

- **Tenacity 9.1+** - Automatic retry- **Docker & Docker Compose** - Containerization- **Docker & Docker Compose** - Containerization

- **pgAdmin 4** - Database administration interface



## 🏗️ System Architecture

### **Web Scraping**### **Web Scraping**

```mermaid

graph TB- **Playwright 1.55+** - Modern web automation- **Playwright 1.55+** - Modern web automation

    A[Dell Website] --> B[Playwright Scraper]

    B --> C[Data Processor]- **Rich 14.1+** - Professional CLI interface- **Rich 14.1+** - Professional CLI interface

    C --> D[Pydantic Validator]

    D --> E[SQLAlchemy Models]

    E --> F[PostgreSQL]

    F --> G[pgAdmin Interface]### **Database & ORM**### **Database & ORM**

    

    H[Dynaconf] --> B- **SQLAlchemy 2.0+** - ORM and data abstraction- **SQLAlchemy 2.0+** - ORM and data abstraction

    H --> E

    I[Rich CLI] --> B- **Alembic 1.16+** - Schema migrations- **Alembic 1.16+** - Schema migrations

    J[Alembic] --> F

```- **psycopg2-binary 2.9+** - PostgreSQL driver- **psycopg2-binary 2.9+** - PostgreSQL driver



### **Separation of Concerns**

```

📁 src/dell/### **Configuration & Data**### **Configuration & Data**

├── 📂 config/          # Configurations (Dynaconf)

├── 📂 models/          # SQLAlchemy Models- **Dynaconf 3.2+** - Configuration management- **Dynaconf 3.2+** - Configuration management

├── 📂 scraper/         # Web scraping logic

├── 📂 services/        # Business rules  - **Pydantic 2.11+** - Data validation- **Pydantic 2.11+** - Data validation

├── 📂 repositories/    # Data access

└── 📂 utils/           # General utilities- **Pandas 2.3+** - Data processing- **Pandas 2.3+** - Data processing

```



## 🗄️ Database Schema

### **Development Tools**### **Development Tools**

### **Main Tables**

- **uv** - Modern dependency manager- **uv** - Modern dependency manager

#### **Categories**

- `id` (PK) - Unique identifier- **Structlog 25.4+** - Structured logging- **Structlog 25.4+** - Structured logging

- `name` - Category name (e.g., "Laptops")

- `slug` - URL-friendly identifier- **Tenacity 9.1+** - Automatic retry- **Tenacity 9.1+** - Automatic retry

- `created_at`, `updated_at`, `is_active` - Audit fields

- **pgAdmin 4** - Database administration interface- **pgAdmin 4** - Database administration interface

#### **Products**  

- `id` (PK) - Unique identifier

- `model` - Dell product model

- `price` - Price (DECIMAL 10,2)## 🏗️ System Architecture## 🏗️ System Architecture

- `link` - Product URL on Dell website

- `category_id` (FK) - Reference to Categories

- `created_at`, `updated_at`, `is_active` - Audit fields

```mermaid```mermaid

### **Relationships**

- **1:N** - One category can have multiple productsgraph TBgraph TB

- **Foreign Key** with referential integrity

    A[Dell Website] --> B[Playwright Scraper]    A[Dell Website] --> B[Playwright Scraper]

## ⚙️ Secure Configuration

    B --> C[Data Processor]    B --> C[Data Processor]

### **Multi-Environment**

```toml    C --> D[Pydantic Validator]    C --> D[Pydantic Validator]

# settings.toml

[development]    D --> E[SQLAlchemy Models]    D --> E[SQLAlchemy Models]

debug = true

scraping_delay = 1    E --> F[PostgreSQL]    E --> F[PostgreSQL]



[production]      F --> G[pgAdmin Interface]    F --> G[pgAdmin Interface]

debug = false

scraping_delay = 3        

```

    H[Dynaconf] --> B    H[Dynaconf] --> B

### **Secrets Management**

```toml    H --> E    H --> E

# .secrets.toml (git ignored)

[default]    I[Rich CLI] --> B    I[Rich CLI] --> B

POSTGRES_PASSWORD = "secure_password"

POSTGRES_USER = "dell_user"    J[Alembic] --> F    J[Alembic] --> F

```

``````

### **Environment Variables**

```bash

# .env (git ignored)

ENV_FOR_DYNACONF=development### **Separation of Concerns**### **Separation of Concerns**

POSTGRES_DB=dell_db

POSTGRES_USER=dell_user``````

POSTGRES_PASSWORD=dev_password_123

```📁 src/dell/📁 src/dell/



## 🐳 Containerization├── 📂 config/          # Configurations (Dynaconf)├── 📂 config/          # Configurations (Dynaconf)



### **Docker Compose Services**├── 📂 models/          # SQLAlchemy Models├── 📂 models/          # SQLAlchemy Models

- **PostgreSQL 16-Alpine** - Main database

- **pgAdmin 4** - Web administration interface├── 📂 scraper/         # Web scraping logic├── 📂 scraper/         # Web scraping logic

- **Persistent volumes** - Data preservation

- **Isolated network** - Container communication├── 📂 services/        # Business rules  ├── 📂 services/        # Business rules  



## 🚀 Setup and Installation├── 📂 repositories/    # Data access├── 📂 repositories/    # Data access



### **Prerequisites**└── 📂 utils/           # General utilities└── 📂 utils/           # General utilities

- Python 3.13+

- Docker & Docker Compose``````

- uv package manager



### **1. Clone and Setup**

```bash## 🗄️ Database Schema## 🗄️ Database Schema

git clone <repository>

cd dell

cp .env.example .env

# Edit credentials in .env### **Main Tables**### **Main Tables**

```



### **2. Install Dependencies**

```bash#### **Categories**#### **Categories**

uv sync

uv run playwright install chromium- `id` (PK) - Unique identifier- `id` (PK) - Unique identifier

```

- `name` - Category name (e.g., "Laptops")- `name` - Category name (e.g., "Laptops")

### **3. Start Infrastructure**

```bash- `slug` - URL-friendly identifier- `slug` - URL-friendly identifier

docker-compose up -d postgres

docker-compose up -d pgadmin  # Optional- `created_at`, `updated_at`, `is_active` - Audit fields- `created_at`, `updated_at`, `is_active` - Audit fields

```



### **4. Setup Database**

```bash#### **Products**  #### **Products**  

# Apply migrations

uv run alembic upgrade head- `id` (PK) - Unique identifier- `id` (PK) - Unique identifier



# Verify created tables- `model` - Dell product model- `model` - Dell product model

docker exec -it dell_postgres psql -U dell_user -d dell_db -c "\dt"

```- `price` - Price (DECIMAL 10,2)- `price` - Price (DECIMAL 10,2)



### **5. Access pgAdmin (Optional)**- `link` - Product URL on Dell website- `link` - Product URL on Dell website

- **URL:** http://localhost:8080

- **Email:** admin@dell.com- `category_id` (FK) - Reference to Categories- `category_id` (FK) - Reference to Categories

- **Password:** admin_dev_123

- `created_at`, `updated_at`, `is_active` - Audit fields- `created_at`, `updated_at`, `is_active` - Audit fields

**Configure connection:**

- **Host:** postgres

- **Port:** 5432

- **Database:** dell_db### **Relationships**### **Relationships**

- **Username:** dell_user  

- **Password:** [your_password_from_.env]- **1:N** - One category can have multiple products- **1:N** - One category can have multiple products



## 📊 Development Methodology- **Foreign Key** with referential integrity- **Foreign Key** with referential integrity



### **Bottom-Up Approach**

1. **🏗️ Infrastructure First** - Docker, PostgreSQL, configurations

2. **🗄️ Database Layer** - Models, relationships, migrations  ## ⚙️ Secure Configuration## ⚙️ Secure Configuration

3. **⚙️ Configuration Management** - Dynaconf, secrets, environments

4. **🕸️ Business Logic** - Scrapers, services, pipeline

5. **💻 User Interface** - CLI, commands, feedback

6. **🧪 Testing & Quality** - Tests, validations### **Multi-Environment**### **Multi-Environment**

7. **🐳 Deployment** - Complete containerization

```toml```toml

### **Applied Principles**

- **Separation of Concerns** - Each layer has single responsibility# settings.toml# settings.toml

- **Database First** - Well-defined schema before logic

- **Configuration Management** - Organized environments and secrets[development][development]

- **Containerization** - Reproducible infrastructure

- **Type Safety** - Pydantic + SQLAlchemy for validationdebug = truedebug = true



## 🔄 Database Migrationsscraping_delay = 1scraping_delay = 1



```bash

# Generate new migration

uv run alembic revision --autogenerate -m "Description of change"[production]  [production]  



# Apply migrationsdebug = falsedebug = false

uv run alembic upgrade head

scraping_delay = 3scraping_delay = 3

# View history

uv run alembic history``````



# Rollback if needed  

uv run alembic downgrade -1

```### **Secrets Management**### **Secrets Management**



## 📈 Project Status```toml```toml



### **✅ Implemented**# .secrets.toml (git ignored)# .secrets.toml (git ignored)

- ✅ Complete Docker infrastructure

- ✅ SQLAlchemy models with relationships[default][default]

- ✅ Alembic migrations system

- ✅ Secure multi-environment configurationPOSTGRES_PASSWORD = "secure_password"POSTGRES_PASSWORD = "secure_password"

- ✅ Functional PostgreSQL database

- ✅ Configured pgAdmin interfacePOSTGRES_USER = "dell_user"POSTGRES_USER = "dell_user"



### **🔄 In Development**``````

- 🔄 Playwright web scraper

- 🔄 Processing pipeline

- 🔄 Rich CLI interface

- 🔄 Structured logging system### **Environment Variables**### **Environment Variables**



### **⏳ Planned**```bash```bash

- ⏳ Automated testing

- ⏳ Application containerization# .env (git ignored)# .env (git ignored)

- ⏳ CI/CD pipeline

- ⏳ Monitoring and alertsENV_FOR_DYNACONF=developmentENV_FOR_DYNACONF=development



## 👨‍💻 DevelopmentPOSTGRES_DB=dell_dbPOSTGRES_DB=dell_db



### **Useful Commands**POSTGRES_USER=dell_userPOSTGRES_USER=dell_user

```bash

# Development environmentPOSTGRES_PASSWORD=dev_password_123POSTGRES_PASSWORD=dev_password_123

uv sync

export ENV_FOR_DYNACONF=development``````



# Start infrastructure

docker-compose up -d

## 🐳 Containerization## 🐳 Containerization

# Apply migrations

uv run alembic upgrade head



# View logs### **Docker Compose Services**### **Docker Compose Services**

docker-compose logs postgres

docker-compose logs pgadmin- **PostgreSQL 16-Alpine** - Main database- **PostgreSQL 16-Alpine** - Main database

```

- **pgAdmin 4** - Web administration interface- **pgAdmin 4** - Web administration interface

## 📄 License

- **Persistent volumes** - Data preservation- **Persistent volumes** - Data preservation

This project is developed for educational and technical demonstration purposes.

- **Isolated network** - Container communication- **Isolated network** - Container communication

---



**Developed with enterprise-grade methodology to demonstrate software architecture and data engineering best practices.** 🏆
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