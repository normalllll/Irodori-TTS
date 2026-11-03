"""Publish complete checkpoints without destroying the previous successful save."""

from __future__ import annotations

import json
import os
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path


def recover_checkpoint(target: Path) -> Path:
    previous = target.with_name(f".{target.name}.previous")
    if not target.exists() and previous.is_dir() and (previous / "complete.json").is_file():
        previous.replace(target)
    return target


@contextmanager
def checkpoint_target(target: Path, *, directory: bool = False, step: int | None = None):
    target.parent.mkdir(parents=True, exist_ok=True)
    # Do not repeat a long best-checkpoint name in the temporary basename.
    # The redundant name exceeded Windows' path limit before final publication.
    stage = target.with_name(f".ckpt-{uuid.uuid4().hex}.partial")
    previous = target.with_name(f".{target.name}.previous")
    recover_checkpoint(target)
    try:
        if directory:
            stage.mkdir()
        yield stage
        files = list(stage.rglob("*")) if directory else [stage]
        for file in files:
            if file.is_file():
                with file.open("r+b") as stream:
                    os.fsync(stream.fileno())
        if directory:
            marker = stage / "complete.json"
            marker.write_text(
                json.dumps(
                    {
                        "step": step,
                        "files": {
                            str(p.relative_to(stage)): p.stat().st_size
                            for p in files
                            if p.is_file()
                        },
                    }
                ),
                encoding="utf-8",
            )
            with marker.open("r+b") as stream:
                os.fsync(stream.fileno())
            if previous.exists():
                shutil.rmtree(previous)
            if target.exists():
                target.replace(previous)
            try:
                stage.replace(target)
            except BaseException:
                if previous.exists() and not target.exists():
                    previous.replace(target)
                raise
            # Retain the preceding complete directory for interruption recovery.
        else:
            os.replace(stage, target)
    finally:
        if stage.is_dir():
            shutil.rmtree(stage)
        elif stage.exists():
            stage.unlink()
