from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Alarm Image Verify"
    database_url: str = "sqlite:///./data/verify.db"
    images_dir: str = "data/images"
    inbox_dir: str = "data/inbox"
    scan_interval_seconds: int = Field(default=5, ge=1, le=10)
    weights_path: str = "weights/yolo.pt"
    device: str = "cpu"
    conf_threshold: float = 0.25
    max_upload_bytes: int = 10 * 1024 * 1024
    allowed_image_suffixes: str = ".jpg,.jpeg,.png,.bmp,.webp"
    detector_backend: str = "stub"
    serve_web: bool = False

    @property
    def allowed_suffix_set(self) -> set[str]:
        return {s.strip().lower() for s in self.allowed_image_suffixes.split(",") if s.strip()}

    def ensure_data_dirs(self) -> None:
        Path(self.images_dir).mkdir(parents=True, exist_ok=True)
        inbox = Path(self.inbox_dir)
        inbox.mkdir(parents=True, exist_ok=True)
        (inbox / "done").mkdir(parents=True, exist_ok=True)


settings = Settings()
