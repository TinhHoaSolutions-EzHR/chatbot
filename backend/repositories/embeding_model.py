from sqlalchemy.orm import Session
from typing import List, Tuple

from models.embedding_model import EmbeddingModel
from models.error import APIError

class EmbeddingModelRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_embedding_models(self, limit: int, offset: int) -> Tuple[List[EmbeddingModel], APIError | None]:
        """
        Get all embedding models
        """
        try:
            embedding_models = self.db_session.query(EmbeddingModel).limit(limit).offset(offset).all()
            if embedding_models:
                return embedding_models, None
            else:
                return [], APIError(detail="Embedding models not found")
        except Exception as e:
            return [], APIError(detail=str(e))
    
    def get_embedding_model(self, id: int) -> Tuple[EmbeddingModel, APIError | None]:
        """
        Get embedding model by id
        """
        try:
            embedding_model = self.db_session.query(EmbeddingModel).filter(EmbeddingModel.id == id).first()
            if embedding_model:
                return embedding_model, None
            else:
                return None, APIError(detail="Embedding model not found")
        except Exception as e:
            return None, APIError(detail=str(e))
    
    def create_embedding_model(self, embedding_model: EmbeddingModel) -> APIError | None:
        """
        Create embedding model
        """
        try:
            self.db_session.add(embedding_model)
            self.db_session.commit()
            return None
        except Exception as e:
            self.db_session.rollback()
            return APIError(detail=str(e))
            
    def update_embedding_model(self, id: int, embedding_model: EmbeddingModel) -> APIError | None:
        """
        Update embedding model
        """
        try:
            self.db_session.query(EmbeddingModel).filter(EmbeddingModel.id == id).update(embedding_model.model_dump())
            self.db_session.commit()
            return None
        except Exception as e:
            self.db_session.rollback()
            return APIError(detail=str(e))
    
    def delete_embedding_model(self, id: int) -> APIError | None:
        """
        Delete embedding model
        """
        try:
            self.db_session.query(EmbeddingModel).filter(EmbeddingModel.id == id).delete()
            self.db_session.commit()
            return None
        except Exception as e:
            self.db_session.rollback()
            return APIError(detail=str(e))