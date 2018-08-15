#!/bin/bash
DIR=$1
ID=$2

# for each .ppm file inside $DIR/image_processing/binarized/left/
for filename in $DIR/image_processing/binarized/left/*.ppm; do
	python image_processor/shapes_detector/detector.py -i "$filename" -oi "$DIR/image_processing/shape_detected/left/$(basename "$filename")_shapes.ppm" -of "$DIR/image_processing/shape_detected/left/$(basename "$filename")_output_file.txt" --label "l_$ID"
done

# for each .ppm file inside $DIR/image_processing/binarized/right/
for filename in $DIR/image_processing/binarized/right/*.ppm; do	
	python image_processor/shapes_detector/detector.py -i "$filename" -oi "$DIR/image_processing/shape_detected/right/$(basename "$filename")_shapes.ppm" -of "$DIR/image_processing/shape_detected/right/$(basename "$filename")_output_file.txt" --label "r_$ID"
done

echo "Done shape detector."
exit 0	