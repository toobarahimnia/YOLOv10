from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import torch
import cv2
from PIL import Image
import numpy as np
import os
from ultralytics import YOLO


def base(request):
    return render(request, 'base.html')


# if using yolov10 then can use best.pt - but performance is poor as dataset is limited to cars and people.
# important: pip install --upgrade ultralytics

    
def load_model():
    model_name='yolov8n.pt'
    model = YOLO(model_name)
    # model = torch.hub.load(os.getcwd(), 'custom', source='local', path = model_name, force_reload = True)
    return model


def get_prediction(media_path, model):
    
    # perform object detection
    result = model(media_path, conf=0.25, save=True, project=settings.MEDIA_ROOT) # name="xxxx"
    # print(result[0].save_dir)
    # print(settings.MEDIA_ROOT)
    # return os.path.join(result[0].save_dir, os.path.basename(media_path))
    relative_results_dir = os.path.relpath(result[0].save_dir, settings.MEDIA_ROOT)
    
    return relative_results_dir

def obj_dtc(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        media_path = fs.url(filename)

        model = load_model()
        # media_full_path = settings.BASE_DIR / media_path
        media_full_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        
        # Get the directory where the predictions are saved
        results_dir = os.path.join(get_prediction(media_full_path, model), filename) 
        # print(f'result dir: {results_dir}')
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, results_dir)):
            return render(request, 'obj_dtc.html', {'error': 'Error in saving predictions'})

        
        if myfile.name.endswith(('.mp4', '.avi')):
            context = {'original_video': media_path, 'result_media': os.path.join(settings.MEDIA_URL, results_dir)}
        else:
            context = {'original_image': media_path, 'result_media': os.path.join(settings.MEDIA_URL, results_dir)}

        return render(request, 'obj_dtc.html', context)
      
    return render(request, 'obj_dtc.html')