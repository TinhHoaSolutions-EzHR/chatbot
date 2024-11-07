from fastapi import status
from typing import Dict, Tuple

from models.api import APIError
from settings import Constants

ERROR_CODES_MAPPING: Dict[int, str] = {
    20001: "Invalid request",
    20002: "Unauthorized request",
    20003: "Forbidden request",
    20004: "Not found",
    20005: "Internal server error",
}


def handle_error(err: APIError) -> Tuple[int, str]:
    """
    Handle error on error code. Return status code and message
    """
    err_code = err.err_code
    if err.err_code not in ERROR_CODES_MAPPING:
        return 500, Constants.NOT_EXISTING_ERROR
    match err_code:
        case err_code if err_code < 20004:
            return status.HTTP_400_BAD_REQUEST, ERROR_CODES_MAPPING[err_code]
        case _:
            return (
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                ERROR_CODES_MAPPING[err_code],
            )
