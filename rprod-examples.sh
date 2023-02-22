# rprod examples

rprod md5sum *.txt
# Command mode
# Literal. No ../ allowed (implicit -l0)
# Read stdout (implicit -rstd)
# Write to stdout (implicit -wstd)

rprod -l md5sum /home/user/ ../*.foo  
# Command mode
# Literal + strip (-l)
# Read stdout
# Write to stdout
## Will index the entire home directory! stripped to ./user/
## More reasonable: /home/user/*.*, bash will expand...

rprod -wf result.log md5sum *.txt
# Command mode
# Literal. No ../ allowed (implicit -l0)
# Read stdout 
# Write to result.log


rprod -il $SCRIPTS/mylib.py -lx python $SCRIPTS/myscript.py 4 5  
# Command mode
# File injection with rename + extension (-lx)
# Read stdout
# Write to stdout
## The command that is run is actually "python file1.py 4 5"
## There must be no file called 4 or 5.
## You can move around myscript.py to different folders or rename it.
## In addition, it can import mylib.py

echo 'md5sum *' > script.sh
rprod -s -rstd -wstd script.sh *.txt
# Script mode (-s)
# File injection with rename + extension (implicit -lx)
# Read stdout (-rstd)
# Write to stdout (-wstd)
