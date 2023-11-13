import cv2
import glob
from PIL import Image

TEMP_DIR = "output"

def convert_mp4_to_jpgs(path):
    video_capture = cv2.VideoCapture(path)
    still_reading, image = video_capture.read()
    frame_count = 0
    while still_reading:
        image = cv2.resize(image, None, None, 0.5, 0.5)
        # print(image.shape)
        cv2.imwrite(f"{TEMP_DIR}/frame_{frame_count:03d}.jpg", image)
        
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1


def make_gif_from_jpegs(output_name="demo.gif"):
    images = glob.glob(f"{TEMP_DIR}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(output_name, format="GIF", append_images=frames[20::4],
                   save_all=True, duration=10, loop=0)

def mp4_to_gif(video_path, output_name="demo.gif"):
    convert_mp4_to_jpgs(video_path)
    make_gif_from_jpegs(output_name)

if __name__ == "__main__":
    mp4_to_gif("src2.mp4")
