import datetime
import os
import re
import jwt
from services.irc import irc
from middleware.errors import CustomHTTPException


async def auth_middleware(app, handler):

    async def auth_middleware_handler(request):
        url = str(request.rel_url)
        if re.search('login', url) or re.search('refresh_access_token', url)\
                or re.search('reset_password', url) or re.search('change_password', url)\
                or request.method == 'OPTIONS':
            response = await handler(request)
            return response
        try:
            auth = request.headers.get('AUTHORIZATION', None)
            if auth:
                access_token = auth.split(' ')[1]
                user_data = jwt.decode(access_token, request.app.config['secret'], algorithms=['HS256'])
                if re.search('me', url):
                    response = await handler(request)
                    return response
                role = user_data.get('role')
                if role == 'superadmin' or role == 'tiny':
                    response = await handler(request)
                    return response
                if role == 'rop':
                    company_id_search = re.search(r'rop/\d+', url)
                    if company_id_search:
                        company_id = company_id_search[0].split('/')[-1]
                        if int(company_id) == int(user_data['company_id']):
                            return await handler(request)
                    user_id_search = re.search(r'rop/user/\d+', url)
                    if user_id_search:
                        user_id = user_id_search[0].split('/')[-1]
                        if int(user_id) == int(user_data['user_id']):
                            return await handler(request)
                return CustomHTTPException(irc['Forbidden'], 403)
            else:
                return CustomHTTPException(irc['ACCESS_DENIED'], 401)
        except jwt.exceptions.InvalidTokenError:
            return CustomHTTPException(irc['ACCESS_DENIED'], 401)
    return auth_middleware_handler
