#!/bin/bash
DIR=$1 &&
ID=$2 &&

echo "Start binarization" &&
./run_binarization.sh $DIR &&

echo "Start shape detection" &&
./run_shape_detector.sh $DIR $ID &&

echo "done make without image conversion." &&
exit 0	