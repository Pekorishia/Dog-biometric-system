#!/bin/bash
DIR=$1
for filename in $DIR/big_pad_extracted_data/left/*.jpg; do
	convert "$filename" -compress none "$filename.ppm"
done

echo "done left"

for filename in $DIR/big_pad_extracted_data/right/*.jpg; do
	convert "$filename" -compress none "$filename.ppm"
done

echo "done left"
exit 0	