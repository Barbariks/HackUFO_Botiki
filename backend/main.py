from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
import cv2

import psycopg2

import torch

from config import database, nn_classes, content_types, cache_folder_path

# model = torch.jit.load("*model_path*.pt")
# model.eval()

app = FastAPI()

def net_forward(img_path : str):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return 0

@app.post("/upload")
def upload(request : Request, file_info: UploadFile = File(...)):
    if file_info.size == 0 or file_info.headers['content-type'] not in content_types:
       return {'message': f'Wront content-type: {file_info.headers["content-type"]}'}
    
    file = file_info.file
    
    if not file.readable():
        return {'message': f'Image "{file_info.filename}" is unreadable'}

    cached_image_path = cache_folder_path + file_info.filename
    with open(cached_image_path, 'wb') as cache_file:
        cache_file.write(file.read())

    file.close()

    category = net_forward(cached_image_path)

    requests = [str(request.base_url) + f'image?filename={i}' for i in range(10)]

    return {
        'category': nn_classes[category],
        'image_requests': requests
    }

@app.get("/image")
def image(filename : str):
    img_path = ''

    return FileResponse(img_path)