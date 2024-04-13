from fastapi import FastAPI, UploadFile, File, Request
<<<<<<< HEAD
from fastapi.responses import FileResponse, StreamingResponse
import cv2
import json
import random
import torch

=======
from fastapi.responses import FileResponse
import cv2

import psycopg2

import torch

from config import database, nn_classes, content_types, cache_folder_path

>>>>>>> 608517f97eeb96edebd8e5cfc758ac677982c399
# model = torch.jit.load("*model_path*.pt")
# model.eval()

app = FastAPI()

<<<<<<< HEAD
cfg = json.load(open('config.json'))
cont_types = cfg['content-types']
nn_classes = cfg['nn_classes']
cache_path = cfg['cache_folder_path']

def net_forward(img_path : str):
    img = cv2.imread(img_path)

    return 0

def get_similar(category_id: int):
    filenames = []

    return filenames


@app.post("/upload")
def upload(request : Request, file_info: UploadFile = File(...)):
    if file_info.size == 0 or file_info.headers['content-type'] not in cont_types:
=======
def net_forward(img_path : str):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return 0

@app.post("/upload")
def upload(request : Request, file_info: UploadFile = File(...)):
    if file_info.size == 0 or file_info.headers['content-type'] not in content_types:
>>>>>>> 608517f97eeb96edebd8e5cfc758ac677982c399
       return {'message': f'Wront content-type: {file_info.headers["content-type"]}'}
    
    file = file_info.file
    
    if not file.readable():
        return {'message': f'Image "{file_info.filename}" is unreadable'}

<<<<<<< HEAD
    cached_image_path = 'image_cache/' + file_info.filename
    cached_file = open(cached_image_path, 'wb')

    if not cached_file.writable():
        return {'message', f'File "{cached_image_path}" is not writable!'}
    
    cached_file.write(file.read())
    cached_file.close()
=======
    cached_image_path = cache_folder_path + file_info.filename
    with open(cached_image_path, 'wb') as cache_file:
        cache_file.write(file.read())
>>>>>>> 608517f97eeb96edebd8e5cfc758ac677982c399

    file.close()

    category = net_forward(cached_image_path)

<<<<<<< HEAD
    requests : list[str] = [str(request.base_url) + f'image?category_id={category}&image_id={i}' for i in range(10)]

    return {
        'category': cfg['nn_classes'][category],
=======
    requests = [str(request.base_url) + f'image?filename={i}' for i in range(10)]

    return {
        'category': nn_classes[category],
>>>>>>> 608517f97eeb96edebd8e5cfc758ac677982c399
        'image_requests': requests
    }

@app.get("/image")
<<<<<<< HEAD
def image(category_id: int, image_id : int):
    if category_id >= len(nn_classes) or category_id < 0:
        return {'message': f'Invalid category_id: {category_id}'}

    category_files = get_similar(category_id)
    if image_id >= len(category_files) or image_id < 0:
        return {'message': f'Invalid image ID: {image_id}'}

    img_path = cache_path + category_files[random.randint(0, len(category_files))]
=======
def image(filename : str):
    img_path = ''
>>>>>>> 608517f97eeb96edebd8e5cfc758ac677982c399

    return FileResponse(img_path)