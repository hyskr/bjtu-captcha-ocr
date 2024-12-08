import os

import cv2
import ddddocr
import numpy as np
import streamlit as st
from PIL import Image


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


def save_annotation(save_path, text):
    with open("result.txt", "a", encoding="utf-8") as f:
        annotation = f"{save_path}, {text}\n"
        f.write(annotation)


def load_processed_images():
    processed_images = set()
    if os.path.exists("result.txt"):
        with open("result.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split(",")
                if len(parts) > 0:
                    # Only save the base name to match the file names in unprocessed_files
                    processed_images.add(os.path.basename(parts[0].strip()))
    return processed_images


def main():
    st.title("图像标注工具")

    if not os.path.exists("./valid1"):
        os.makedirs("./valid1", exist_ok=True)

    img_dir = "./img1"
    file_list = sorted(os.listdir(img_dir))
    processed_images = load_processed_images()

    # Filter out already processed images
    unprocessed_files = [file for file in file_list if file not in processed_images]

    # if "current_image" not in st.session_state:
    # st.session_state.current_image = 0
    #  and st.session_state.current_image < len(unprocessed_files)
    if unprocessed_files:
        image_file = unprocessed_files[0]
        image_path = os.path.join(img_dir, image_file)

        processed_image = trans(image_path)

        st.image(
            processed_image, caption=f"处理后的图像 {image_file}", use_column_width=True
        )

        # 辅助标注
        ocr = ddddocr.DdddOcr(
            show_ad=False,
            import_onnx_path=r"dddd_trainer\projects\math2\models\math2_1.0_599_10800_2024-08-07-01-49-02.onnx",
            charsets_path=r"dddd_trainer\projects\math2\models\charsets.json",
        )
        save_path = f"./valid1/{image_file}"

        pil_image = Image.fromarray(processed_image)
        pil_image.save(save_path)

        image = Image.open(f"./valid1/{image_file}")

        result = ocr.classification(image)
        text = st.text_input("请输入验证码：", value=result)

        if st.button("保存"):
            save_annotation(save_path, text)
            st.success("标注已保存!")
            # st.session_state.current_image += 1
            # Ensure we reset the index if we reach the end
            # if st.session_state.current_image >= len(unprocessed_files):
            # st.session_state.current_image = 0
            st.rerun()

    else:
        st.info("没有更多的图像可标注或文件夹为空。")


if __name__ == "__main__":
    main()
