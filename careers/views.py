from rest_framework import mixins, viewsets

from .models import Post
from .pagination import PostPagination
from .serializers import PostSerializer, PostUpdateSerializer


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    list   → GET  /careers/
    create → POST /careers/
    partial_update → PATCH /careers/{id}/
    destroy → DELETE /careers/{id}/
    """

    queryset = Post.objects.all()
    pagination_class = PostPagination
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "partial_update":
            return PostUpdateSerializer
        return PostSerializer
