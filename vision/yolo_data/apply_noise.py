import torch
from torchvision import transforms
from PIL import Image, ImageFilter
import random
import os
import shutil


# Function to add salt and pepper noise to an image tensor
def add_salt_and_pepper_noise(image, prob=0.05):
    output = image.clone()
    salt_pepper = torch.rand_like(image)
    output[salt_pepper < (prob / 2)] = 0  # Pepper
    output[salt_pepper > 1 - (prob / 2)] = 1  # Salt
    return output


# Define the augmentation pipeline with probabilities
augmentation_pipeline = transforms.Compose([
    transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5),  # Color jitter without hue change
    transforms.Lambda(lambda img: img.filter(ImageFilter.MedianFilter(size=3)) if random.random() < 0.5 else img),
    # Median noise with probability 0.5
    transforms.Lambda(lambda img: img.filter(ImageFilter.SHARPEN) if random.random() < 0.3 else img),
    # Sharpen with probability 0.3
    transforms.ToTensor(),
    transforms.Lambda(lambda img: add_salt_and_pepper_noise(img) if random.random() < 0.2 else img),
    # Salt and pepper noise with probability 0.5
    transforms.ToPILImage(),
])


def augment_image(image_path, num_replicas=4):
    image = Image.open(image_path)
    augmented_images = []
    for _ in range(num_replicas):
        augmented_image = augmentation_pipeline(image)
        augmented_images.append(augmented_image)
    return augmented_images


def copy_bounding_boxes(txt_path, output_dir, num_replicas=4):
    for i in range(num_replicas):
        shutil.copy(txt_path, os.path.join(output_dir, f'augmented_image_{i}.txt'))


def augment_images_in_folder(folder_path, num_replicas=4):
    images = folder_path + 'images/'
    texts = folder_path + 'labels/'
    for filename in os.listdir(images):
        if filename.endswith('.jpg'):
            image_path = os.path.join(images, filename)
            txt_path = os.path.join(texts, filename.split('.')[0] + '.txt')

            print(f'augmenting: {image_path}\n            {txt_path}')

            # Augment images and save them
            augmented_images = augment_image(image_path)
            for i, img in enumerate(augmented_images):
                img.save(os.path.join(images, f'{os.path.splitext(filename)[0]}_augmented_{i}.jpg'))
                shutil.copy(txt_path, os.path.join(texts, f'{os.path.splitext(filename)[0]}_augmented_{i}.txt'))


# Example usage
folder_path = '../train/'
augment_images_in_folder(folder_path)

print("Augmentation and copying of bounding boxes completed.")
