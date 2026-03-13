import os
import subprocess
import uuid
import httpx
import fal_client
from .config import settings
from .models import ShortIdea


def _download(url: str, out_path: str):
    with httpx.stream("GET", url, timeout=300) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)


def create_video(idea: ShortIdea) -> str:
    os.makedirs(settings.workdir, exist_ok=True)
    fal_client.api_key = settings.fal_key

    result = fal_client.subscribe(
        settings.fal_video_model,
        arguments={
            "prompt": idea.visual_prompt,
            "aspect_ratio": "9:16",
            "duration": 10,
        },
    )

    video_url = result.get("video", {}).get("url") or result.get("video_url")
    if not video_url:
        raise RuntimeError(f"No video URL from provider: {result}")

    raw_path = os.path.join(settings.workdir, f"{uuid.uuid4().hex}_raw.mp4")
    out_path = os.path.join(settings.workdir, f"{uuid.uuid4().hex}_final.mp4")
    _download(video_url, raw_path)

    # add random music bed if available + normalize to short-friendly format
    music = None
    if os.path.isdir(settings.music_dir):
        files = [f for f in os.listdir(settings.music_dir) if f.lower().endswith((".mp3", ".wav", ".m4a"))]
        if files:
            music = os.path.join(settings.music_dir, files[0])

    if music:
        cmd = [
            "ffmpeg", "-y", "-i", raw_path, "-i", music,
            "-map", "0:v:0", "-map", "1:a:0",
            "-shortest", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
            "-c:a", "aac", "-b:a", "160k", "-threads", str(settings.max_threads),
            "-movflags", "+faststart", out_path,
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-i", raw_path,
            "-c:v", "libx264", "-crf", "20", "-preset", "medium",
            "-an", "-threads", str(settings.max_threads),
            "-movflags", "+faststart", out_path,
        ]

    subprocess.run(cmd, check=True)
    return out_path
