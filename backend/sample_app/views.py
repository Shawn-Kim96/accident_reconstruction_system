from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.http import require_GET

# Create your views here.
@require_GET
def sample_api(request) -> JsonResponse:
    """
    test sample app
    """
    return JsonResponse({"message": "Hello, world!"})