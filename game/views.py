from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
import json, jwt
from connect4.settings import SECRET_KEY, GAME_COUNT
from datetime import datetime
from .models import *

def authenticate(request):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'token':
        msg = "No Authorization Token Found in Header"
        return {'type' : 'failed', 'message' : msg}

    if len(auth) == 1:
        msg = 'Invalid token header. No credentials provided.'
        return {'type' : 'failed', 'message' : msg}
    elif len(auth) > 2:
        msg = 'Invalid token header'
        return {'type' : 'failed', 'message' : msg}

    try:
        token = auth[1]
        if token=="null":
            msg = 'Null token not allowed'
            return {'type' : 'failed', 'message' : msg}
    except UnicodeError:
        msg = 'Invalid token header. Token string should not contain invalid characters.'
        return {'type' : 'failed', 'message' : msg}

    return authenticate_credentials(token)

def authenticate_credentials(token):
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except:
        return {'type' : 'failed', 'message' : 'Invalid token'}
    name1 = payload['name1']
    name2 = payload['name2']
    msg = {'Error': "Token mismatch",'status' :"401"}
    try:
        game = Game.objects.get(name1=name1, name2=name2)
           
    except :
        return {'type' : 'failed', 'message' : 'Invalid token'}

    return {'type' : 'success', 'name1' : name1, 'name2' : name2, 'game' : game}

def update_game(column, mat, move):
    print(move)
    print(column)
    for i in range(6):
        if i == 5:
            if mat[i][column] == '_':
                print("I am here")
                mat[i][column] = move
                break
        else:
            if mat[i][column] == '_' and mat[i+1][column] != '_':
                mat[i][column] = move
                break
    return mat

def check_if_winner(mat, move, winner):

    row = len(mat)
    col = len(mat[0])
    # check row wise winner
    for i in range(row):
        for j in range(col-3):
            if mat[i][j] == move and mat[i][j+1] == move and mat[i][j+2] == move and mat[i][j+3] == move:
                winner.append([i, j])
                winner.append([i, j+1])
                winner.append([i, j+2])
                winner.append([i, j+3])
                return True

    # check column wise winner
    for i in range(col):
        for j in range(row-3):
            if mat[j][i] == move and mat[j+1][i] == move and mat[j+2][i] == move and mat[j+3][i] == move:
                winner.append([j, i])
                winner.append([j+1, i])
                winner.append([j+2, i])
                winner.append([j+3, i])
                return True

    # check left diagonal winner
    for i in range(row-3):
        for j in range(3, col):
            if mat[i][j] == move and mat[i+1][j-1] == move and mat[i+2][j-2] == move and mat[i+3][j-3] == move:
                winner.append([i, j])
                winner.append([i+1, j-1])
                winner.append([i+2, j-2])
                winner.append([i+3, j-3])
                return True

    # check right diagonal winner
    for i in range(row-3):
        for j in range(col-3):
            if mat[i][j] == move and mat[i+1][j+1] == move and mat[i+2][j+2] == move and mat[i+3][j+3] == move:
                winner.append([i, j])
                winner.append([i+1, j+1])
                winner.append([i+2, j+2])
                winner.append([i+3, j+3])
                return True

    return False

def print_mat(mat):
    row = len(mat)
    col = len(mat[0])
    for i in range(row):
        for j in range(col):
            print(mat[i][j], end=' ')
        print()

class StartNewGame(APIView):
    def post(self, request):
        username1 = request.data.get('name1')
        username2 = request.data.get('name2')
        # GAME_COUNT += 1
        payload = {
            'name1' : username1,
            'name2' : username2,
            # 'game_count' : GAME_COUNT,
            'time' : str(datetime.now())
        }
        mat = list()
        for i in range(6):
            row = list()
            for j in range(7):
                row.append('_')
            row = '$'.join(row)
            mat.append(row)
        mat = '&'.join(mat)
        try:
            game = Game.objects.get(name1=username1, name2=username2)
            game.mat = mat
            game.save()
        except:
            game = Game(name1=username1, name2=username2, mat=mat)
            game.save()
        token = jwt.encode(payload, SECRET_KEY)
        return Response({
            'status' : HTTP_201_CREATED,
            'token' : token,
            'response' : 'Ready'
        })

class MakeMove(APIView):
    def post(self, request):
        response = authenticate(request)
        if response['type'] == 'success':
            game = response['game']
            mat = game.mat
            mat = mat.split('&')
            mat = [row.split('$') for row in mat]
            is_valid_move = True
            is_winner = False
            column = request.data.get('column')
            color = request.data.get('color')
            move = 'R' if color == 'red' else 'Y'
            # If column given by user is not between 0 - 6, it is an invalid move
            if column < 0 or column > 6:
                is_valid_move = False
            elif mat[0][column] != '_':
                is_valid_move = False
            else:
                mat = update_game(column, mat, move)
                print_mat(mat)
                winner = list()
                is_winner = check_if_winner(mat, move, winner)
                print(winner)
                mat = ['$'.join(row) for row in mat]
                mat = '&'.join(mat)
                game.mat = mat
                game.save()

            if is_valid_move:
                if is_winner:
                    return Response({
                        'status' :HTTP_200_OK,
                        'response' : 'Valid',
                        'name1' : response['name1'],
                        'name2' : response['name2'],
                        'winner' : color,
                        'positions' : winner
                    })
                else:
                    return Response({
                        'status' :HTTP_200_OK,
                        'response' : 'Valid',
                        'name1' : response['name1'],
                        'name2' : response['name2'],
                        'winner' : ''
                    })
            else:
                return Response({
                    'status' :HTTP_400_BAD_REQUEST,
                    'response' : 'Invalid Move'
                })
        else:
            return Response({
                'status' : HTTP_400_BAD_REQUEST,
                'response' : response['message']
            })

class GetAllMoves(APIView):
    def get(self, request):
        response = authenticate(request)
        if response['type'] == 'success':
            game = response['game']
            mat = game.mat
            mat = mat.split('&')
            mat = [row.split('$') for row in mat]
            return Response({
                'status' :HTTP_200_OK,
                'response' : mat
            })
        else:
            return Response({
                'status' : HTTP_400_BAD_REQUEST,
                'response' : response['message']
            })  