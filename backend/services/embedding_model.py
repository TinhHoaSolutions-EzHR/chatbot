from sqlalchemy.orm import Session
from typing import List, Tuple

from repositories.embeding_model import EmbeddingModelRepository
from models.embedding_model import EmbeddingModel
from models.error import APIError
from utils.logger import LoggerFactory

logger = LoggerFactory(__name__).get_logger()

class EmbeddingModelService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_embedding_models(self, limit: int, offset: int) -> Tuple[List[EmbeddingModel], APIError | None]:
        """
        Get all embedding models
        """
        return EmbeddingModelRepository(db_session=self.db_session).get_embedding_models(
            limit=limit, offset=offset
        )
        
    def get_embedding_model(self, id: int) -> Tuple[EmbeddingModel, APIError | None]:
        """
        Get embedding model by id
        """
        return EmbeddingModelRepository(db_session=self.db_session).get_embedding_model(id=id)
    
    def create_embedding_model(self, embedding_model: EmbeddingModel) -> APIError | None:
        """
        Create embedding model
        """
        err = None
        try:
            # Begin transaction
            self.db_session.begin()
            
            err = EmbeddingModelRepository(db_session=self.db_session).create_embedding_model(embedding_model=embedding_model)
            
            # Commit transaction
            self.db_session.commit()
        except Exception as e:
            # Rollback transaction
            self.db_session.rollback()
            logger.error(f"Error creating embedding model: {e}")
            err = APIError(detail=str(e))
        return err
        
    def update_embedding_model(self, id: int, embedding_model: EmbeddingModel) -> APIError | None:
        """
        Update embedding model
        """
        err = None
        try:
            # Begin transaction
            self.db_session.begin()
            
            err = EmbeddingModelRepository(db_session=self.db_session).update_embedding_model(id=id, embedding_model=embedding_model)
           
            # Commit transaction
            self.db_session.commit()
        except Exception as e:
            # Rollback transaction
            self.db_session.rollback()
            logger.error(f"Error updating embedding model: {e}")
            err = APIError(detail=str(e))
        return err
        
    def delete_embedding_model(self, id: int) -> APIError | None:
        """
        Delete embedding model
        """
        try:
            # Begin transaction
            self.db_session.begin()
            
            err = EmbeddingModelRepository(db_session=self.db_session).delete_embedding_model(id=id)
            
            # Commit transaction
            self.db_session.commit()
        except Exception as e:
            # Rollback transaction
            self.db_session.rollback()
            logger.error(f"Error deleting embedding model: {e}")
            err = APIError(detail=str(e))
        return err