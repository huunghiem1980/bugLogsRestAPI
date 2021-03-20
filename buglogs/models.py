from django.db import models

# Create your models here.


class Project(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    ten_du_an = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ten_du_an


class Log(models.Model):
    ngay_ghi_nhan = models.DateTimeField(blank=True, null=True)
    user_ghi_nhan = models.TextField(blank=True, null=True)
    mo_ta_log = models.TextField(blank=True, null=True)
    moi_truong = models.CharField(max_length=10, blank=True, null=True)
    vi_tri = models.TextField(blank=True, null=True)
    loai_log = models.IntegerField(blank=True, null=True)
    trang_thai_log = models.IntegerField(blank=True, null=True)
    dev_thuc_hien = models.TextField(blank=True, null=True)
    ngay_test_lai = models.TextField(blank=True, null=True)

    du_an = models.ForeignKey(
        Project, on_delete=models.CASCADE, default="TDCN")

    def __str__(self):
        return self.mo_ta_log


class LogStatusAndCatagoryStatistic:
    def __init__(self, trang_thai, bug, yeu_cau_moi, yeu_cau_thay_doi, khong_phai_bug):
        self.trang_thai = trang_thai
        self.bug = bug
        self.yeu_cau_moi = yeu_cau_moi
        self.yeu_cau_thay_doi = yeu_cau_thay_doi
        self.khong_phai_bug = khong_phai_bug
