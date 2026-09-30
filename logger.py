import sys
import traceback
from pathlib import Path


class ResilientLogger:
    def __init__(self, filepath: str = "cli_activity.log"):
        self.filepath = Path(filepath)
        self.fallback = sys.stderr

    def _write_safely(self, message: str) -> None:
        try:
            clean_message = message.encode("utf-8", errors="replace").decode("utf-8")
        except Exception:
            clean_message = "[Encoding Error] Failed to process log entry"

        try:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(clean_message + "\n")
        except (PermissionError, OSError) as err:
            self.fallback.write(
                f"[FALLBACK] logging failure ({type(err).__name__}): {clean_message}\n"
            )
            self.fallback.flush()

    def log(self, level: str, raw_data: any) -> None:
        try:
            detail = str(raw_data)
        except Exception as e:
            detail = f"<Unstringable {type(raw_data).__name__}: {type(e).__name__}>"

        if len(detail) > 1000:
            detail = detail[:997] + "..."

        formatted = f"[{level.upper()}] {detail}"
        self._write_safely(formatted)

    def log_exception(self, exc: Exception) -> None:
        try:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        except Exception:
            tb = f"Could not trace: {type(exc).__name__}"
        self.log("CRITICAL", tb)
