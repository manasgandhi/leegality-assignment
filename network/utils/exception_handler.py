from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


def get_object_or_json404(klass, *args, **kwargs):
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404:
        raise NotFound({"error": klass.__name__ + " not found!"})


def custom_error(msg):
    return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)
