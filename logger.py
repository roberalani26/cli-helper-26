import sys
from datetime import datetime

class Colorizer:
    COLORS = {'info': '\033[94m', 'warn': '\033[93m', 'error': '\033[91m', 'reset': '\033[0m'}

    @classmethod
    def paint(cls, level, message):
        return f"{cls.COLORS.get(level, '')}[{datetime.now().strftime('%H:%M:%S')}] {level.upper()}: {message}{cls.COLORS['reset']}"

class Logger:
    def __init__(self, output=sys.stdout):
        self.output = output

    def _log(self, level, msg):
        print(Colorizer.paint(level, msg), file=self.output)

    def info(self, msg): self._log('info', msg)
    def warn(self, msg): self._log('warn', msg)
    def error(self, msg): self._log('error', msg)

    def context(self, label):
        class ContextLogger:
            def __init__(self, parent, lbl): self.p, self.l = parent, lbl
            def info(self, m): self.p.info(f"[{self.l}] {m}")
            def warn(self, m): self.p.warn(f"[{self.l}] {m}")
            def error(self, m): self.p.error(f"[{self.l}] {m}")
        return ContextLogger(self, label)