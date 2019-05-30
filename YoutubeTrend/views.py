import os
import time
import xml.etree.ElementTree as ET
import isodate
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
from YoutubeTrend.models import Operation, Video

CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = "AIzaSyA-6hhIeoI-kyvWmFPGwjrKaYrgGS3D-yo"


def get_authenticated_service(developerKey):
    return build(API_SERVICE_NAME, API_VERSION, developerKey=developerKey)


def main_search(service, q, max_results, order, token, location, location_radius,developerKey):
    remain = 0
    if max_results > 50:
        remain = max_results-50
        max_results = 50
    search_response = service.search().list(
        q=q,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",  # Part signifies the different types of data you want
        maxResults=max_results,
        location=location,
        locationRadius=location_radius,
        key=developerKey

    ).execute()

    result_list = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            response = service.videos().list(
                part='statistics, snippet,contentDetails',
                id=search_result['id']['videoId']).execute()
            result_list.append(response)
    if remain > 0:
        search_response = service.search().list(
            q=q,
            type="video",
            pageToken=search_response['nextPageToken'],
            order=order,
            part="id,snippet",  # Part signifies the different types of data you want
            maxResults=remain,
            location=location,
            locationRadius=location_radius,
            key=developerKey
        ).execute()
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                response = service.videos().list(
                    part='statistics, snippet,contentDetails',
                    id=search_result['id']['videoId']).execute()
                result_list.append(response)

    return result_list


def screenshotvideo(url, interval, id, fullduration, title, quality, likes, views, comments):
    os.mkdir(title+"/"+str(id), 0o755)
    save_xml(id, url, fullduration, views, likes, comments, title+"/"+str(id))
    interval = int(interval)
    parsed_t = isodate.parse_duration(fullduration)
    durationseconds=parsed_t.total_seconds()
    iterat=int(durationseconds/int(interval))
    for i in range(0, iterat):
        part(url, time.strftime('%H:%M:%S', time.gmtime(int(i*interval))), "00:00:01", title, str(id), quality, i)


def part(url, starttime, duration, title, id, quality, i):
    f = os.popen("ffmpeg $(youtube-dl -f "+quality+" -g '"+url+"' | sed 's/.*/-ss "+starttime+" -i &/') -t "+duration+" -c:v libx264 "+title+"-"+id+".mp4")
    now = f.read()
    f = os.popen("ffmpeg -i "+title+"-"+id+".mp4 -ss 00:00:00 -vframes 1 "+title+"/"+id+"/"+title+"-"+id+"_"+str(i)+".jpg")
    now = f.read()
    f = os.popen("rm -rf "+title+"-"+id+".mp4")
    now = f.read()


def screenshotlist(results):
    for result in results:
        screenshotvideo("https://www.youtube.com/watch?v="+str(result['items'][0]['id']), 25, result['items'][0]['id'], result['items'][0]['contentDetails']['duration'])


def searchlist(keyword, max_results, order,developerKey):
    service = get_authenticated_service(developerKey)
    resultset = main_search(service, keyword, max_results=max_results, order=order, token=None, location=None, location_radius=None,developerKey=developerKey)
    return resultset


def save_xml(id, url, duration, views, likes, comments, location):
    video = ET.Element('video')
    id_element = ET.SubElement(video, 'id')
    url_element = ET.SubElement(video, 'url')
    duration_element = ET.SubElement(video, 'duration')
    views_element = ET.SubElement(video, 'views')
    likes_element = ET.SubElement(video, 'likes')
    comments_element = ET.SubElement(video, 'comments')

    id_element.text = id
    url_element.text = url
    duration_element.text = duration
    views_element.text = views
    likes_element.text = likes
    comments_element.text = comments

    data = ET.tostring(video)
    file = open(location+'/'+str(id)+'.xml', 'w')
    file.write(str(data))



@csrf_exempt
def dig_it(request):
    if request.method == 'POST':
        form = request.POST
        keyword = form['KeyWords']
        max_results = form['MaxResults']
        order = form['RankType']
        developerKey=form['ApiKey']
        if max_results == "":
            max_results = 10
        result = searchlist(keyword, int(max_results), order,developerKey)
        operation = Operation(
            keyword=keyword,
            api_key=developerKey,
            rank_by=order,
            created_by=request.user
        )
        operation.save()
        return render(request, 'home.html', {'result': result,'operation_id':operation.id})


def saveFile(request):
    if request.method == 'POST':
        form = request.POST
        operation_id=form.get('operation_id')
        videosUrls = form.getlist('videosUrls[]')
        durationList = form.getlist('durationList[]')
        likesList = form.getlist('likesList[]')
        viewsList = form.getlist('viewsList[]')
        commentsList = form.getlist('commentsList[]')
        stillImageValue = form.get('stillImageValue')
        titleDate = form.get('titelDate')
        titlePrefix = form.get('titelPrefix')
        quality = form.get('quality')
        operation = get_object_or_404(Operation, id=operation_id)
        duration_list = []
        for element in durationList:
            pt_index = element.index('PT')
            s_index = element.index('S')
            duration_list.append(element[pt_index:s_index+1])

        title = str(titlePrefix+"_"+titleDate).replace(" ", "_")
        os.mkdir(title, 0o755)
        i = 0
        for element in videosUrls:
            video = Video(
                video_id=element[element.index('?v=') + 3:],
                video_url=element,
                title=title,
                duration=durationList[i],
                views=viewsList[i],
                likes=likesList[i],
                comments=commentsList[i],
                related_to=operation
            )
            video.save()
            screenshotvideo(element,
                            stillImageValue,
                            element[element.index('?v=')+3:],
                            duration_list[i],
                            title,
                            quality,
                            likesList[i],
                            viewsList[i],
                            commentsList[i])
            i = i+1
    return HttpResponseRedirect(reverse('searchs', kwargs={}))


def searchshistory(request):
    operations = Operation.objects.all()
    ctx = {'operation_list': operations}

    return render(request, 'searches.html', context=ctx)


def showOperation(request,op):
    operation=Operation.objects.get(id=op)
    videos=Video.objects.filter(related_to=operation)
    videos_aug=[]
    for video in videos:
        pass
        # videos_aug.append({'video':video,'images':})

    return None