from django.urls import path
from .views import PollList, PollDetail, Vote

urlpatterns = [
    path('polls/', PollList.as_view(), name='poll_list'),
    path('polls/<int:pk>/', PollDetail.as_view(), name='poll_detail'),
    path('polls/<int:poll_id>/choices/<int:choice_id>/vote/', Vote.as_view(), name='vote'),
]
