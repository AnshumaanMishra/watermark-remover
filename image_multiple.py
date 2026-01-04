import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image


def remove_watermark_multipage(input_pdf, output_pdf):
    print("Converting PDF to images...")
    pages = convert_from_path(input_pdf, dpi=300, thread_count=4)

    cleaned_page_list = []

    for i, page in enumerate(pages):
        print(f"Processing page {i + 1} of {len(pages)}...")

        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        lower_gray = np.array([180, 180, 180])
        upper_gray = np.array([250, 250, 250])

        mask = cv2.inRange(img, lower_gray, upper_gray)
        img[mask > 0] = [255, 255, 255]

        cleaned_page_list.append(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))

    if cleaned_page_list:
        cleaned_page_list[0].save(
            output_pdf,
            save_all=True,
            append_images=cleaned_page_list[1:],
            resolution=300.0,
            quality=95,
        )
    print(f"Complete! Saved to {output_pdf}")


remove_watermark_multipage("wm16_merged.pdf", "clean_multipage.pdf")
