from django.db import models

class Surat(models.Model):
    nomer = models.IntegerField(unique=True)
    nama = models.TextField(max_length=100)
    nama_latin = models.TextField(max_length=100)
    jumlah_ayat = models.IntegerField()
    tempat_turun = models.TextField()
    arti = models.TextField()
    deskripsi = models.TextField()  # Perbaiki penulisan nama field

class Audio(models.Model):
    surat = models.ForeignKey(Surat, on_delete=models.CASCADE, related_name='audio_links')
    versi = models.CharField(max_length=100)
    link = models.URLField(max_length=200)

class Ayat(models.Model):
    surat = models.ForeignKey(Surat, on_delete=models.CASCADE, related_name='ayat_links')  # Perbaiki kaitannya
    nomer_ayat = models.IntegerField()
    teks_arab = models.TextField()
    teks_latin = models.TextField()  # Perbaiki penulisan nama field
    teks_indo = models.TextField()  # Perbaiki penulisan nama field
