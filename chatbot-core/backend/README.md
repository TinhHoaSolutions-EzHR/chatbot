# EzHr-Chatbot API Server

This API server powers the EzHr-Chatbot, a Large Language Model (LLM)-based assistant, built with FastAPI and LlamaIndex.

## Project Structure

The project follows a structured flow:

1. **Define Endpoints**: `routers/v1/`
2. **Service Logic**: `services/`
3. **Database Operations**: `repositories/`
4. **Model Definitions**: `models/`

### Workflow Breakdown

- **Endpoints**: Define API routes in `routers/v1/`. For example, an endpoint for embedding models might be defined in `routers/v1/embedding_model.py`.

  ```python
  router = APIRouter(prefix="/embedding_models", tags=["embedding_models"])

  @router.get("/", response_model=APIResponse, status_code=status.HTTP_200_OK)
  async def get_embedding_models(db_session: Session = Depends(get_db_session)):
      # Other logic
      embedding_models, err = EmbeddingModelService(db_session).get_embedding_models()
      # Other logic
  ```

- **Service Layer**: Extract parameters in the controller and delegate logic to the services, located in the `services/` directory. Each method in the service class corresponds to a controller endpoint. Example:

  ```python
  class EmbeddingModelService:
      def __init__(self, db_session: Session):
          self._db_session = db_session

      def get_embedding_models(self) -> Tuple[List[EmbeddingModel], Optional[APIError]]:
          return EmbeddingModelRepository(db_session=self._db_session).get_embedding_models()
  ```

- **Repository Layer**: Perform database operations within repositories, found in the `repositories/` directory. Here’s an example repository method:

  ```python
  class EmbeddingModelRepository:
      def __init__(self, db_session: Session):
          self._db_session = db_session

      def get_embedding_models(self) -> Tuple[List[EmbeddingModel], Optional[APIError]]:
          try:
              embedding_models = self._db_session.query(EmbeddingModel).all()
              return embedding_models, None
          except Exception as e:
              logger.error(f"Error getting embedding models: {e}", exc_info=True)
              return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
  ```

- **Model Definitions**: Define database entities in the `models/` directory. Example of a model definition:

  ```python
  class EmbeddingModel(Base):
      __tablename__ = "embedding_models"

      id = Column(Integer, primary_key=True, index=True, autoincrement=True)
      name = Column(String, index=True)
      description = Column(String)
      provider = Column(String)
      created_at = Column(DateTime, default=datetime.now)
      updated_at = Column(DateTime, default=datetime.now)
      deleted_at = Column(DateTime, default=None, nullable=True)
  ```

This structured approach maintains a clean separation of concerns, making the API server more maintainable and scalable.

## Development Guide

This backend uses FastAPI, Uvicorn, and LlamaIndex.

### Requirements

- Python version 3.11.10 or higher, specified in file `.tool-versions`
- [uv](https://docs.astral.sh/uv/) for package management, installation, and running the server.
- Docker and Docker Compose for container orchestration.

### Setup

1. Clone the repository.

2. Install [uv](https://docs.astral.sh/uv/) >= 0.5.4 and then use it to install all packages.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or if you use asdf
asdf plugin add uv
asdf install uv 0.5.4
asdf local uv 0.5.4
```

NOTE: All packages information is stored in `pyproject.toml`

3. Install [docker](https://docs.docker.com/engine/install/)

4. Install [docker-compose](https://docs.docker.com/compose/install/)

5. Create the environment file from example

```bash
cp .env.example .env.development
```

(Optional) If you want to use [direnv](https://direnv.net/), you can use the .envrc file

```bash
cp .envrc.sample .envrc
direnv allow
```

Then the environment variables from `.env.development` will be loaded and unloaded when you enter and exit the directory.

6. Start the development docker compose

```bash

cd chatbot-core
make build
make up
```

The docker compose will build services and start. The API server will be available at `http://localhost:5000`.

7. (Optional) If you want to run the server locally, you can run the following command:

```bash
uv sync
uv run fastapi dev --port 5000
```

`uv` tool will create a virtual environment and install all the dependencies. The FastAPI server will be available at `http://localhost:5000`.

8. To exec any commands, you can use the following command:

```bash
make exec SERVICES=api-server COMMAND="<your command here>"
```

### Alembic

This project uses Alembic for database migrations. To work with Alembic, first you need to ensure these requirements are met:

1. Develop under docker compose environment.
2. The database connection string is set in the `.env.development` file: `DATABASE_URL`. Default value to `DATABASE_URL="mssql+pyodbc://SA:P%%26ssword123@database:1433/chatbot_core?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"`
3. Running and healthy database service.
4. The `api-server` service is running.
5. Edited one of those models in `backend/app/models/` directory.

To create a new migration, run the following command:

```bash
cd chatbot-core
make alembic-revision "<your migration message here>"
```

This command will create a new migration file in the `backend/alembic/versions/` directory.

To upgrade the database to the latest migration, run the following command:

```bash
cd chatbot-core
make alembic-upgrade-head
```

To downgrade the database to the previous migration, run the following command:

```bash
cd chatbot-core
make exec SERVICES=api-server COMMAND="uv run alembic downgrade -1"
```

### Alembic naming convention

The naming convention for the migration file is as follows:

Example:

- `FK__agent__user`
- `FK__chat_message__chat_session`

### Troubleshooting

#### 1. How to reset alembic

1. Firstly change directory to `chatbot-core`

```bash
cd chatbot-core
```

2. Make down all services

```bash
make down
```

3. Spawn up the database

```bash
make up SERVICES=database
```

Wait the database service to be ready for 10 seconds.

4. Exec the database using dbeaber or data grip, then run the following sql script

```sql
DROP DATABASE chatbot_core;
```

![image](https://github.com/user-attachments/assets/2d86a604-0f2b-4c2b-8155-0b1d14ad09be)

This will drop all existing tables. Will then create later.

5. Startup services

Make sure the `api-server` has the command to run `alembic upgrade head`.

```bash
make up
```

Otherwise, you can run the following command:

```bash
make alembic-upgrade-head
```

6. Check log the service `api-server`, now you will see all the alembic migrations created

```bash
make logs SERVICES=api-server
```

Successful logs:

![image](https://github.com/user-attachments/assets/b8536f78-5a99-4a5c-9535-0ff927be2116)

Example after successfully reset alembic:

![image](https://github.com/user-attachments/assets/b97ec69e-4366-43aa-a4b5-3fac5f43c21f)
