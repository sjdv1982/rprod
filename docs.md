# Reproducibility

In Python mode, rprod always leads to reproducible calculations.

Reproducibility in bash mode is based on whether rprod can correctly distinguish between files and values. Here, we can distinguish between false positives and false negatives.

## False positives

A false positive means that a file argument is identified (and checksummed) where it
should be a value.

Pathological example:

```bash
rprod 'date > /tmp/TEMP; echo 1 >> /tmp/TEMP; tail -n 1 /tmp/TEMP` .
```
Here, the result is always 1, but it will not federate because:

- /tmp/TEMP is seen as an input, while it is not.
- the content of /tmp/TEMP always changes.

Putting the command in a script and running rprod in script mode will prevent this.

## False negatives

A false negative means that a file argument is not checksummed because it is not recognized as such. 

Example:

- We have the following script `count-files.sh`:

```bash
#!/bin/bash
filepattern=$1
ls $filepattern* | wc -l
```

- We have the contents of `/tmp` with three files: `a1`, `a2`, `a3`

- We run the following command:

`rprod -s -rstd -wstd count-files.sh /tmp/a`

In this case /tmp/a is a *file pattern*, but rprod cannot recognize that. Using file patterns in bash scripts is bad design and should be avoided, and here it bites you. The result is 3, but if we remove e.g. `/tmp/a1`, the result federates and remains 3.

A solution is to write an `count-files.rprod` script that returns first:
```json
{
    "command": "count-files.sh /tmp/a",
    "literal_files": ["count-files.sh", "/tmp/a1", "/tmp/a2", "/tmp/a3"]
}
```

and then:

```json
{
    "command": "count-files.sh /tmp/a",
    "literal_files": ["count-files.sh", "/tmp/a2", "/tmp/a3"]
}
```

Note that this still doesn't federate against file renames or argument reordering.

# Federation

...