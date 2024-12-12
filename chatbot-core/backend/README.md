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

2. Install [uv](https://docs.astral.sh/uv/) and then use it to install all packages.

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

5. Start the development docker compose

```bash

cd chatbot-core
make up

```

The docker compose will be built and started. The API server will be available at `http://localhost:5000`.

6. (Optional) If you want to run the server locally, you can run the following command:

```bash

uv sync
uv run fastapi dev --port 5000

```

`uv` tool will create a virtual environment and install all the dependencies. The FastAPI server will be available at `http://localhost:5000`.
