from django.urls import path

from .views import PollList, PollDetail, Vote

urlpatterns = [
    path('', PollList.as_view(), name='poll_list'),
    path('<int:pk>/', PollDetail.as_view(), name='poll_detail'),
    path('<int:poll_id>/choices/<int:choice_id>/vote/', Vote.as_view(), name='vote'),
]
