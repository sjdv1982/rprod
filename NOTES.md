# Notes

- Bash mode: have something to split sys.argv into tokens so that we can do:
 `rprod 'echo 1; echo 2'`

- Bash mode: have `--celltype <celltype> <filename>` syntax. To federate with Seamless.

- Bash mode: option to reorder arguments by checksum (for order-independent argument lists)

- rprod can be nested/re-entrant, i.e you can use rprod on code using rprod. In rprod-py, nesting works out of the box. Transformers auto-import @transformation not from rprod, but from `seamless.imperative`. Non-blocking works.
In rprod-bash, nesting works because of backends. Non-blocking works with '&' and `wait`/ `rprod --wait`.

- Add rprod to the seamless-minimal image (seamless-minimal mode, disallow dummy)
Only limitation: only local, because SEAMLESS_COMMUNION_PORT is normally not made available by jobless.

- rprod --env option will take a conda YAML file / Docker image name

- rprod config:

  - allowed back-end modes

  - Is Silk a requirement? Will be needed for "mixed" celltypes if form is not pure-plain/pure-binary.

  Or else embed Silk routines in rprod?

- rprod-bash core: have an abstracted "database.send" where it can send (non-code) buffers and then forget about them, working only with the checksums.

- rprod-bash core: describe bash transformers as language="bash". Only in the Seamless backends then convert them to language="python" as shown in tests/bash2.py.

- `__format__` in Seamless transformers supports hash pattern and filesystem. Add support for both in rprod-bash Seamless backends. Directories must be `celltype=mixed, hash_pattern={"*":"##"}`. All file arguments must have filesystem just like Seamless bash transformers.

- rprod gui: Have a HTML GUI, hooked up to a Seamless database, that takes a transformation checksum and visualizes it as JSON with clickable links / value expansion.

- Interpret `rprod wait` as `rprod --wait`, with a warning.

- Take care with file locking: "POSIX File locking as available with fcntl(F_SETLK): the POSIX locking API is the most portable one and in theory works across NFS. ... locking cannot be used on any file that is publicly accessible (i.e. has the R bit set for groups/others, i.e. more access bits on than 0600), because that would otherwise effectively give arbitrary users a way to indefinitely block execution of any process (regardless of the UID it is running under) that wants to access and lock the file. This is generally not an acceptable security risk. Finally, while POSIX file locks are supposedly NFS-safe they not always really are as there are still many NFS implementations around where locking is not properly implemented, and NFS tends to be used in heterogenous networks. The biggest problem about this is that there is no way to properly detect whether file locking works on a specific NFS mount (or any mount) or not."
Still, locking should be a backup mechanism since appends under 4K should be atomic under Linux. F_SETLK is sufficient (Python fcntl.lockf, exclusive lock = write lock), no need for F_OFD_SETLK. Flush after every write! 