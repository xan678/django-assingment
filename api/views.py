from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny

from api.models import Post
from api.serializers import PostSerializer
from common.views import (PostCreateModelMixin, GetListModelMixin,
                          GetRetrieveModelMixin, DeleteDestroyModelMixin, PutUpdateModelMixin)


class PostView(PostCreateModelMixin, GetListModelMixin, GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = ((MultiPartParser,))  # added to support form data in swagger

    def get_queryset(self):
        return super(PostView, self).get_queryset().select_related('user')

    def post(self, request, *args, **kwargs):
        """create own post"""
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """return list of post"""
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """user set as current user"""
        serializer.save(user=self.request.user)


class PostDetailView(GetRetrieveModelMixin, DeleteDestroyModelMixin, PutUpdateModelMixin, GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = super(PostDetailView, self).get_queryset().select_related('user')
        if self.request.user.is_authenticated and self.request.method != 'GET':
            """user can edit or delete own posts"""
            qs = qs.filter(user=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        """return detail of post"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """to update content of own post"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """to delete own post"""
        return self.destroy(request, *args, **kwargs)
