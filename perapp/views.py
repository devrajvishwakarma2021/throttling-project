
from django.shortcuts import render

# Create your views here.
from django.http.response import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle

# from perapp.throttles import JackRateThrottle

# from  rest_framework.permissions  import IsAuthenticated
# from rest_framework.authentication import SessionAuthentication



# class TodoModelViewSet(viewsets.ModelViewSetiewSet):
#         queryset = Todo.objects.all
#         serializer_class = TodoSerializer
#         authentication_classes = [SessionAuthentication]
#         permission_classes = [IsAuthenticated]


class TodoAPIView(APIView):

    # READ a single Todo
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
        else:
            data = Todo.objects.all()

        serializer = TodoSerializer(data, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = TodoSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Todo Created Successfully',
            'data': serializer.data
        }

        return response

    def put(self, request, pk=None, format=None):
        todo_to_update = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(instance=todo_to_update,data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Todo Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, pk, format=None):
        todo_to_delete =  Todo.objects.get(pk=pk)

        todo_to_delete.delete()

        return Response({
            'message': 'Todo Deleted Successfully'
        })


    from rest_framework.throttling import ScopedRateThrottle


# class PostViewSet(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = serializer.PostSerializer
#     throttle_classes = [JackRateThrottle]
#     http_method_names = ['get']


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    throttle_classes = [UserRateThrottle]
    http_method_names = ['get']

# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = serializer.UserSerializer
#     throttle_classes = [ScopedRateThrottle]
#     throttle_scope = 'jack'