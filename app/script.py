# Script made to screenshot a video between selected frames and deleting the duplicated ones
# Usage example: taking screenshots from an app benchmark video
# By Lucheti29

import cv2
import time
import datetime
import os
import argparse

def capture_frames(video_path, output_folder, fps):
    # Open the video using CV2
    video_capture = cv2.VideoCapture(video_path)

    # Verify if the video was open successfully
    if not video_capture.isOpened():
        print("No se pudo abrir el video.")
        return

    i = 0
    frame_number = 0
    while True:
        # Read the frame number
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video_capture.read()

        # If it couldn't be read, break the cycle
        if not ret:
            break

        # Save the frame
        output_path = f"{output_folder}/frame_{i}.png"
        cv2.imwrite(output_path, frame)
        
        i += 1
        frame_number += fps

    # Free the resources
    video_capture.release()
    cv2.destroyAllWindows()

def dhash(image, hash_size=8):
    # Resize the image to hash_size + 1 x hash_size and convert it to grayscale
    resized = cv2.resize(image, (hash_size + 1, hash_size))
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Calculate the difference between adjacent columns
    diff = gray_image[:, 1:] > gray_image[:, :-1]

    # Convert the difference matrix into a binary hash
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hamming_distance(hash1, hash2):
    # Calculate the Hamming distance between two hashes
    return bin(hash1 ^ hash2).count('1')

def are_images_equal(image_path1, image_path2):
    # Read two images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # Calculate the hash of the images
    hash1 = dhash(image1)
    hash2 = dhash(image2)

    # Calculate the Hamming distance between hashes
    distance = hamming_distance(hash1, hash2)

    # Define a threshold to determinate if the images are equal
    threshold = 5

    # Images are considered equal if the Hamming distance is below the threshold
    return distance <= threshold

def get_image_creation_time(image_path):
    stat_info = os.stat(image_path)
    creation_time = stat_info.st_ctime
    return creation_time

def optimizing_sample(image_folder):
    # Get the list of files in the folder
    image_files = os.listdir(image_folder)

    # Sort the list by creation date
    image_files.sort(key=lambda file: get_image_creation_time(os.path.join(image_folder, file)))

    files_to_delete = []

    previous_image_path = None

    for image_name in image_files:
        # Read the current image
        image_path = os.path.join(image_folder, image_name)
        current_image = cv2.imread(image_path)

        # Compare the current image with the last one
        if previous_image_path is not None:
            if are_images_equal(image_path, previous_image_path):
                files_to_delete.append(image_path)

        # Update the last image with the current one for the next iteration
        previous_image_path = image_path

    # Delete the duplicated images
    for file_path in files_to_delete:
        os.remove(file_path)

def create_folder_with_creation_date():
    # Obtain the current date
    current_date = datetime.datetime.now()

    # Format the date with the desired format
    formatted_date = current_date.strftime("%Y-%m-%d_%H-%M-%S")

    #Name the folder with the creation date
    folder_name = f"screenshots_{formatted_date}"

    # Complete folder's path
    folder_path = os.path.join(".", folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path

if __name__ == "__main__":
    # Create an ArgumentParser
    parser = argparse.ArgumentParser()

    # Setup the script arguments
    parser.add_argument("--video", help="File video name")
    parser.add_argument("--fps", help="Number of frames between screenshots")
    parser.add_argument("--optimize", help="Optimize the screenshots removing the duplicate ones")

    args = parser.parse_args()

    print("Video: " + args.video)
    print("FPS: " + args.fps)
    print("Optimize: " + args.optimize)

    # Path to video
    video_path = args.video

    # Output folder
    output_folder = create_folder_with_creation_date()

    # Create the output folder if needed
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Capture the frames
    capture_frames(video_path, output_folder, int(args.fps))

    if args.optimize == "true":
        # Optimize the frames deleting the duplicated ones
        optimizing_sample(output_folder)