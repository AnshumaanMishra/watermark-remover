import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image


def remove_watermark_multipage(input_pdf, output_pdf):
    # 1. Convert all pages to a list of PIL images
    # Using thread_count improves speed for multi-page PDFs
    print("Converting PDF to images...")
    pages = convert_from_path(input_pdf, dpi=300, thread_count=4)

    cleaned_page_list = []

    for i, page in enumerate(pages):
        print(f"Processing page {i + 1} of {len(pages)}...")

        # Convert PIL to OpenCV format
        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        # 2. Define the color range for the light gray watermark
        # These values (180-250) target the specific gray of 'CONFIDENTIAL'
        lower_gray = np.array([180, 180, 180])
        upper_gray = np.array([250, 250, 250])

        # 3. Create a mask and turn those pixels white
        mask = cv2.inRange(img, lower_gray, upper_gray)
        img[mask > 0] = [255, 255, 255]

        # 4. Convert back to PIL format for PDF saving
        cleaned_page_list.append(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))

    # 5. Save all processed images into a single multi-page PDF
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
