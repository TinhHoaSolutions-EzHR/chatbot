from sqlalchemy.orm import Session
from typing import List, Tuple

from models.embedding_model import EmbeddingModel
from models.api import APIError

from utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class EmbeddingModelRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_embedding_models(self) -> Tuple[List[EmbeddingModel], APIError | None]:
        """
        Get all embedding models
        """
        try:
            embedding_models = self.db_session.query(EmbeddingModel).all()
            return embedding_models, None
        except Exception as e:
            logger.error(f"Error getting embedding models: {e}")
            return [], APIError(err_code=20001)

    def get_embedding_model(self, id: int) -> Tuple[EmbeddingModel, APIError | None]:
        """
        Get embedding model by id
        """
        try:
            embedding_model = (
                self.db_session.query(EmbeddingModel)
                .filter(EmbeddingModel.id == id)
                .first()
            )
            return embedding_model, None
        except Exception as e:
            logger.error(f"Error getting embedding model: {e}")
            return None, APIError(err_code=20001)

    def create_embedding_model(
        self, embedding_model: EmbeddingModel
    ) -> APIError | None:
        """
        Create embedding model
        """
        try:
            self.db_session.add(embedding_model)
            self.db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error creating embedding model: {e}")
            self.db_session.rollback()
            return APIError(err_code=20001)

    def update_embedding_model(
        self, id: int, embedding_model: EmbeddingModel
    ) -> APIError | None:
        """
        Update embedding model
        """
        try:
            self.db_session.query(EmbeddingModel).filter(
                EmbeddingModel.id == id
            ).update(embedding_model.model_dump())
            self.db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error updating embedding model: {e}")
            self.db_session.rollback()
            return APIError(err_code=20001)

    def delete_embedding_model(self, id: int) -> APIError | None:
        """
        Delete embedding model
        """
        try:
            self.db_session.query(EmbeddingModel).filter(
                EmbeddingModel.id == id
            ).delete()
            self.db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error deleting embedding model: {e}")
            self.db_session.rollback()
            return APIError(err_code=20001)
