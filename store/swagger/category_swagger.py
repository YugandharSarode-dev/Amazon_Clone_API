from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
import json

# Responses
response_list = {
    'message': ['Ok'],
    'code': 200,
    'success': True,
    'data': []
}

response_get = {
    'message': ['Ok'],
    'code': 200,
    'success': True,
    'data': {}
}

response_post = {
    'message': ['Category created successfully.'],
    'code': 201,
    'success': True,
    'data': {}
}

response_update = {
    'message': ['Category updated successfully.'],
    'code': 200,
    'success': True,
    'data': {}
}

response_delete = {
    'message': ['Category deleted successfully.'],
    'code': 200,
    'success': True,
    'data': {}
}

response_unauthorized = {
    'message': ["Only superusers can perform this action."],
    'code': 401,
    'success': False,
    'data': {}
}

response_unauthenticate = {
    'message': ["Authentication credentials were not provided."],
    'code': 403,
    'success': False,
    'data': {}
}

response_not_found = {
    'message': ['Category not found'],
    'code': 404,
    'success': False,
    'data': {}
}

# List decorator
swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('keyword', IN_QUERY, description='Search by name or description', type='string'),
        Parameter('page', IN_QUERY, description='Page number', type='integer'),
        Parameter('limit', IN_QUERY, description='Items per page', type='integer')
    ],
    responses={
        '200': json.dumps(response_list),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found)
    },
    operation_id='list categories',
    operation_description='API to list all categories'
)

# Create decorator (superuser only)
swagger_auto_schema_post = swagger_auto_schema(
    responses={
        '201': json.dumps(response_post),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '400': json.dumps({'message': ['Invalid request'], 'code': 400, 'success': False, 'data': {}})
    },
    operation_id='create category',
    operation_description='API to create category (Superuser only)'
)

# Update decorator (superuser only)
swagger_auto_schema_update = swagger_auto_schema(
    responses={
        '200': json.dumps(response_update),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
        '400': json.dumps({'message': ['Invalid request'], 'code': 400, 'success': False, 'data': {}})
    },
    operation_id='update category',
    operation_description='API to update category (Superuser only)'
)

# Delete decorator (superuser only)
swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found)
    },
    operation_id='delete category',
    operation_description='API to delete category (Superuser only)'
)

# Retrieve decorator
swagger_auto_schema = swagger_auto_schema(
    responses={
        '200': json.dumps(response_get),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found)
    },
    operation_id='get category',
    operation_description='API to fetch single category'
)
