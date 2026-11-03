"""Publish complete checkpoints without destroying the previous successful save."""

from __future__ import annotations

import json
import os
import random
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import torch


def capture_rng() -> dict:
    numpy_state = np.random.get_state()
    # Primitive values and tensors keep torch.load(weights_only=True) usable.
    return {
        "python": random.getstate(),
        "numpy": [numpy_state[0], numpy_state[1].tolist(), *numpy_state[2:]],
        "torch": torch.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
    }


def restore_rng(state: dict) -> None:
    random.setstate(state["python"])
    name, keys, position, gaussian, cached = state["numpy"]
    np.random.set_state((name, np.asarray(keys, dtype=np.uint32), position, gaussian, cached))
    torch.set_rng_state(state["torch"].cpu())
    if state["cuda"] and torch.cuda.is_available():
        torch.cuda.set_rng_state_all([value.cpu() for value in state["cuda"]])


@contextmanager
def preserve_rng():
    state = capture_rng()
    try:
        yield
    finally:
        restore_rng(state)


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
