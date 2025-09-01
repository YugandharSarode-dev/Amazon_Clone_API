from django.db import transaction
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_pagination_resp, get_serielizer_error
from store.model.product_model import Product
from store.serializers.product_serializer import ProductSerializer
from utility.role import is_superuser, is_provider

# swagger imports
from ..swagger.product_swagger import (
    swagger_auto_schema_list, swagger_auto_schema_post,
    swagger_auto_schema_update, swagger_auto_schema_delete,
    swagger_auto_schema
)


class ProductView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = ProductSerializer
    singular_name = 'Product'
    model_class = Product.objects
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    search_fields = ['name', 'description']

    def get_object(self):
        try:
            pk = self.kwargs.get('id')
            return self.model_class.get(pk=pk)
        except:
            return None

    def _check_permission(self, user, instance=None, action='create'):
        if is_superuser(user):
            return True

        if is_provider(user):
            if action == 'create':
                return True
            if instance and instance.created_by_id == user.id:
                return True

        return False

    @swagger_auto_schema_post
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        if not self._check_permission(request.user, action='create'):
            return ApiResponse.response_unauthorized(self, message='You do not have permission to add product.')

        sp1 = transaction.savepoint()
        try:
            req_data = request.data.copy()

            # Set creator automatically
            req_data['created_by'] = request.user.id

            serializer = self.serializer_class(data=req_data)
            if serializer.is_valid():
                product = serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_created(
                    self,
                    data=self.serializer_class(product).data,
                    message=self.singular_name + ' created successfully.'
                )

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @swagger_auto_schema_update
    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found.')

        if not self._check_permission(request.user, instance=instance, action='update'):
            return ApiResponse.response_unauthorized(self, message='You do not have permission to update product.')

        sp1 = transaction.savepoint()
        try:
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_ok(self, data=serializer.data, message=self.singular_name + ' updated successfully.')

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @swagger_auto_schema
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance:
                resp_dict = self.transform_single(instance)
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found.')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        try:
            query_params = request.query_params
            queryset = self.model_class.all()

            # Provider sees only their products
            if is_provider(request.user):
                queryset = queryset.filter(created_by_id=request.user.id)

            keyword = query_params.get('keyword')
            if keyword:
                queryset = queryset.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))

            category_id = query_params.get('category')
            if category_id:
                queryset = queryset.filter(category_id=category_id)

            min_price = query_params.get('min_price')
            max_price = query_params.get('max_price')
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)

            sort_by = query_params.get('sort_by') or 'id'
            if query_params.get('sort_direction') == 'descending':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)

            response_data = [self.transform_single(obj) for obj in queryset]
            paginated_data = get_pagination_resp(response_data, request)
            return ApiResponse.response_ok(self, data=paginated_data)

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @swagger_auto_schema_delete
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found.')

        if not self._check_permission(request.user, instance=instance, action='delete'):
            return ApiResponse.response_unauthorized(self, message='You do not have permission to delete product.')

        try:
            instance.delete()
            return ApiResponse.response_ok(self, message=self.singular_name + ' deleted.')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def transform_single(self, instance):
        return {
            'product_id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'stock': instance.stock,
            'category': instance.category.name,
            'created_by': instance.created_by.username,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }
