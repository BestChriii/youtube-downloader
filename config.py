from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()
VIDEOS_URL = os.getenv("VIDEOS_URL").split(",")
PLAYLISTS_URL = os.getenv("PLAYLISTS_URL").split(",")
project_dir = Path.cwd()
VIDEOS_DIR = os.getenv("VIDEOS_DIR", project_dir / "downloads")
