from functools import wraps
from rest_framework.serializers import ValidationError


def validate_serializer(serializer_class):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            data = request.data or request.GET
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator
