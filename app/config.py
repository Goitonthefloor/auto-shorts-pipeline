from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    fal_key: str = os.getenv("FAL_KEY", "")
    fal_image_model: str = os.getenv("FAL_IMAGE_MODEL", "fal-ai/flux/schnell")
    fal_video_model: str = os.getenv("FAL_VIDEO_MODEL", "fal-ai/minimax/video-01-live")

    youtube_client_secret_path: str = os.getenv("YOUTUBE_CLIENT_SECRET_PATH", "/app/secrets/client_secret.json")
    youtube_token_path: str = os.getenv("YOUTUBE_TOKEN_PATH", "/app/secrets/token.json")
    youtube_category_id: str = os.getenv("YOUTUBE_CATEGORY_ID", "24")
    youtube_privacy_status: str = os.getenv("YOUTUBE_PRIVACY_STATUS", "public")

    max_threads: int = int(os.getenv("MAX_THREADS", "12"))
    workdir: str = os.getenv("WORKDIR", "/app/data")
    music_dir: str = os.getenv("MUSIC_DIR", "/app/music")


settings = Settings()
