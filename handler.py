import sys
import functools
import logging

logger = logging.getLogger('cli-helper-26')

def robust_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            logger.info('graceful termination requested')
            sys.exit(0)
        except ValueError as e:
            logger.error(f'data validation failure: {e}')
            return None
        except Exception as e:
            logger.critical(f'unexpected system state: {e!r}')
            return {'error': True, 'msg': str(e)}
    return wrapper

class EdgeHandler:
    def __init__(self):
        self.registry = {}

    @robust_execution
    def process_input(self, data):
        if not isinstance(data, (dict, list)):
            raise ValueError('invalid input type for processing')
        return [self._transform(i) for i in (data if isinstance(data, list) else [data])]

    def _transform(self, item):
        if 'key' not in item:
            raise KeyError('missing required processing key')
        return item['key'].upper()

if __name__ == '__main__':
    handler = EdgeHandler()
    result = handler.process_input({'key': 'hello'})
    print(f'processed: {result}')