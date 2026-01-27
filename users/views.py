from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.middleware.csrf import get_token
import random
import string


def create_group_code():
    code_str = string.ascii_letters + string.digits
    code = ''.join(random.choices(code_str, k=6))
    return code


def create_group():
    group = ''
    print('OI')
    try:
        code = create_group_code()
        group = Group.objects.get(name=code)
    except Group.DoesNotExist:
        try:
            print(code)
            new_group = Group.objects.create(
                name=code
            )
            print('TESTE')
            return new_group
        except Exception as error:
            raise error

    return create_group()


@api_view(['GET'])
def csrf_view(request):
    return Response(
        {'csrfToken': get_token(request)}
    )


@api_view(['POST'])
def create_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response(
                {"error": 'Dados insuficientes'},
                status=400
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        print('TESTE222')
        user.groups.add(create_group())
    except IntegrityError:
        return Response(
            {'error': 'Usuario já existe'},
            status=400
        )

    return Response(
        {'message': 'Usuario criado com sucesso'},
        status=201
    )


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Credenciais insuficientes'},
            status=400
        )

    user = authenticate(
        request,
        username=username, 
        password=password
    )

    if user is None:
        return Response(
            {'error': 'Credenciais invalidas'},
            status=401
        )

    login(
        request,
        user,
    )

    return Response(
        {'message': 'Login realizado com sucesso'},
        status=200
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response(
        {'message': 'Logout realizado com sucesso'},
        status=200
    )



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user

    if 'username' in request.data:
        user.username = request.data['username']

    if 'password' in request.data:
        user.set_password(request.data['password'])

    if 'email' in request.data:
        user.email = request.data['email']

    user.save()
    return Response(
        {'message': 'Dados atualizados com sucesso'},
        status=200
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'room': user.groups.values_list('name')
    }

    return Response(
        data,
        status=200
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user

    user.delete()

    return Response(
        status=204
    )
