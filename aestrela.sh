#!/bin/bash

if [ $6 == 1 ]
then
    python3 main.py $1 $2 $3 $4 $5 a-star manhattan
elif [ $6 == 2 ]
then
    python3 main.py $1 $2 $3 $4 $5 a-star octile
else
    echo "error: invalid heuristic"
fi
