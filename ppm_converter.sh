#!/bin/bash
DIR=$1

# for each .jpg file inside $DIR/big_pad_extracted_data/left/
for filename in $DIR/big_pad_extracted_data/left/*.jpg; do
	convert "$filename" -compress none "$filename.ppm"
done

# for each .jpg file inside $DIR/big_pad_extracted_data/right/
for filename in $DIR/big_pad_extracted_data/right/*.jpg; do
	convert "$filename" -compress none "$filename.ppm"
done

echo "Done image conversion (jpg to ppm)."
exit 0	