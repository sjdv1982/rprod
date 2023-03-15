function _rprod_complete() {
    echo $READLINE_LINE
    READLINE_LINE=$(_rprodize $READLINE_LINE @@@ $RPROD_OPTS)
}

function rprod-auto() {
    if [ -z "$_RPROD_OLD_PS1" ]; then
        _RPROD_OLD_PS1=$PS1
        PS1='\033[01;95m\][rprod]\033[00m\]\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ \[\]\[\]'
    fi
    RPROD_OPTS=$*
    if [ -z "$1" ]; then
        RPROD_OPTS=''
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
        PS1=$_RPROD_OLD_PS1
        unset _RPROD_OLD_PS1
    fi

}

function rprod-auto-toggle() {
    if [ -n "$RPROD_AUTO_ON" ]; then
        unset RPROD_AUTO_ON
        rprod-auto-off
    else
        RPROD_AUTO_ON=1
        rprod-auto
    fi 
}    

bind -x '"\C-tt":rprod-auto-toggle'
echo 'rprod-auto-toggle: Press Ctrl-T, then T '

