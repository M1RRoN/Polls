from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer
from django.conf import settings
import redis
import json
import pika

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def update_poll_in_redis(poll_id):
    poll = Poll.objects.get(id=poll_id)
    poll_serializer = PollSerializer(poll)
    poll_json = json.dumps(poll_serializer.data)
    r.set(poll_id, poll_json)
    return poll_json


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class Vote(generics.GenericAPIView):
    serializer_class = ChoiceSerializer

    def post(self, request, poll_id, choice_id):
        choice = get_object_or_404(Choice, pk=choice_id, poll_id=poll_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        choice.votes += 1
        choice.save()
        update_poll_in_redis(poll_id)
        return Response(status=status.HTTP_200_OK)
