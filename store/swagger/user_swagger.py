from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
import json

# Response templates
response_list = {'message': ['Ok'], 'code': 200, 'success': True, 'data': []}
response_get = {'message': ['Ok'], 'code': 200, 'success': True, 'data': {}}
response_post = {'message': ['User created'], 'code': 201, 'success': True, 'data': {}}
response_update = {'message': ['User updated'], 'code': 200, 'success': True, 'data': {}}
response_delete = {'message': ['User deleted'], 'code': 200, 'success': True, 'data': {}}
response_unauthenticate = {'message': ["Authentication credentials were not provided."], 'code': 403, 'success': True, 'data': {}}
response_unauthorized = {'message': ["Unauthorized"], 'code': 401, 'success': True, 'data': {}}
response_bad_request = {'message': ['Invalid request'], 'code': 400, 'success': True, 'data': {}}
response_not_found = {'message': ['User not found'], 'code': 404, 'success': True, 'data': {}}

# List users
swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('page', IN_QUERY, description='Page number', type='int'),
        Parameter('limit', IN_QUERY, description='Page size', type='int'),
        Parameter('keyword', IN_QUERY, description='Search keyword', type='char'),
        Parameter('status', IN_QUERY, description='Filter by status', type='char'),
    ],
    responses={
        '200': json.dumps(response_list),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='list users',
    operation_description='API to list users'
)

# Create user with role field
swagger_auto_schema_post = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='Mobile number'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'role': openapi.Schema(type=openapi.TYPE_INTEGER, description='User role: 2 = staff, 3 = provider')
        },
        required=['username', 'password', 'role']
    ),
    responses={
        '201': json.dumps(response_post),
        '400': json.dumps(response_bad_request),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='create user',
    operation_description='API to create new user'
)

# Update user
swagger_auto_schema_update = swagger_auto_schema(
    responses={
        '200': json.dumps(response_update),
        '400': json.dumps(response_bad_request),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized)
    },
    operation_id='update user',
    operation_description='API to update user'
)

# Delete user
swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='delete user',
    operation_description='API to delete single user'
)

# Bulk delete users
swagger_auto_schema_bulk_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='bulk delete users',
    operation_description='API to delete multiple users'
)

# Get single user
swagger_auto_schema = swagger_auto_schema(
    responses={
        '200': json.dumps(response_get),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='get user',
    operation_description='API to fetch single user'
)
