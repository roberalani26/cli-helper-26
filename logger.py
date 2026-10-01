import gzip
import logging
from pathlib import Path

class GzipRotatingHandler(logging.Handler):
    """A custom logging handler that rotates files by compressing them
    into .gz format instantly upon reaching a line threshold.
    """
    def __init__(self, filename: str, max_lines: int = 100, backup_count: int = 3):
        super().__init__()
        self.filepath = Path(filename)
        self.max_lines = max_lines
        self.backup_count = backup_count
        self.line_count = 0
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if self.filepath.exists():
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.line_count = sum(1 for _ in f)
        else:
            self.filepath.touch()
            self.line_count = 0

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            with open(self.filepath, 'a', encoding='utf-8') as f:
                f.write(msg + '\n')
            self.line_count += 1

            if self.line_count >= self.max_lines:
                self.rotate()
        except Exception:
            self.handleError(record)

    def rotate(self) -> None:
        for i in range(self.backup_count - 1, 0, -1):
            old_file = self.filepath.with_suffix(f'.{i}.log.gz')
            new_file = self.filepath.with_suffix(f'.{i+1}.log.gz')
            if old_file.exists():
                old_file.rename(new_file)

        target = self.filepath.with_suffix('.1.log.gz')
        if self.filepath.exists():
            with open(self.filepath, 'rb') as f_in:
                with gzip.open(target, 'wb') as f_out:
                    f_out.writelines(f_in)
            self.filepath.unlink()

        self._ensure_file()

def setup_logger(name: str = 'cli_helper', log_file: str = 'app.log', max_lines: int = 50) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = GzipRotatingHandler(log_file, max_lines=max_lines)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger