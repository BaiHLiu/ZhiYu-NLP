#!/bin/zsh

cd /home/lbh/lzy/GPT2-NewsTitle-main 
conda activate NLP
nohup python api.py --device=0 --port=12345 &

nohup python api.py --device=0 --port=12346 &

nohup python api.py --device=1 --port=12347 &

nohup python api.py --device=1 --port=12348 &
