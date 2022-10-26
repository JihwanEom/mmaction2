#!/bin/bash
export CUDA_VISIBLE_DEVICES=1
# classification
dirname=~/video_workspace/time_ratio/
mkdir -p ${dirname}
logname=${dirname}/mmaction_ucf101_training_log.txt
start_time=`date +%y/%m/%d-%T`
echo exp_start:$start_time > ${logname}
python3 tools/train.py configs/recognition/evl/evl_ucf101_rgb.py --seed 0 --deterministic --validate --gpus 1 | tee -a ${logname}
end_time=`date +%y/%m/%d-%T`
echo exp_end:$end_time >> ${logname}

