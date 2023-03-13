import seamless

seamless.database_cache.connect()
seamless.database_sink.connect()

import seamless.highlevel
from seamless.metalevel.stdgraph import load as load_stdgraph

sctx = load_stdgraph("bash_transformer")
executor_code_checksum = sctx.executor_code.checksum
executor_code_buffer = sctx.executor_code.buffer
executor_code = sctx.executor_code.value

from seamless.imperative import _run_transformer, _get_semantic

semantic_code_checksum = _get_semantic(
    executor_code, bytes.fromhex(executor_code_checksum)
)
bashcode = "(ls $a; date) > RESULT"
result0 = _run_transformer(
    semantic_code_checksum,
    executor_code_buffer,
    bytes.fromhex(executor_code_checksum),
    signature=None,
    meta=None,
    args=[],
    kwargs={
        "bashcode": bashcode,
        "a": "/tmp",
        "pins_": ["a"],
    },
    celltypes={
        "a": "text",
        "bashcode": "text",
        "pins_": "plain",
        "result": "bytes",
    },
    result_callback=None,
)
try:
    result = result0.decode()
except Exception:
    result = result0
print(result)
