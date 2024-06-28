from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_details # Function based view: 1
from watchlist_app.api.views import (WatchDetailAV, WatchListAV, StreamPlataformAV, StreamPlataformDetailAV, 
                                     ReviewList, ReviewDetail, ReviewCreate, StreamPlataformVS, UserReview,
                                     WatchListGV
                                    )
router = DefaultRouter()
router.register('stream', StreamPlataformVS, basename='streamplatform')

urlpatterns = [
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>', movie_details, name='movie-detail') 1
    
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-detail'),
    path('list2/', WatchListGV.as_view(), name='movie-list2'),
    
    path('', include(router.urls)),
    
    # path('stream/', StreamPlataformAV.as_view(), name='stream'), # without router 
    # path('stream/<int:pk>', StreamPlataformDetailAV.as_view(), name='stream-detail'),
    
    # path('review/', ReviewList.as_view(), name='review-list'), # list all the reviews.... but what happen if you want reviews for an specific plataform 
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-list'),
    
    # path('stream/<int:pk>/review/', ReviewList.as_view(), name='review-detail'), # reviews for a particular movie 
    # path('stream/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    # path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review-detail') # access individual review
    
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'), # reviews for a particular movie 
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'), # access individual review
    # path('reviews/<str:username>/', UserReview.as_view(), name='user-review-detail')
    path('reviews/', UserReview.as_view(), name='user-review-detail')
    
    

]