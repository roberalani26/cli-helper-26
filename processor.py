"""Stream text processor for CLI output formatting with typed transformations."""

import sys
from dataclasses import dataclass
from typing import Annotated, Callable, Generator, Iterable, TypeVar

T = TypeVar("T")
ProcessedChunk = Annotated[str, "CLI formatted string chunk"]
TransformFunc = Callable[[str], str]


@dataclass(frozen=True)
class PipelineStep:
    """Single transformation step within the CLI processing pipeline."""

    name: str
    transform: TransformFunc
    enabled: bool = True

    def __call__(self, payload: str) -> str:
        """Execute transformation if step is active."""
        return self.transform(payload) if self.enabled else payload


class StreamProcessor:
    """Creative pipeline engine for streaming text content to CLI outputs."""

    def __init__(self, steps: list[PipelineStep] | None = None) -> None:
        """Initialize the processor with optional predefined steps."""
        self._pipeline: list[PipelineStep] = steps or []

    def pipe(self, name: str, fn: TransformFunc) -> "StreamProcessor":
        """Fluently append a named transformation logic to execution chain."""
        self._pipeline.append(PipelineStep(name=name, transform=fn))
        return self

    def process_stream(
        self, source: Iterable[str]
    ) -> Generator[ProcessedChunk, None, None]:
        """Yield decorated and modified stream segments through active pipeline steps."""
        for raw_line in source:
            current: str = raw_line.rstrip("\n")
            for step in self._pipeline:
                current = step(current)
            yield ProcessedChunk(current)

    def consume(self, source: Iterable[str], target=sys.stdout) -> int:
        """Stream elements to target writer, returning total processed count."""
        count: int = 0
        for chunk in self.process_stream(source):
            target.write(f"{chunk}\n")
            count += 1
        return count


def uppercase_prefix(prefix: str) -> TransformFunc:
    """Create a closure adding standard CLI styled prefix to text."""

    def _wrapper(text: str) -> str:
        return f"[{prefix.upper()}] {text}"

    return _wrapper
