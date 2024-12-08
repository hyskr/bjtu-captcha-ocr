import os
import shutil
import uuid
import cv2
import numpy as np
from PIL import Image
import os
import streamlit as st
import ddddocr
destination_dir = "train"

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

def trans(image_path):
    # Load grayscale image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.GaussianBlur(image, (1, 1), 1)

    # Use Laplacian filter to sharpen image
    laplacian_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, laplacian_filter)

    # Apply binary thresholding
    _, adaptive_thresh = cv2.threshold(sharpened_image, 150, 255, cv2.THRESH_BINARY_INV)

    # Define structuring element for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # Perform morphological opening to remove small noise
    opened_image = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)

    # Find contours in the image
    contours, _ = cv2.findContours(
        opened_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Create mask to filter contours
    mask = np.zeros_like(opened_image)

    # Define minimum contour area threshold
    min_contour_area = 2

    # Filter contours by area
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

    # Apply mask to retain relevant contours
    filtered_image = cv2.bitwise_and(opened_image, mask)

    final_image = cv2.bitwise_not(filtered_image)

    return final_image

with open("result.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.split(",")
        parts = [part.strip() for part in parts]
        if not parts[1].endswith("="):
            parts[1] = parts[1] + "="
        parts[1] = parts[1].replace("*", "x")

        source_file0 = parts[0].replace("valid1", "img1")
        source_file1 = parts[0]
        processed_image = trans(source_file0)
        pil_image = Image.fromarray(processed_image)
        # pil_image.save(source_file1)

        hash_value = uuid.uuid4().hex
        print(f"{parts[1]}_{hash_value}.png")
        destination_file = f"{destination_dir}\{parts[1]}_{hash_value}.png".replace(
            " ", ""
        )

        shutil.copy(source_file0, destination_file)

        # print(f"Copied {source_file} to {destination_file}")
