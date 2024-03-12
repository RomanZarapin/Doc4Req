import jwt
from datetime import datetime
from middleware.errors import CustomHTTPException
from services.users.user_services import get_auth_user_data
from services.irc import irc


async def get_access_token(user_data: dict, exp: datetime, secret: str) -> str:
    return jwt.encode({
            'iat': int(round((datetime.now()).timestamp())),
            'exp': int(round(exp.timestamp())),
            'token_type': 'access',
            'user_id': user_data['id'],
            'company_id': user_data['company_id'],
            'role': user_data['role']
        },
        secret,
        algorithm='HS256'
    )


async def get_refresh_token(user_data: dict, exp: datetime, secret: str) -> str:
    return jwt.encode({
            'exp': int(round(exp.timestamp())),
            'token_type': 'refresh',
            'user_id': user_data['id'],
        },
        secret,
        algorithm='HS256'
    )


async def get_access_from_refresh_token(token: str, exp: datetime, secret: str) -> str:
    data = jwt.decode(token, secret, algorithms=['HS256'])
    user_id = data.get('user_id')
    if not user_id:
        raise CustomHTTPException(irc['ACCESS_DENIED'])
    user_data = await get_auth_user_data(user_id=user_id)
    token_data = {
        'token_type': 'access',
        'iat': int(round((datetime.now()).timestamp())),
        'exp': int(round(exp.timestamp())),
        'user_id': user_id,
        'company_id': user_data['company_id'],
        'role': user_data['role']
    }
    return jwt.encode(token_data, secret, algorithm='HS256')
