import os
import time
import numpy as np
from PIL import Image
import imageio
import random
from CMC.ContinuousMarkovChain import ContinuousMarkovChain
from tqdm import tqdm

# Parameters
save_interval = 100  # Save every 10 frames

def spiral_order(data):
    """ Generate pixels in spiral order from a given image data. """
    x, y = 0, 0
    dx, dy = 0, -1
    max_x, max_y = data.shape[1], data.shape[0]
    for _ in range(max_x * max_y):
        if (-max_x/2 < x <= max_x/2) and (-max_y/2 < y <= max_y/2):
            yield data[y, x]
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

def save_frame(data, frame_path):
    """ Save an image frame from numpy array data. """
    img = Image.fromarray(data.astype('uint8'), 'RGB') # switch to rgba for pngs
    img.save(frame_path)

def process_image(image_path):
    # Load image and prepare directory for saving frames and output
    img = Image.open(image_path)
    img_data = np.array(img)
    timestamp = int(time.time())
    frames_dir = f"./media/{timestamp}/frames"
    os.makedirs(frames_dir, exist_ok=True)

    # Generate pixel sequence in spiral order
    pixel_sequence = list(spiral_order(img_data))

    # Create Markov chain
    cmc = ContinuousMarkovChain(pixel_sequence, attractor_coefficient=1)

    # Generate new image sequence using Markov chain
    current_pixel = random.choice(pixel_sequence)
    new_image_data = np.zeros_like(img_data)

    frames = []
    total_pixels = img_data.shape[0] * img_data.shape[1]
    for i in tqdm(range(total_pixels)):  # Iterate over all possible pixel positions
        next_pixel = cmc.get_next_state(current_pixel)
        if next_pixel is None:
            break
        new_image_data[i // img_data.shape[1], i % img_data.shape[1]] = next_pixel
        if i % save_interval == 0 or i == 0 or i == total_pixels - 1:
            frame_path = os.path.join(frames_dir, f"frame{i}.jpg")
            save_frame(new_image_data, frame_path)
            frames.append(frame_path)
        current_pixel = next_pixel

    # Create GIF from frames
    with imageio.get_writer(f'./media/{timestamp}/output.gif', mode='I') as writer:
        for frame_path in frames:
            image = imageio.imread(frame_path)
            writer.append_data(image)

    print("GIF created successfully.")


def process_images(image_paths):
    # Make sure output dir is createed
    timestamp = int(time.time())
    frames_dir = f"./media/{timestamp}/frames"
    os.makedirs(frames_dir, exist_ok=True)

    # Load image and prepare directory for saving frames and output
    pixel_sequences = []
    for image_path in image_paths:
        img = Image.open(image_path)
        img_data = np.array(img)
        print(img_data.shape, "shape of", image_path)

        # Generate pixel sequence in spiral order
        pixel_sequence = list(spiral_order(img_data))
        pixel_sequences.append(pixel_sequence)

    # Create Markov chain
    cmc = ContinuousMarkovChain(pixel_sequences, attractor_coefficient=1)

    # Generate new image sequence using Markov chain
    current_pixel = random.choice(pixel_sequence)
    new_image_data = np.zeros_like(img_data)

    frames = []
    total_pixels = img_data.shape[0] * img_data.shape[1]
    for i in tqdm(range(total_pixels)):  # Iterate over all possible pixel positions
        next_pixel = cmc.get_next_state(current_pixel)
        if next_pixel is None:
            break
        new_image_data[i // img_data.shape[1], i % img_data.shape[1]] = next_pixel
        if i % save_interval == 0 or i == 0 or i == total_pixels - 1:
            frame_path = os.path.join(frames_dir, f"frame{i}.jpg")
            save_frame(new_image_data, frame_path)
            frames.append(frame_path)
        current_pixel = next_pixel

    # Create GIF from frames
    with imageio.get_writer(f'./media/{timestamp}/output.gif', mode='I') as writer:
        for frame_path in frames:
            image = imageio.imread(frame_path)
            writer.append_data(image)

    print("GIF created successfully.")



import cProfile
import pstats

if __name__ == "__main__":
    image_paths = ["./inputs/images/" + name for name in [
        "dog1.jpg", "dog2.jpg", "dog3.jpg"
    ]]
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    process_images(image_paths)
    
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()