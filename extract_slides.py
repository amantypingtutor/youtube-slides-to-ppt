import os
import sys
import cv2
import numpy as np
import yt_dlp
from pptx import Presentation
from pptx.util import Inches
import img2pdf
import requests

def get_stream_url(youtube_url):
    """YouTube Stream URL via Multi-Client Bypass or Proxy fallback"""
    # 1. Direct yt-dlp with TV/Web Embedded client bypass
    ydl_opts = {
        'format': 'best[height<=720]/best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['tv_embedded', 'web_embedded', 'android'],
                'player_skip': ['configs', 'webpage']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            if 'url' in info:
                return info['url']
    except Exception as e:
        print(f"Direct stream failed, trying fallback: {e}")

    # 2. Invidious Proxy Stream Fallback (100% Bot-Bypass on Cloud)
    video_id = youtube_url.split("v=")[-1].split("&")[0].split("?")[0].split("/")[-1]
    instances = [
        "https://inv.tux.pizza",
        "https://invidious.nerdvpn.de",
        "https://invidious.projectsegfau.lt"
    ]
    
    for instance in instances:
        try:
            api_url = f"{instance}/api/v1/videos/{video_id}"
            res = requests.get(api_url, timeout=10).json()
            formats = res.get('formatStreams', [])
            if formats:
                # 360p or 720p stream URL
                return formats[-1]['url']
        except Exception:
            continue

    raise RuntimeError("Could not retrieve stream URL. Bot block triggered on all endpoints.")

def extract_slides(youtube_url, output_folder="slides", sample_interval_sec=4, threshold=0.15):
    os.makedirs(output_folder, exist_ok=True)
    stream_url = get_stream_url(youtube_url)
    
    cap = cv2.VideoCapture(stream_url)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_interval = int(fps * sample_interval_sec)
    
    prev_gray = None
    slide_count = 0
    saved_images = []
    frame_idx = 0

    print("Extracting slides from video...")
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
            print(f"✓ Slide {slide_count} captured at {int(frame_idx/fps)}s")

        frame_idx += frame_interval

    cap.release()
    return saved_images

def save_outputs(images, ppt_path="output.pptx", pdf_path="output.pdf"):
    if not images:
        print("No slides found.")
        return

    # PPTX
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for img in images:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(img, 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(ppt_path)

    # PDF
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(images))

    print(f"Artifacts ready: {ppt_path} and {pdf_path}")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://youtu.be/EIhoVK88HOU"
    slides = extract_slides(url)
    save_outputs(slides)
    
