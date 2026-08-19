import os
import sys
import cv2
import numpy as np
import yt_dlp
from pptx import Presentation
from pptx.util import Inches
import img2pdf

def get_stream_url(youtube_url):
    ydl_opts = {
        'format': 'best[height<=720]',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']

def extract_slides(youtube_url, output_folder="slides", sample_interval_sec=3, threshold=0.15):
    os.makedirs(output_folder, exist_ok=True)
    stream_url = get_stream_url(youtube_url)
    
    cap = cv2.VideoCapture(stream_url)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_interval = int(fps * sample_interval_sec)
    
    prev_gray = None
    slide_count = 0
    saved_images = []
    frame_idx = 0

    print("Extracting slides...")
    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (640, 360))

        if prev_gray is None:
            is_new = True
        else:
            diff = cv2.absdiff(prev_gray, gray)
            non_zero_ratio = np.count_nonzero(diff > 30) / diff.size
            is_new = non_zero_ratio > threshold

        if is_new:
            slide_count += 1
            img_path = f"{output_folder}/slide_{slide_count:04d}.jpg"
            cv2.imwrite(img_path, frame)
            saved_images.append(img_path)
            prev_gray = gray
            print(f"Slide {slide_count} captured at {int(frame_idx/fps)}s")

        frame_idx += frame_interval

    cap.release()
    return saved_images

def save_outputs(images, ppt_path="output.pptx", pdf_path="output.pdf"):
    if not images:
        print("No slides found.")
        return

    # Create PPTX
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for img in images:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(img, 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(ppt_path)

    # Create PDF
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(images))

    print(f"Done! Created {ppt_path} and {pdf_path}")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://youtu.be/EIhoVK88HOU"
    slides = extract_slides(url)
    save_outputs(slides)
  
