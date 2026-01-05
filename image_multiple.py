import os

import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image


def remove_watermark():
    pdf_name = input("Enter the PDF filename: ")
    if not os.path.exists(pdf_name):
        print("File not found!")
        return

    # Default BGR values for light gray watermarks
    lower_bgr = np.array([190, 190, 190])
    upper_bgr = np.array([245, 245, 245])

    change_color = input("Do you want to change the watermark color? (y/n): ").lower()

    if change_color == "y":
        r_low = int(input("Lower Red: "))
        g_low = int(input("Lower Green: "))
        b_low = int(input("Lower Blue: "))
        r_high = int(input("Upper Red: "))
        g_high = int(input("Upper Green: "))
        b_high = int(input("Upper Blue: "))

        lower_bgr = np.array([b_low, g_low, r_low])
        upper_bgr = np.array([b_high, g_high, r_high])

    print("Processing...")
    try:
        pages = convert_from_path(pdf_name, dpi=300)
    except Exception as e:
        print(f"Error: {e}")
        return

    cleaned_pages = []

    for page in pages:
        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
        mask = cv2.inRange(img, lower_bgr, upper_bgr)
        img[mask > 0] = [255, 255, 255]
        cleaned_pages.append(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))

    output_name = "cleaned_" + pdf_name
    cleaned_pages[0].save(
        output_name,
        save_all=True,
        append_images=cleaned_pages[1:],
        resolution=300.0,
        quality=100,
    )
    print(f"Success: {output_name}")


if __name__ == "__main__":
    remove_watermark()
