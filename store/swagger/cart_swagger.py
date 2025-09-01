from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
import json

response_list = {
    'message': ['Ok'],
    'code': 200,
    'success': True,
    'data': []
}

response_post = {
    'message': ['Cart item added'],
    'code': 201,
    'success': True,
    'data': {}
}

response_update = {
    'message': ['Cart item updated'],
    'code': 200,
    'success': True,
    'data': {}
}

response_delete = {
    'message': ['Cart item deleted'],
    'code': 200,
    'success': True,
    'data': {}
}

response_unauthenticate = {
    'message': ["Authentication credentials were not provided."],
    'code': 403,
    'success': False,
    'data': {}
}

response_unauthorized = {
    'message': ["Unauthorized"],
    'code': 401,
    'success': False,
    'data': {}
}

response_bad_request = {
    'message': ['Invalid request'],
    'code': 400,
    'success': False,
    'data': {}
}

response_not_found = {
    'message': ['Cart item not found'],
    'code': 404,
    'success': False,
    'data': {}
}

# List decorator
swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('page', IN_QUERY, description='Page number', type='integer'),
        Parameter('limit', IN_QUERY, description='Number of items per page', type='integer'),
        Parameter('keyword', IN_QUERY, description='Search keyword', type='string'),
        Parameter('sort_by', IN_QUERY, description='Sort by id or product name', type='string'),
        Parameter('sort_direction', IN_QUERY, description='ascending or descending', type='string'),
    ],
    responses={
        '200': json.dumps(response_list),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='list cart',
    operation_description='API to list cart items with optional filters, sorting, and pagination',
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        '201': json.dumps(response_post),
        '400': json.dumps(response_bad_request),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='create cart item',
    operation_description='API to add items to cart'
)

swagger_auto_schema_update = swagger_auto_schema(
    responses={
        '200': json.dumps(response_update),
        '400': json.dumps(response_bad_request),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized)
    },
    operation_id='update cart item',
    operation_description='API to update cart item quantity'
)

swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='delete cart item',
    operation_description='API to delete single cart item'
)

swagger_auto_schema_bulk_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='bulk delete cart items',
    operation_description='API to delete multiple cart items'
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        '200': json.dumps(response_post),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='get cart item',
    operation_description='API to fetch single cart item'
)
