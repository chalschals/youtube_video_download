from django.shortcuts import render
from django.views.generic import TemplateView
from downloader.forms import YoutubeForm1, YoutubeForm2
from pytube import YouTube
from downloader.models import Youtube
from django.conf import settings
import shutil
import os
from os import walk
from pathlib import Path
# Create your views here.


def YoutubeDownloader(request):
    error = 0
    error_msg = ""
    resolutions = []
    formObj = YoutubeForm1()
    level = 1
    table_id = 0
    link = ""
    finalLink = None
    if request.method == 'POST':
        print("====================", request.POST.get('level'))
        if request.POST.get('level') == "1":
            print("====================INSIDE==1")
            data = request.POST
            formObj = YoutubeForm1(data)
            if formObj.is_valid():
                table_id = formObj.save()
                URL = data.get('url')
                try:
                    yt = YouTube(URL)
                    for n in yt.streams.filter(progressive=True):
                        if n.resolution:
                            resolutions.append(
                                int(n.resolution.replace("p", '')))
                    resolutions = list(set(resolutions))
                    resolutions.sort()
                    level = 2
                    VIDEO_IDENTITY = URL.split(
                        "/")[len(URL.split("/"))-1].replace("watch?v=", "")
                    link = "https://www.youtube.com/embed/"+VIDEO_IDENTITY
                except:
                    table_id = 0
                    level = 1
                    error = 1
                    error_msg = "Invalid URL"
                    resolutions = []
                    link = ""
                    finalLink = None

        if request.POST.get('level') == "2":
            data = request.POST
            videoOrAudio = data.get("video_or_audio")
            resolution = data.get("resolution")
            resolution = resolution+"p"
            tableId = data.get("table_id")
            URL = data.get('url')
            VIDEO_IDENTITY = URL.split(
                "/")[len(URL.split("/"))-1].replace("watch?v=", "")
            OUT_PATH = os.path.join(
                settings.MEDIA_DIR, VIDEO_IDENTITY)  # FULL PATH
            if Path(OUT_PATH).exists() and Path(OUT_PATH).is_dir():
                shutil.rmtree(OUT_PATH)
            try:
                yt = YouTube(URL)
                if videoOrAudio == "audio":
                    yt.streams.filter(
                        mime_type="audio/mp4").first().download(OUT_PATH)
                    ytIns = Youtube.objects.get(id=tableId)
                    ytIns.sourcttype = videoOrAudio
                    ytIns.save()
                else:
                    yt.streams.filter(
                        mime_type="video/mp4", resolution=resolution).first().download(OUT_PATH)
                    ytIns = Youtube.objects.get(id=tableId)
                    ytIns.resolution = resolution
                    ytIns.sourcttype = videoOrAudio
                    ytIns.save()
                files = None
                for (dirpath, dirnames, filenames) in walk(OUT_PATH):
                    files = filenames[0]
                if files:
                    finalLink = os.path.join(
                        settings.MEDIA_URL, VIDEO_IDENTITY, files)
            except:
                table_id = 0
                level = 1
                error = 1
                error_msg = "Invalid URL"
                resolutions = []
                link = ""
                finalLink = None
    return render(
        request,
        'index.html',
        context={'form': formObj,
                 "error": error,
                 "error_msg": error_msg,
                 "resolutions": resolutions,
                 "level": level,
                 "table_id": table_id,
                 "link": link,
                 "finalLink": finalLink
                 })
