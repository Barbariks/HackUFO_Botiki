from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, StreamingResponse
import cv2
import json
import random
import torch

# model = torch.jit.load("*model_path*.pt")
# model.eval()

app = FastAPI()

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
       return {'message': f'Wront content-type: {file_info.headers["content-type"]}'}
    
    file = file_info.file
    
    if not file.readable():
        return {'message': f'Image "{file_info.filename}" is unreadable'}

    cached_image_path = 'image_cache/' + file_info.filename
    cached_file = open(cached_image_path, 'wb')

    if not cached_file.writable():
        return {'message', f'File "{cached_image_path}" is not writable!'}
    
    cached_file.write(file.read())
    cached_file.close()

    file.close()

    category = net_forward(cached_image_path)

    requests : list[str] = [str(request.base_url) + f'image?category_id={category}&image_id={i}' for i in range(10)]

    return {
        'category': cfg['nn_classes'][category],
        'image_requests': requests
    }

@app.get("/image")
def image(category_id: int, image_id : int):
    if category_id >= len(nn_classes) or category_id < 0:
        return {'message': f'Invalid category_id: {category_id}'}

    category_files = get_similar(category_id)
    if image_id >= len(category_files) or image_id < 0:
        return {'message': f'Invalid image ID: {image_id}'}

    img_path = cache_path + category_files[random.randint(0, len(category_files))]

    return FileResponse(img_path)