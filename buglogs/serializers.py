from rest_framework import serializers
from buglogs.models import Log, Project, LogStatusAndCatagoryStatistic


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id',
                  'ngay_ghi_nhan',
                  'user_ghi_nhan',
                  'mo_ta_log',
                  'moi_truong',
                  'vi_tri',
                  'loai_log',
                  'trang_thai_log',
                  'dev_thuc_hien',
                  'ngay_test_lai',
                  'du_an')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id',
                  'ten_du_an')
