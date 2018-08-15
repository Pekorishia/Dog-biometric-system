#!/bin/bash
DIR=$1 &&
ID=$2 &&

echo "Start .jpg to .ppm conversion" &&
./ppm_converter.sh $DIR &&

echo "Start binarization" &&
./run_binarization.sh $DIR &&

echo "Start shape detection" &&
./run_shape_detector.sh $DIR $ID &&

echo "done make." &&
exit 0	