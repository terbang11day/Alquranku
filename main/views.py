from django.shortcuts import render
import requests
from .models import Surat, Audio, Ayat
import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse


def fetch_surat():
    response = requests.get('https://equran.id/api/v2/surat')
    if response.status_code == 200:
        surat_list = response.json()['data']

        for surat_item in surat_list:
            # Mengambil detail surat
            surat_detail_response = requests.get(f'https://equran.id/api/v2/surat/{surat_item["nomor"]}')
            if surat_detail_response.status_code == 200:
                surat_detail = surat_detail_response.json()['data']

                # Membuat dan menyimpan instance Surat
                surat, created = Surat.objects.get_or_create(
                    nomor=surat_detail['nomor'],
                    defaults={
                        'nama': surat_detail['nama'],
                        'nama_latin': surat_detail['namaLatin'],
                        'jumlah_ayat': surat_detail['jumlahAyat'],
                        'tempat_turun': surat_detail['tempatTurun'],
                        'arti': surat_detail['arti'],
                        'deskripsi': surat_detail['deskripsi']
                    }
                )

                # Membuat dan menyimpan instance Audio
                for key, link in surat_detail['audioFull'].items():
                    Audio.objects.get_or_create(
                        surat=surat,
                        versi=key,
                        defaults={'link': link}
                    )

                # Membuat dan menyimpan instance Ayat
                for ayat_item in surat_detail['ayat']:
                    Ayat.objects.get_or_create(
                        surat=surat,
                        nomor_ayat=ayat_item['nomorAyat'],
                        defaults={
                            'teks_arab': ayat_item['teksArab'],
                            'teks_latin': ayat_item['teksLatin'],
                            'teks_indonesia': ayat_item['teksIndonesia']
                        }
                    )




def json_surat(request):
    data = Surat.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_ayat(request):
    data = Ayat.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_audio(request):
    data = Audio.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_main(request):
    semua_surat = Surat.objects.all()
    semua_ayat = Ayat.objects.all()
    semua_audio = Audio.objects.all()
    
    context = {
        'semua_surat': semua_surat,
        'semua_ayat': semua_ayat,
        'semua_audio': semua_audio,
    }

    return render(request, 'main.html', context)

