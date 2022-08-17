import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

import reviews.models as m
from users.models import User

from . import permissions as p
from . import serializers as s
from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet


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
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    search_fields = ('genre__slug',)
    filterset_fields = ('genre__slug',)
    permission_classes = (p.IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return s.TitleCreateSerializer
        return s.TitleListSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (
        p.HasRightsOrReadOnly,
    )

    serializer_class = s.ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(m.Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(m.Title, pk=title_id)
        )

    def perform_update(self, serializer):
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        p.HasRightsOrReadOnly,
    )
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = s.UserSerializer
    permission_classes = (p.IsPost,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        return Response('serializer.data', status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (p.IsPost,)

    def post(self, request):
        serializer = s.TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.initial_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.initial_data.get(
                'confirmation_code'
            )

            if user.confirmation_code != confirmation_code:
                return Response(
                    {"token": "incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"token": f"{access_token}"})
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = m.User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, p.IsAdmin,)
    serializer_class = s.UserListSerializer
    filter_backends = (filters.OrderingFilter,)


class MeViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = s.UserEditSerializer
    pagination_class = None

    def get_object(self):
        username = self.request.user.username
        return get_object_or_404(User, username=username)

    def perform_update(self, serializer):
        serializer.save()
