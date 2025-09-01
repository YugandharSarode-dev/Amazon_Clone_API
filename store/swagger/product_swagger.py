from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
import json

# Existing responses
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

response_not_found = {
    'message': ['Product not found'],
    'code': 404,
    'success': False,
    'data': {}
}

# Decorator for list endpoint with query params
swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('sort_by', IN_QUERY, description='Sort by id, price, name', type='string'),
        Parameter('sort_direction', IN_QUERY, description='ascending or descending', type='string'),
        Parameter('keyword', IN_QUERY, description='Search by name or description', type='string'),
        Parameter('page', IN_QUERY, description='Page number', type='integer'),
        Parameter('limit', IN_QUERY, description='Number of items per page', type='integer'),
        Parameter('min_price', IN_QUERY, description='Filter products with price >= min_price', type='number'),
        Parameter('max_price', IN_QUERY, description='Filter products with price <= max_price', type='number'),
        Parameter('category', IN_QUERY, description='Filter by category id', type='integer'),
    ],
    responses={
        '200': json.dumps(response_list),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },
    operation_id='list_products',
    operation_description='API to list products with optional filters, sorting, and pagination',
)

# Decorators for other endpoints
swagger_auto_schema_post = swagger_auto_schema(
    operation_description="Create a new Product"
)

swagger_auto_schema_update = swagger_auto_schema(
    operation_description="Update an existing Product"
)

swagger_auto_schema_delete = swagger_auto_schema(
    operation_description="Delete a Product"
)

swagger_auto_schema = swagger_auto_schema(
    operation_description="Retrieve a Product by ID"
)
