# rprod

- rprod will consist of two parts: rprod-bash and rprod-py. All in the same conda/pip package.
  rprod-bash: rprod command line tool.
  rprod-py: "from rprod import transformer" decorator (only public API).
  Both will use rprod py library to synthesize transformation
  Copy a bit of code from seamless.imperative to synthesize

# rprod-bash

## Run modes

- Command mode: synthesize a command line (default)
- Script mode: constant bash code, insert files and variables

## Guess modes

How to guess what is a file and what is a value

1. Any argument with extension that exists as a file or directory is a file or directory
2. Any argument with extension that does not exist => stop
3. Any argument ending with a slash must be a directory, else => stop
4. Any argument without extension that exists as directory is a directory
5. Any argument without extension that does not exist as a file or directory is a value
6. Any argument without extension that exists as a file => stop

All rules can be overridden for individual items.
2., 3., 6. can be overridden for the entire invocation => value

Be very verbose. Dry-run option. Give individual sizes, say what needs to be uploaded to the database.
Indicate if there is a result, and how much it is to download.

## File injection mode

- Literal (default for command mode). Least reproducible. All paths must be subfolders of the current directory.
- Literal, but strip directories. No subfolder restriction, but no files can have same name.
- Rename to file1.py, file2.txt, etc. (default for script mode)
- Rename to file1, file2, etc. Most reproducible, but least informative error messages. Some tools may fail.
- No guessing at all, require assistant.

Add an include (-i) option to inject additional files not part of the command. You can do -il to specify -l for those files, -ilx for -lx, etc.

## Result read modes

- Read from stdout (default in command mode)
- Read from RESULT (default in script mode)
- Read from specified file

Can launch if result read mode is defined, even if result report mode is not. Just relaunch later, result will be instant.

## Result report mode

Rprod always writes stderr to stderr, unless cache hit.

- Print to stdout (default in command mode)
- Print just the checksum (default in script mode)
- Save to a specified file

## Assistants

For script mode, as_file or as_var can be read from comments in the script, if the order is fixed and no options.

Command/script assistant (.rprod or .rprod.py/.rprod.sh/.rprod.bash extension, same name as script/command. Look in same dir as script, and in special directory too)
Script, must be executable, normally Python script with argparse.
If not executable, must be .rprod and contain '#' comments.
Invoked with the command line
Returns:

1. Dict where:
    - key is a file name or env var
    - value indicates: as_file or as_var, and the name
1a. Dict of "literal_files":list, "files":dict, "vars":dict.
2. In command mode: return synthesized command as well


## Backend modes

## rprod back-end mode "dummy"

"rprod" does nothing. "transformer" decorator does nothing.

## rprod back-end mode "seamless-network"

Need to make SEAMLESS_DATABASE and SEAMLESS_COMMUNION connections.
Send buffers/transformations there.
Only --remote, or: --local => --remote  (depends on config)
This mode could have config support for multiple remotes.

## rprod back-end mode "seamless-sandbox"

Try to make SEAMLESS_DATABASE and SEAMLESS_COMMUNION connections
If no Seamless database can be found, rprod library will launch one, for the duration of the process.
rprod-bash: run scripts/run-transformation.py for --local. --remote needs
SEAMLESS_DATABASE/SEAMLESS_COMMUNION connections, identical to "seamless-network".
rprod-py: import transformation from seamless.imperative. Seamless will auto-connect itself to SEAMLESS_COMMUNION
This mode could have config support for multiple remotes.

### rprod back-end mode "seamless-minimal"

Runs inside transformations, both local and seamless-minimal Docker image.
In both of those cases, set an environment variable to enforce "seamless-minimal".
Works the same as "seamless-sandbox", but SEAMLESS_DATABASE MUST exist.