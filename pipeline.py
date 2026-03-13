from .models import RunResult
from .ideation import generate_ideas
from .generation import create_video
from .youtube_uploader import upload_short


def run_pipeline(instruction: str) -> RunResult:
    ideas = generate_ideas(instruction)
    items = []
    uploaded = 0

    for idea in ideas:
        video_path = create_video(idea)
        upload_res = upload_short(video_path, idea.title, idea.description)
        uploaded += 1
        items.append({
            "title": idea.title,
            "video_path": video_path,
            "youtube_id": upload_res.get("id"),
        })

    return RunResult(
        instruction=instruction,
        created=len(ideas),
        uploaded=uploaded,
        items=items,
    )
