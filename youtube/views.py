from django.shortcuts import render, render_to_response

from django.core.handlers.wsgi import WSGIRequest

#from django.views.static import serve
#return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

import os, shutil

from pytube import YouTube

from pprint import pprint

import moviepy.editor as mp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILENAME = ""


def main(request):
    
    clear_media_directory()
    return render(request, "index.html", {'message':'', 'filename':'', 'file_found': False})
    


def search(request):
    
    clear_media_directory()
    url = request.GET['url']
    start = request.GET['start_time']
    stop = request.GET['stop_time']
    option = request.GET['option']
    

    if validated(url, start, stop, option):
        '''
        fetch_video(url)
        fetch_audio(start, stop)
                    
        filepath = 'media/' + FILENAME + ".mp3"
        
        return render_to_response('index.html', {'message':'', 'filename': filepath, 'file_found': True})
        #return render(, 'index.html', {'message':'', 'filename': filepath, 'file_found': True})
        '''
        try:
            
            #fetch the vid
            fetch_video(url)
            
            filepath = 'media/' + FILENAME + ".mp4"
            
            #if audio option was chosen, then we create the mp3 file
            if (option == 'audio'):
                try:
                    fetch_audio(start, stop)
                    
                    filepath = 'media/' + FILENAME + ".mp3"
                    
                    return render_to_response('index.html', {'message':'', 'filename': filepath, 'file_found': True})
                    #return render(request, 'index.html', {'message': '', 'filename': filepath, 'file_found': True})
                except:
                    return render_to_response('index.html', {'message':'Error during MP3 extraction.', 'filename': '' , 'file_found': False})
                    #return render(request, 'index.html', {'message': 'Error during MP3 extraction.', 'filename':'', 'file_found': False})
            
                       
            else:
                return render_to_response('index.html', {'message':'', 'filename': filepath, 'file_found': True})
            
        except:
            return render_to_response('index.html', {'message':'Invalid Youtube URL', 'filename': '', 'file_found': False})
            #return render(request, 'index.html', {'message': 'Invalid Youtube URL', 'filename':'', 'file_found': False})
        
        
    else:
        return render_to_response('index.html', {'message':'Start/End times are incorrect', 'filename':'' , 'file_found': False})
        #return render(request, 'index.html', {'message': 'Start/End times are incorrect', 'filename':'', 'file_found': False})
    

    
    


def validated(url, start, stop, option):
    
    try:
        if url == '' or option == '':
            return False
        return  (start == '' and stop == '') or (int(start) < int(stop)) 
    except:
        return False


def fetch_video(url):
    
    global FILENAME
    yt = YouTube(url)
    FILENAME = yt.filename

    (yt.filter('mp4')[-1]).download('static/media/')
    

def fetch_audio(start_time, stop_time):
    
    
    video_name = FILENAME + ".mp4"
    audio_name = FILENAME + ".mp3"
    

    if (start_time == ''):

        clip = mp.VideoFileClip('static/media/' + video_name)
        clip.audio.write_audiofile('static/media/' + audio_name)
    else:
        start = int(start_time)
        stop = int(stop_time)
        clip = mp.VideoFileClip('static/media/' + video_name).subclip(start, stop)
        clip.audio.write_audiofile('static/media/' + audio_name)
                




def clear_media_directory():
    
    
    folder = 'static/media/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            pass
        