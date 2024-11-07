# EzHr-Chatbot API Server

This API server powers the EzHr-Chatbot, a Large Language Model (LLM)-based assistant, built with FastAPI and LlamaIndex.

## Prerequisites

A PostgreSQL database is required to store data. For testing purposes, you can set up a PostgreSQL instance using Docker:

```bash
docker run --name postgres -e POSTGRES_PASSWORD=123 -e POSTGRES_USER=root -e POSTGRES_DB=ezhr_chatbot -p 5432:5432 -d postgres:15.2-alpine

# Create the required table
docker exec -it postgres psql -U root -d ezhr_chatbot -c "CREATE TABLE embedding_model (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT NOT NULL, provider VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, deleted_at TIMESTAMP NULL);"
```

### Environment Variables

Set the following environment variables for database connectivity:

```bash
export POSTGRES_USER=root
export POSTGRES_PASSWORD=123
export POSTGRES_DB=ezhr_chatbot
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

### Installing Dependencies and Running the Server

Ensure Python 3.10 or later is installed. Install dependencies and start the server as follows:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 5000
```

## Project Structure

The project follows a structured flow:

1. **Define Endpoints**: `routers/v1/`
2. **Service Logic**: `services/`
3. **Database Operations**: `repositories/`
4. **Model Definitions**: `models/`

### Workflow Breakdown

- **Endpoints**: Define API routes in `routers/v1/`. For example, an endpoint for embedding models might be defined in `routers/v1/embedding_model.py`.

    ```python
    router = APIRouter(prefix="/embedding_model", tags=["embedding_model"])

    @router.get("/", response_model=APIResponse)
    async def get_embedding_models(db_session: Session = Depends(get_session)):
        pass
    ```

- **Service Layer**: Extract parameters in the controller and delegate logic to the services, located in the `services/` directory. Each method in the service class corresponds to a controller endpoint. Example:

    ```python
    class EmbeddingModelService:
        def __init__(self, db_session: Session):
            self.db_session = db_session

        def get_embedding_models(self) -> Tuple[List[EmbeddingModel], APIError | None]:
            return EmbeddingModelRepository(self.db_session).get_embedding_models()
    ```

- **Repository Layer**: Perform database operations within repositories, found in the `repositories/` directory. Here’s an example repository method:

    ```python
    class EmbeddingModelRepository:
        def __init__(self, db_session: Session):
            self.db_session = db_session

        def get_embedding_models(self) -> Tuple[List[EmbeddingModel], APIError | None]:
            try:
                embedding_models = self.db_session.query(EmbeddingModel).all()
                return embedding_models, None
            except Exception as e:
                logger.error(f"Error getting embedding models: {e}")
                return [], APIError(err_code=20001)
    ```

- **Model Definitions**: Define database entities in the `models/` directory. Example of a model definition:

    ```python
    class EmbeddingModel(Base):
        __tablename__ = "embedding_model"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        name = Column(String, index=True)
        description = Column(String)
        provider = Column(String)
        created_at = Column(DateTime, default=datetime.now)
        updated_at = Column(DateTime, default=datetime.now)
        deleted_at = Column(DateTime, default=None, nullable=True)
    ```

This structured approach maintains a clean separation of concerns, making the API server more maintainable and scalable.