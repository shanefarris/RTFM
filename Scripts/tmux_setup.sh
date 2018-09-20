#!/bin/bash

if [ $# -eq 2 ]; then
    echo 'Specify tmux session name'
    exit
else
    $SESSIONNAME="$1"
    tmux has-session -t $SESSIONNAME &> /dev/null
    tmux new -s $SESSIONNAME 
fi
