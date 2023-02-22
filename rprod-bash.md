# rprod-bash

This is to run rprod from the command line.

## rprod --local and sessions

The first thing `rprod --local` does is to look for a session file. The session file name is based on the process id of the bash shell (that started `rprod --local`). If the session file does not exist, it will create it (first do `ps` and check if there isn't any older rprod sibling process that should be creating it already). Creating a session file means: writing a header and then looking for the Seamless database, potentially creating it as a subprocess. Failure to create a database is written into the session file, poisoning all future `rprod --local` invocations. If there is Slurm ncores/mem etc, this is written into the session file as well.

There are a number of session-changing commands, such as `rprod --session ncores X`, these write into the session file and exit.

`rprod --local` has two open file objects to the session file: one for read, one for append. Use *fcntl* to acquire a lock on the file when writing.
Once it has those opened, it writes a "submit" entry in the session, and the polling phase starts. Essentially, it reads all entries in the session, especially the "submit" and "finished" entries, and figures out if its turn has come (this is deterministic, FIFO). If its turn has come, it executes its transformation, and writes a "finished" entry. (Afterwards, it exits unless it has created the database). If its turn has not yet come, it does some more polling. Polling consists of a) periodic `file.readline` on the session file and b) checking `ps` to detect crashed rprod processes (that didn't write their "finished" entry properly). Essentially, a) should happen more often than b), and both should happen less often if there are a lot of waiting rprod processes before it. Experiment: creating 1000 processes with a long sleep (time.sleep(20)) is no problem. So the first 20 processes could poll every 0.5 sec, process 21-39 could poll from 0.5 sec to 20 secs, and every 20 secs for process 40-9999.

With `--local`, you must run `rprod --wait` (no arguments) at the end of the shell, which does `rprod --collect` and then stops the database and cleans up the session file. Best to do `trap EXIT 'rprod --wait'`. This cleans up *all* leftover session files, not just the one from the current session. "Leftover" means that the bash shell process is no longer running.
If you only use `--remote`, you may use `rprod --wait`, but normal `wait` may suffice.

`rprod --collect` waits for all running rprod processes to finish, both local and remote. A local rprod process is considered running if it has written a "submit" entry in the session file AND not yet a "finished" entry AND the process id is listed by `ps`.

`rprod` has options such as `--ncores X`, `--mem` etc. For `--local`, these are used to determine whether its turn has yet come. For `--remote`, these are passed on as "__meta__" fields to run_transformation. `--local` also has fields that describe the minimum amount of free cores / free memory. These are enforced at the beginning of the *execution* phase, i.e. execution is halted until those resources are available, but they are disregarded by downstream `rprod` processes in determining if it is their turn or not.

`rprod` is always blocking, but you can do `rprod ... &` and then `rprod --wait` (or `--collect`), or else `PID=$!` to get the process ID. You can then do `rprod --wait $PID $PID2 ...` or `rprod --collect $PID $PID2 ...`, these do the same thing and do not kill any database.