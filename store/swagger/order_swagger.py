from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
import json

response_list = {'message': ['Ok'], 'code': 200, 'success': True, 'data': []}
response_get = {'message': ['Ok'], 'code': 200, 'success': True, 'data': {}}
response_post = {'message': ['Order placed'], 'code': 201, 'success': True, 'data': {}}
response_update = {'message': ['Order updated'], 'code': 200, 'success': True, 'data': {}}
response_delete = {'message': ['Order deleted'], 'code': 200, 'success': True, 'data': {}}
response_unauthenticate = {'message': ["Authentication credentials were not provided."], 'code': 403, 'success': True, 'data': {}}
response_unauthorized = {'message': ["Unauthorized"], 'code': 401, 'success': True, 'data': {}}
response_bad_request = {'message': ['Invalid request'], 'code': 400, 'success': True, 'data': {}}
response_not_found = {'message': ['Order not found'], 'code': 404, 'success': True, 'data': {}}

swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('page', IN_QUERY, description='Page number', type='int'),
        Parameter('limit', IN_QUERY, description='Page size', type='int'),
        Parameter('keyword', IN_QUERY, description='Search keyword', type='char'),
        Parameter('status', IN_QUERY, description='Filter by status', type='char'),
    ],
    responses={'200': json.dumps(response_list),'403': json.dumps(response_unauthenticate),'401': json.dumps(response_unauthorized),'404': json.dumps(response_not_found)},
    operation_id='list orders',
    operation_description='API to list orders'
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={'201': json.dumps(response_post),'400': json.dumps(response_bad_request),'403': json.dumps(response_unauthenticate),'401': json.dumps(response_unauthorized),'404': json.dumps(response_not_found)},
    operation_id='create order',
    operation_description='API to place order from cart or directly'
)

swagger_auto_schema_update = swagger_auto_schema(
    responses={'200': json.dumps(response_update),'400': json.dumps(response_bad_request),'403': json.dumps(response_unauthenticate),'401': json.dumps(response_unauthorized)},
    operation_id='update order',
    operation_description='API to update order status'
)

swagger_auto_schema_delete = swagger_auto_schema(
    responses={'200': json.dumps(response_delete),'403': json.dumps(response_unauthenticate),'401': json.dumps(response_unauthorized),'404': json.dumps(response_not_found)},
    operation_id='delete order',
    operation_description='API to delete single order'
)

swagger_auto_schema_bulk_delete = swagger_auto_schema(
    responses={'200': json.dumps(response_delete),'403': json.dumps(response_unauthenticate),'401': json.dumps(response_unauthorized),'404': json.dumps(response_not_found)},
    operation_id='bulk delete orders',
    operation_description='API to delete multiple orders'
)

swagger_auto_schema = swagger_auto_schema(
    responses={'200': json.dumps(response_get),'403': json.dumps(response_unauthenticate),'401': json.dumps(response_unauthorized),'404': json.dumps(response_not_found)},
    operation_id='get order',
    operation_description='API to fetch single order'
)
