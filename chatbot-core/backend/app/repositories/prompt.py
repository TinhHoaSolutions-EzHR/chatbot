# from typing import Tuple
# from typing import Union
# from sqlalchemy.orm import Session
# from sqlalchemy.sql.elements import ColumnElement
# from app.models.api import APIError
# from app.models.prompt import Prompt
# from app.repositories.base import BaseRepository
# from app.utils.error_handler import ErrorCodesMappingNumber
# from app.utils.logger import LoggerFactory
# logger = LoggerFactory().get_logger(__name__)
# class PromptRepository(BaseRepository):
#     def __init__(self, db_session: Session):
#         """
#         Prompt repository class for handling prompt-related database operations.
#         Args:
#             db_session (Session): Database session
#         """
#         super().__init__(db_session=db_session)
#     def get_prompt_by_criteria(self, criteria: ColumnElement[bool]) -> Tuple[Prompt, Union[APIError, None]]:
#         """
#         Get prompt by criteria
#         Args:
#             criteria (ColumnElement): Criteria to filter prompt
#         Returns:
#             Tuple[Prompt, Union[APIError, None]]: Prompt object and APIError object if any error
#         """
#         if not isinstance(criteria, ColumnElement):
#             raise TypeError(f"Criteria's type should be ColumnElement. Got {type(criteria)}")
#         try:
#             prompt = self._db_session.query(Prompt).filter_by(criteria).first()
#             return prompt, None
#         except Exception as e:
#             logger.error(f"Error occurred while getting prompt by criteria: {e}")
#             return None, ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR
