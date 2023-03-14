function _rprod_complete() {
    local skip 
    local skipwords
    local ins
    local ins2
    skipwords="rprod rprod-auto rprod-auto-off \
cd rm ls mv cp \
exit source echo function set let export \
conda mamba pip apt \
code nano vi emacs gedit"
    skip=$(echo """$skipwords
$READLINE_LINE""" | python -c '''
import sys, re
skipwords = sys.stdin.readline().strip().split()
line = sys.stdin.read()
words = re.split(r"[^a-zA-Z0-9_-]+", line)
if len(words) > 0 and words[0] in skipwords:
    print(1)
else:
    print(0)''')
    if [ $skip == "0" ]; then 
        ins="rprod $RPROD_OPTS '"
        ins2="'" 
        lins=$(echo $ins | awk '{print length($0)}')
        READLINE_LINE=$ins$READLINE_LINE$ins2
        READLINE_POINT=$((READLINE_POINT + lins))
        READLINE_MARK=$((READLINE_MARK + lins))
    fi
}

function rprod-auto() {
    if [ -z "$_RPROD_OLD_PS1" ]; then
        _=''
        ###_RPROD_OLD_PS1=$PS1
        ###PS1='\033[01;31m\][rprod]\033[00m\]'$PS1
    fi
    RPROD_OPTS=$*
    if [ -z "$1" ]; then
        RPROD_OPTS='-c'
    fi
    echo 'rprod auto ON'
    echo "rprod options: $RPROD_OPTS"
    bind -x '"\C-t1":_rprod_complete'
    bind '"\C-t2": accept-line'
    bind '"\C-M":"\C-t1\C-t2"'
}


function rprod-auto-off() {
    echo 'rprod auto OFF'
    bind '"\C-M": accept-line'
    if [ -n "$_RPROD_OLD_PS1" ]; then
        _=''
        ###PS1=$_RPROD_OLD_PS1
    fi

}
