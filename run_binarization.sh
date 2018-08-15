#!/bin/bash
DIR=$1

COUNT=0

# for each .ppm file inside $DIR/big_pad_extracted_data/left/
for filename in $DIR/big_pad_extracted_data/left/*.ppm; do
	# generate 19 binarized images based on the threshold values bellow
	for number in 32 40 48 56 64 72 80 88 96 104 112 120 128 136 144 152 160 168 176;	do
		./image_processor/generate_binarized_img/binarization "$filename" "$number"  "$DIR/image_processing/binarized/left/$(basename "$filename")_$number"
	done
	let COUNT+=1
done

# reset counter
COUNT=0

# for each .ppm file inside $DIR/big_pad_extracted_data/right/
for filename in $DIR/big_pad_extracted_data/right/*.ppm; do	
	# generate 19 binarized images based on the threshold values bellow
	for number in 32 40 48 56 64 72 80 88 96 104 112 120 128 136 144 152 160 168 176;	do
		./image_processor/generate_binarized_img/binarization "$filename" "$number"  "$DIR/image_processing/binarized/right/$(basename "$filename")_$number"
	done
	let COUNT+=1
done

echo "Done binarization."

exit 0	