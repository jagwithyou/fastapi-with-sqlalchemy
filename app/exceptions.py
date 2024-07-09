from sqlalchemy.exc import SQLAlchemyError
from functools import wraps

def async_exception_handler_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            if 'db' in kwargs:
                await kwargs['db'].rollback()
            raise Exception(f"Error occurred while interacting with db: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
    return wrapper