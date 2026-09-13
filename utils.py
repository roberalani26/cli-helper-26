from typing import Any, Union

class PathNavigator:
    """A creative utility to navigate nested data structures using division '/' operator."""
    def __init__(self, data: Any):
        self.data = data

    def __truediv__(self, key: Union[str, int]) -> "PathNavigator":
        """Navigate into the nested structure. Supports wildcard expansion for lists."""
        if self.data is None:
            return PathNavigator(None)

        if key == "*":
            if isinstance(self.data, list):
                return PathNavigator(self.data)
            if isinstance(self.data, dict):
                return PathNavigator(list(self.data.values()))
            return PathNavigator([])

        if isinstance(self.data, list):
            if isinstance(key, int):
                try:
                    return PathNavigator(self.data[key])
                except IndexError:
                    return PathNavigator(None)
            if str(key).isdigit():
                try:
                    return PathNavigator(self.data[int(key)])
                except IndexError:
                    return PathNavigator(None)
            
            extracted = []
            for item in self.data:
                nav = PathNavigator(item) / key
                if nav.data is not None:
                    if isinstance(nav.data, list):
                        extracted.extend(nav.data)
                    else:
                        extracted.append(nav.data)
            return PathNavigator(extracted if extracted else None)

        if isinstance(self.data, dict):
            return PathNavigator(self.data.get(key))

        return PathNavigator(None)

    def resolve(self, default: Any = None) -> Any:
        """Retrieve the wrapped structure, falling back to default."""
        return self.data if self.data is not None else default

    def __repr__(self) -> str:
        return f"PathNavigator({repr(self.data)})"


def dig(data: Any, path: str, default: Any = None) -> Any:
    """Extract data nested deep using dot or slash notation strings."""
    delim = "/" if "/" in path else "."
    steps = [int(x) if x.isdigit() else x for x in path.split(delim)]
    node = PathNavigator(data)
    for step in steps:
        node = node / step
    return node.resolve(default)
