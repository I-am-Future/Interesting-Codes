import cv2
import sys
from tqdm import tqdm
import os

# Define a mapping of common video formats to FourCC codes
FORMAT_TO_FOURCC = {
    "avi": cv2.VideoWriter_fourcc(*"XVID"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
    # Add more formats and corresponding FourCC codes as needed
}

def main():
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python video_encoding.py <input_video> <output_format>")
        return

    # Get the input video file name and target encoding format from command line
    input_video = sys.argv[1]
    output_format = sys.argv[2]

    try:
        # Open the input video file
        cap = cv2.VideoCapture(input_video)

        # Check if the video file was successfully opened
        if not cap.isOpened():
            print("Error: Unable to open input video.")
            return

        # Get video properties (frame dimensions, frame rate, etc.)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

        # Map the output format to the corresponding FourCC code
        if output_format in FORMAT_TO_FOURCC:
            fourcc = FORMAT_TO_FOURCC[output_format]
        else:
            print("Error: Unsupported output format.")
            return

        # output name is input name, with diff extension name
        output_name = input_video.replace(input_video.split('.')[-1], output_format)

        # Define the codec and create a VideoWriter object for the output video
        output_video = cv2.VideoWriter(
            output_name,
            fourcc,
            frame_rate,
            (frame_width, frame_height)
        )

        # Get the basename of the input video (without extension)
        base_name = os.path.basename(input_video)

        # Get the total number of frames in the input video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create a tqdm progress bar
        progress_bar = tqdm(total=total_frames, desc="Processing Frames")

        # Process and write each frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Perform any processing on 'frame' if needed

            # Write the processed frame to the output video
            output_video.write(frame)

            # Update the progress bar
            progress_bar.update(1)

        # Release video capture and writer
        cap.release()
        output_video.release()

        # Close the progress bar
        progress_bar.close()

        print(f"Video saved as {output_name}")

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
