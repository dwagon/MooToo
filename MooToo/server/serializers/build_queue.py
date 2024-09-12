from typing import TYPE_CHECKING, Any

from .construct import construct_serializer

if TYPE_CHECKING:
    from MooToo.build_queue import BuildQueue


def build_queue_serializer(build_queue: "BuildQueue") -> dict[str, Any]:
    return {"queue": [construct_serializer(_) for _ in build_queue._queue]}


# EOF
