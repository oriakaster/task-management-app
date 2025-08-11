# app/middleware/error_handler.py
import uuid
import logging
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError
from app.core.errors import AppError, DatabaseError  

logger = logging.getLogger(__name__)

def _json(status: int, code: str, message: str,
          *, fields: dict | None = None, details=None,
          headers=None, error_id: str | None = None) -> JSONResponse:
    """input: status, code, message, fields=None, details=None, headers=None, error_id=None
       output: JSONResponse
       Creates a JSON response with the given status, code, message, and optional fields, details, headers, and error_id."""
    body = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    
    if details is not None:
        body["error"]["details"] = details
    if fields is not None:
        body["error"]["fields"] = fields
    if error_id is not None:
        body["error"]["errorId"] = error_id

    return JSONResponse(status_code=status, content=body, headers=headers)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """input: request, call_next
           output: JSONResponse or response from call_next
           Handles errors during request processing and returns appropriate JSON responses."""
        try:
            response = await call_next(request)

        except AppError as e:
            # Domain/business errors (e.g., USERNAME_TAKEN, TASK_FORBIDDEN, etc.)
            return _json(e.http_status, e.code, e.message, details=getattr(e, "details", None))

        except RequestValidationError as e:
            # 422 validation errors -> put field map under error.fields
            field_map: dict[str, list[str]] = {}
            for err in e.errors():
                loc = err.get("loc", [])
                key = ".".join(str(x) for x in (loc[1:] if loc and loc[0] in {"body","query","path","header"} else loc)) or "request"
                field_map.setdefault(key, []).append(err["msg"])
            return _json(422, "VALIDATION_ERROR", "Invalid input.", fields=field_map)

        except HTTPException as e:
            # Preserve status + headers; normalize message into nested error
            detail = e.detail
            msg = detail if isinstance(detail, str) else (detail.get("message") if isinstance(detail, dict) else str(detail))
            code = (detail.get("error") if isinstance(detail, dict) else None) or "HTTP_ERROR"
            return _json(e.status_code, code, msg or "HTTP error", headers=e.headers)

        except JWTError:
            # Token issues -> 401 INVALID_TOKEN
            return _json(401, "INVALID_TOKEN", "Could not validate credentials",
                         headers={"WWW-Authenticate": "Bearer"})

        except SQLAlchemyError:
            # DB issues -> 500 with errorId for log correlation
            err_id = str(uuid.uuid4())
            logger.exception("SQLAlchemyError %s at %s %s", err_id, request.method, request.url.path)
            return _json(500, "DATABASE_ERROR", "Something went wrong. Try again later.", error_id=err_id)

        except Exception:
            # Catch-all -> 500 with errorId
            err_id = str(uuid.uuid4())
            logger.exception("Unhandled %s at %s %s", err_id, request.method, request.url.path)
            return _json(500, "INTERNAL_SERVER_ERROR", "Unexpected error. Try again later.", error_id=err_id)
        
        path = request.url.path
        if path not in ("/docs", "/redoc", "/openapi.json") and response.status_code in (404, 405):
            if response.status_code == 404:
                return _json(404, "HTTP_ERROR", "Not found")
            if response.status_code == 405:
                return _json(405, "HTTP_ERROR", "Method not allowed")

        return response
