from . import permissions as p
from . import serializers as s
import reviews.models as m
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)


class CreateDestroyListViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = m.Category.objects.all()
    serializer_class = s.CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (p.IsAdminOrReadOnly,)


class GenresViewSet(CreateDestroyListViewSet):
    queryset = m.Genre.objects.all()
    serializer_class = s.GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (p.IsAdminOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = m.Title.objects.all()
    permission_classes = (p.IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return s.TitleCreateSerializer
        return s.TitleListSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        p.IsAuthorOrReadOnly,
    ]

    queryset = m.Review.objects.all()
    serializer_class = s.ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        p.IsAuthorOrReadOnly,
    ]
    serializer_class = s.CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(m.Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(m.Review, pk=review_id)
        )
