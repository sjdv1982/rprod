import sys
import pathlib
import os

if "SEAMLESS_DATABASE_IP" not in os.environ:
    os.environ["SEAMLESS_DATABASE_IP"] = "localhost"
if "SEAMLESS_DATABASE_PORT" not in os.environ:
    os.environ["SEAMLESS_DATABASE_PORT"] = "5522"

command = sys.argv[1:]
assert len(command), sys.argv

import seamless

seamless.database_cache.connect()
seamless.database_sink.connect()

import seamless.highlevel
from seamless.metalevel.stdgraph import load as load_stdgraph

sctx = load_stdgraph("bash_transformer")
executor_code_checksum = sctx.executor_code.checksum
executor_code_buffer = sctx.executor_code.buffer
executor_code = sctx.executor_code.value


def get_pins_literal(command):
    # policy: extension/slash makes no difference
    pins = []
    currdir = pathlib.Path(".").resolve()
    for token in command:
        path = pathlib.Path(token)
        if path.exists():
            path = path.resolve()
            if currdir not in path.parents:
                raise ValueError(token)
            pins.append(token)
    return pins


def run_command_literal(command):
    from seamless.imperative import _run_transformer, _get_semantic

    pins = get_pins_literal(command)
    cmd = " ".join(command)
    semantic_code_checksum = _get_semantic(
        executor_code, bytes.fromhex(executor_code_checksum)
    )
    bashcode = "(\n" + cmd + "\n) > RESULT"
    kwargs = {
        "bashcode": bashcode,
        "pins_": pins,
    }
    celltypes = {
        "bashcode": "text",
        "pins_": "plain",
        "result": "bytes",
    }
    for pin in pins:
        with open(pin, "rb") as f:
            kwargs[pin] = f.read()
        celltypes[pin] = "bytes"

    result0: bytes = _run_transformer(
        semantic_code_checksum,
        executor_code_buffer,
        bytes.fromhex(executor_code_checksum),
        signature=None,
        meta=None,
        args=[],
        kwargs=kwargs,
        celltypes=celltypes,
        result_callback=None,
        modules={}
    )
    try:
        result = result0.decode()
    except UnicodeDecodeError:
        result = result0
    return result


print(run_command_literal(command))
