from django.db import transaction
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_serielizer_error
from store.model.category_model import Categories
from store.serializers.category_serializer import CategorySerializer


class CategoryView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = CategorySerializer
    singular_name = 'Category'
    model_class = Categories.objects
    # authentication_classes = [OAuth2Authentication]
    # permission_classes = [IsAuthenticated]

    search_fields = ['name', 'description']

    def get_object(self):
        try:
            pk = self.kwargs.get('id')
            return self.model_class.get(pk=pk)
        except:
            return None

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        sp1 = transaction.savepoint()
        try:
            req_data = request.data.copy()
            serializer = self.serializer_class(data=req_data)
            if serializer.is_valid():
                category = serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_created(
                    self,
                    data=self.serializer_class(category).data,
                    message=self.singular_name + ' created successfully.'
                )

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        sp1 = transaction.savepoint()
        try:
            instance = self.get_object()
            if not instance:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found.')

            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_ok(
                    self,
                    data=serializer.data,
                    message=self.singular_name + ' updated successfully.'
                )

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance:
                resp_dict = self.transform_single(instance)
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found.')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.model_class.all()
            resp_list = [self.transform_single(item) for item in queryset]
            return ApiResponse.response_ok(self, data=resp_list)

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not instance:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found.')

            instance.delete()
            return ApiResponse.response_ok(self, message=self.singular_name + ' deleted.')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def transform_single(self, instance):
        return {
            'category_id': instance.id,
            'name': instance.name,
            'description': instance.description
        }
