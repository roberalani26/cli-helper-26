import sys
import signal
from typing import Callable, Any, Dict

class ExecutionPipeline:
    def __init__(self):
        self._tasks: Dict[str, Callable] = {}
        signal.signal(signal.SIGINT, self._handle_exit)

    def register(self, name: str, func: Callable):
        self._tasks[name] = func

    def run(self, name: str, *args, **kwargs) -> Any:
        if name not in self._tasks:
            raise ValueError(f'task {name} not registered')
        return self._tasks[name](*args, **kwargs)

    def _handle_exit(self, signum, frame):
        sys.exit(0)

class StreamProcessor(ExecutionPipeline):
    def process(self, data: str):
        return ''.join(reversed(data)).upper()

def cleanup_stream(data: str):
    return data.strip().replace('\n', ' ')

if __name__ == '__main__':
    handler = StreamProcessor()
    handler.register('clean', cleanup_stream)
    handler.register('reverse', handler.process)
    
    payload = '  cli-helper-26  \n'
    cleaned = handler.run('clean', payload)
    result = handler.run('reverse', cleaned)
    sys.stdout.write(f'processed: {result}\n')