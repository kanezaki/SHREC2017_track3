#!/bin/bash

subset=$1
mode=$2 # normal or perturbed

if [ $mode == 'normal' ]
then
    echo "aligned model"
    caffemodel=./models/rotationnet_alex_SHREC2017_SUB_case2_b900_ratio_iter_78000.caffemodel
else
    echo "unaligned model"
    caffemodel=./models/rotationnet_alex_SHREC2017_SUB_case2_b900_ratio_perturbed_iter_78000.caffemodel
fi

dirname=results_alex_ratio_subclass
mkdir -p $dirname


# compute and save scores.

if [ $subset == 'test' ]
then
    if [ `ls $dirname/${subset}_${mode}.npy 2>/dev/null | wc -l` -ne 1 ]
    then
	python save_scores.py --center_only --gpu --model_def prototxt/deploy_alex_subclass.prototxt --pretrained_model $caffemodel --input_file TXT/${subset}_${mode}.txt --output_file $dirname/${subset}_${mode}.npy
	python save_scores_txt.py $dirname/${subset}_${mode}.npy 203 >$dirname/${subset}_${mode}.txt
    fi
    exit
fi

for ((c=0;c<55;c++))
do
    if [ `ls $dirname/${subset}_${mode}_$c.npy 2>/dev/null | wc -l` -ne 1 ]
    then
	python save_scores.py --center_only --gpu --model_def prototxt/deploy_alex_subclass.prototxt --pretrained_model $caffemodel --input_file TXT/${subset}_${mode}_$c.txt --output_file $dirname/${subset}_${mode}_$c.npy
	python save_scores_txt.py $dirname/${subset}_${mode}_$c.npy 203 >$dirname/${subset}_${mode}_$c.txt
    fi
done


