# load Seamless bash executor code, store it in the database
# TODO: bundle the code with rprod and pre-compute checksums,
#   so that Seamless is not needed at runtime

import seamless.highlevel
from seamless.metalevel.stdgraph import load as load_stdgraph
from seamless.imperative import _get_semantic

sctx = load_stdgraph("bash_transformer")
executor_code_checksum = sctx.executor_code.checksum
executor_code_buffer = sctx.executor_code.buffer
executor_code = sctx.executor_code.value
semantic_code_checksum = _get_semantic(
    executor_code, bytes.fromhex(executor_code_checksum)
)
del sctx

# /TODO

# TODO: abstract _run_transformer, also to support communion
# (and also to support messaging, to see if the transformation already exists)
from seamless.imperative import _run_transformer as run_transformer

# / TODO


def run_bash_transformation(
    code: str,
    checksum_dict: dict[str, str],
    *,
    directories: list[str],
    result_mode: str
) -> str:
    """Runs a bash transformation.

    Input:

    - code: bash code to execute inside a workspace. The code must write its result:
        - to /dev/stdout if result_mode is "stdout"
        - or: to a file called RESULT, if result_mode is "file"
        - or: to a directory called RESULT, if result_mode is "directory"
    - checksum_dict: checksums of the files/directories to be injected in the workspace
    - directories: list of the keys in checksum_dict that are directories
    """
    if result_mode not in ("file", "directory", "stdout"):
        raise TypeError(result_mode)

    if result_mode == "directory":
        raise NotImplementedError

    if len(directories):
        raise NotImplementedError

    if result_mode == "stdout":
        bashcode = "(\n" + code + "\n) > RESULT"
    else:
        raise NotImplementedError

    pins = sorted(checksum_dict.keys())
    kwargs = {
        "bashcode": bashcode,
        "pins_": pins,
    }
    assert "bashcode" not in checksum_dict  # TODO: workaround
    assert "pins_" not in checksum_dict  # TODO: workaround

    kwargs.update(checksum_dict)
    celltypes = {
        "bashcode": "text",
        "pins_": "plain",
        "result": "bytes",
    }
    for pin in pins:
        celltypes[pin] = "bytes"

    result0: bytes = run_transformer(
        semantic_code_checksum,
        executor_code_buffer,
        bytes.fromhex(executor_code_checksum),
        signature=None,
        meta=None,
        args=[],
        kwargs=kwargs,
        celltypes=celltypes,
        result_callback=None,
        modules={},
        checksum_kwargs=list(checksum_dict.keys()),
    )
    try:
        result = result0.decode()
    except UnicodeDecodeError:
        result = result0
    return result

    # TODO: add support for filesystem __format__ annotation
