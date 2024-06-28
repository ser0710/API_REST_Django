from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ValidationError
from watchlist_app.models import WatchList, StreamPlataform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlataformSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from watchlist_app.api.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchlistPagination, WatchListLOPagination, WatchListLCPagination

# ----------------------------- Generic class-based view: ------------------

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated] # object level permission
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle] # if we want to define an scope without creating a new file (throttling.py)
    throttle_scope = 'review-detail'
    
class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating =  (movie.avg_rating + serializer.validated_data['rating'])/2
        movie.number_rating = movie.number_rating + 1
        movie.save()
        serializer.save(watchlist=movie, review_user=review_user)
        
        
# ----------------------------- Mixin: ------------------

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# ----------------------------- Function based view: ------------------
# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method =='GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#     elif request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------------- Class based view: ------------------
class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
 
        
        
class StreamPlataformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        plataform = StreamPlataform.objects.all()
        serializer = StreamPlataformSerializer(plataform, many=True) # context={'request': request} add if want to work with HyperlinkedRelatedField or HyperlinkedModelSerializer
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlataformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlataformDetailAV(APIView):
    def get(self, request, pk):
        try:
            plataform = StreamPlataform.objects.get(pk=pk)
        except StreamPlataform.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlataformSerializer(plataform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        plataform = StreamPlataform.objects.get(pk=pk)
        serializer = StreamPlataformSerializer(plataform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        plataform = StreamPlataform.objects.get(pk=pk)
        plataform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

# ----------------------------- view set: ------------------ # works fine with router prefer use it when have simple tasks
# class StreamPlataformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlataform.objects.all()
#         serializer = StreamPlataformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlataform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlataformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlataformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# ----------------------------- model view set: ------------------

class StreamPlataformVS(viewsets.ModelViewSet): # Access to all methods (ModelViewSet), Read only method: (ReadOnlyViewSet)
    queryset = StreamPlataform.objects.all()
    serializer_class = StreamPlataformSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
    
# ----------------------------- filtering ---------------------
class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username) # fk..?
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username) # fk..?
    
    
# ---------------------------- only a test class ----------------------
# class WatchList(generics.ListAPIView): # this is an example of filter
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['title', 'plataform__name']


# class WatchList(generics.ListAPIView): # this is an example of search
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['^title', '=plataform__name'] # use = to exact match, (^ starts with)
    
# class WatchList(generics.ListAPIView): # this is an example of ordering
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['avg_rating', 'plataform__name']


# ------------------------- ordering --------------------------

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
    pagination_class = WatchListLCPagination # WatchlistPagination WatchListLOPagination 
    