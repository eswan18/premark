from pkg_resources import resource_filename
from pathlib import Path
from typing import runtime_checkable, Protocol


@runtime_checkable
class Readable(Protocol):
    def read(self) -> Union[str, bytes]: ...


FileCoercible = Union[str, Path, Readable]


def contents_of_file_coercible(f: FileCoercible) -> Union[str, bytes]:
    if isinstance(f, Readable):
        contents = f.read()
    else:
        if isinstance(f, str):
            f = Path(file)
        contents = f.read_text()
    return contents


def pkg_file(path: str) -> str:
    return resource_filename('premark', path)
