from django.shortcuts import get_object_or_404
from watchlist.models import WatchList, StreamPlatform, Review
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination

class WatchListAV(APIView):
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post (self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class MovieDetailAV(APIView):
    # permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    # permission_classes = [IsAdminOrReadOnly]

class StreamPlatformAV(APIView):
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True,
                                              context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist_id=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [ScopedRateThrottle]

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewCreateThrottle]
    # throttle_scope = 'review-detail'

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,
                                                review_user=review_user)
        if review_queryset.exists():
            raise ValidationError('you have already reviewed this movie')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating +
                                    serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = username)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']