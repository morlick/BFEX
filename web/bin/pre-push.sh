#!/bin/bash

# Get the base of your git install
GIT_WORK_TREE=$(git rev-parse --show-toplevel)

echo $@

# If running the script without arguments, install pre-push to hooks.
if [[ $# -eq 0 ]]; then
    echo "Installing pre-push hook."
    cp -f $GIT_WORK_TREE/web/bin/pre-push.sh $GIT_WORK_TREE/.git/hooks/pre-push
    chmod +x $GIT_WORK_TREE/.git/hooks/pre-push
    echo "Installed pre-push hook."
else
    source activate BFEX
    pytest $GIT_WORK_TREE/web/test
fi