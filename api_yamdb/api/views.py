import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters, permissions, viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

import reviews.models as m
from . import serializers as s
from . import permissions as p
from users.models import User


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


class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = s.UserSerializer
    permission_classes = (p.IsPost,)

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        confirmation_code = uuid.uuid4().hex
        serializer.save(confirmation_code=confirmation_code)

        send_mail(
            'Code for get token',
            confirmation_code,
            'bestTeam@ever.com',
            [email],
            fail_silently=False,
        )


class TokenView(APIView):
    permission_classes = (p.IsPost,)

    def post(self, request):
        serializer = s.TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.initial_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.initial_data.get('confirmation_code')

            if user.confirmation_code != confirmation_code:
                return Response({"token": "incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"token": f"{access_token}"})
