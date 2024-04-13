import numpy as np

from transformers import CLIPModel, CLIPProcessor
from sklearn.metrics.pairwise import cosine_similarity

from PIL import Image

from matplotlib import pyplot as plt

device = 'cuda:0'

data = np.load('image_embeddings.npz')

image_filepaths = data['file_names']
image_embeddings = data['embeddings']

model_id = 'openai/clip-vit-base-patch32'
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)

search_image = Image.open('image.png')
search_inputs = processor(text=None, images=search_image, return_tensors="pt")
search_pixel_values = search_inputs["pixel_values"].to(device)
search_features = model.get_image_features(pixel_values=search_pixel_values).squeeze(0).cpu().detach().numpy()

distances = 1 - cosine_similarity([search_features], image_embeddings).flatten()

path_indexes = distances.argsort()[:10]
distances = sorted(distances)[:10]

plt.imshow(search_image)

fig, axes = plt.subplots(1, 10, figsize=(20, 4))

for i in range(10):
    image_path = image_filepaths[path_indexes[i]]
    image = Image.open(image_path)

    ax = axes[i]

    ax.imshow(image)
    ax.set_title(f'Distance: {distances[i]:.3f}')
    ax.axis('off')

plt.show()
