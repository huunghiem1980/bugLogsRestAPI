from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import connection

from buglogs.models import Log, Project
from buglogs.serializers import LogSerializer, ProjectSerializer
from buglogs.models import LogStatusAndCatagoryStatistic
import sys

# Create your views here.


@csrf_exempt
@api_view(['GET', 'POST'])
def log_list(request, project=""):
    if request.method == 'POST':
        try:
            log_data = JSONParser().parse(request)
            log_serializer = LogSerializer(data=log_data)

            if log_serializer.is_valid():
                log_serializer.save()
                print(log_serializer.data)
                response = {
                    'message': "Them moi thanh cong log voi id= %d" % log_serializer.data.get('id'),
                    'data': [log_serializer.data],
                    'error': ""
                }
                return JsonResponse(response, status=status.HTTP_201_CREATED)
            else:
                error = {
                    'message': "Them moi that bai!",
                    'logs': [],
                    'error': log_serializer.errors
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
        except:
            exceptionError = {
                'message': "Them moi that bai!",
                'logs': [],
                'error': "Co loi xay ra"
            }
            return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'GET':
        try:
            if project != "":
                logs = Log.objects.filter(du_an=project)
            else:
                logs = Log.objects.all()

            logs_serializer = LogSerializer(logs, many=True)
            response = {
                'message': "Lay toan bo log thanh cong",
                'data': logs_serializer.data,
                'error': ""
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        except:
            error = {
                'message': "Lay danh sach Log khong thanh cong!",
                'data': "[]",
                'error': "Error"
            }
            return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['PUT', 'DELETE', 'GET'])
def log_detail(request, pk):
    try:
        log = Log.objects.get(pk=pk)
    except Log.DoesNotExist:
        exceptionError = {
            'message': "Khong tim thay Log voi id = %s!" % pk,
            'data': "[]",
            'error': "404 Code - Not Found!"
        }
        return JsonResponse(exceptionError, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            log_data = JSONParser().parse(request)
            log_serializer = LogSerializer(log, data=log_data)
            if log_serializer.is_valid():
                log_serializer.save()
                response = {
                    'message': "Cap nhat thanh cong Log voi id= %s" % pk,
                    'data': [log_serializer.data],
                    'error': ""
                }
                return JsonResponse(response)

            response = {
                'message': "Cap nhat that bai Log voi id = %s" % pk,
                'data': [log_serializer.data],
                'error': log_serializer.errors
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            exceptionError = {
                'message': "Cap nhat that bai Log voi id = %s!" % pk,
                'data': [log_serializer.data],
                'error': "Internal Error!"
            }
            return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        print('Dang xoa Log voi id = %s' % pk)
        log.delete()
        log_serializer = LogSerializer(log)
        response = {
            'message': "Xoa thanh cong Log voi id = %s" % pk,
            'data': [log_serializer.data],
            'error': ""
        }
        return JsonResponse(response)

    elif request.method == 'GET':
        log_serializer = LogSerializer(log)
        response = {
            'message': "Lay thanh cong Log voi id = %s" % pk,
            'data': [log_serializer.data],
            'error': ""
        }
        return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def project_list(request):
    try:
        projects = Project.objects.all()
        projects_serializer = ProjectSerializer(projects, many=True)
        response = {
            'message': "Lay toan bo dự án thanh cong",
            'data': projects_serializer.data,
            'error': ""
        }
        return JsonResponse(response, status=status.HTTP_200_OK)
    except:
        error = {
            'message': "Lay danh sach dự án khong thanh cong!",
            'data': "[]",
            'error': "Error"
        }
        return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def projectStatistic(request, project=""):
    try:
        query = """DECLARE @DynamicPivotQuery AS NVARCHAR(MAX)
DECLARE @ColumnName AS NVARCHAR(MAX)

--Get distinct values of the PIVOT Column
SELECT @ColumnName= ISNULL(@ColumnName + ',','') + QUOTENAME(loai_log)
FROM (SELECT DISTINCT loai_log FROM buglogs_log) as colTable

--Prepare the PIVOT query using the dynamic
SET @DynamicPivotQuery =
N'select * from
(
	select trang_thai_log,loai_log
	from buglogs_log where du_an_id=''""" + project + """''
) src
pivot (
	count(loai_log)
	for loai_log in (' + @ColumnName + ')) desTable';

	--Execute the Dynamic Pivot Query
EXEC sp_executesql @DynamicPivotQuery"""

        with connection.cursor() as cursor:
            cursor.execute(query)
            # columns = [col[0] for col in cursor.description]
            columns = ["trang_thai_log",
                       "bug",
                       "yeu_cau_moi",
                       "yeu_cau_thay_doi",
                       "khong_phai_bug"]
            rows = cursor.fetchall()
            statistic = [dict(zip(columns, row)) for row in rows]

            response = {
                'message': "Lay du lieu thanh cong",
                'data': statistic,
                'error': ""
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
    except:
        print("loi ne", sys.exc_info()[0])
        error = {
            'message': "Lay du lieu khong thanh cong!",
            'data': "[]",
            'error': "Error"
        }
        return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
