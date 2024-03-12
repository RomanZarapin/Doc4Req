from cerberus import Validator
from middleware.errors import CustomHTTPException


async def validate(data, schema):
    v = Validator()

    if v.validate(data, schema) is False:
        print(v.errors)
        raise CustomHTTPException({
            'message': 'Validation errors',
            'errors': v.errors,
            'code': 'VALIDATION_EXCEPTION'
        }, 422)

    return True
