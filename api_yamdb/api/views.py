from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

import reviews.models as m
from . import serializers as s
from . import permissions as p



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = m.Category.objects.all()
    serializer_class = s.CategorySerializer
    filter_backends = (filters.OrderingFilter,)
    pagination_class = LimitOffsetPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class GenresViewSet(viewsets.ModelViewSet):
    queryset = m.Genres.objects.all()
    serializer_class = s.GenresSerializer
    filter_backends = (filters.OrderingFilter,)
    pagination_class = LimitOffsetPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = m.Titles.objects .all()
    serializer_class = s.TitlesSerializer
    filter_backends = (filters.OrderingFilter,)
    pagination_class = LimitOffsetPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


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
