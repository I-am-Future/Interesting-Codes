#!/bin/bash

# or zsh? #! /bin/zsh

# Kill the session if it exists
tmux kill-session -t proj

# Create a new tmux session in the background
tmux new-session -d -s proj

# Split the window into 2 rows (upper and lower)
tmux split-window -h -t proj:0.0

# Send echo messages to each panel
tmux send-keys -t proj:0.0 'echo "Panel 1"; cd ~/.cache' C-m
tmux send-keys -t proj:0.1 'echo "Panel 2"; cd ~/.cache' C-m

# Attach to the session
tmux attach -t proj

