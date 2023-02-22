## Gnu parallel 

### nuggets

--pipe
The --pipe functionality puts GNU parallel in a different mode: Instead of treating the data on stdin (standard input) as arguments for a command to run, the data will be sent to stdin (standard input) of the command.

--jobs 0 will run as many jobs in parallel as possible


### ramblings about GNU parallel

and there is the "sem" `parallel --semaphore` mode... 

All of this sucks if you want to reserve a number of nodes and an amount of memory for local jobs! And it sucks if you have many!
There is async (https://github.com/ctbur/async/), but it is hard to install and unmaintained.