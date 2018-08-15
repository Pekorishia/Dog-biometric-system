#!/bin/bash

echo "making tom" &&
./make_wo_ppm.sh "dataset/Tom-Lhasa_Apso" "tom" &&

echo "making nina" &&
./make_wo_ppm.sh "dataset/Nina-Beagle" "nina" &&

echo "making lulu" &&
./make_wo_ppm.sh "dataset/Lulu-German_Spitz" "lulu" &&

echo "making love" &&
./make_wo_ppm.sh "dataset/Love-Golden_Retriever" "love" &&

echo "making lola" &&
./make_wo_ppm.sh " dataset/Lola-Greyhound_mix" "lola" &&

echo "making lady" &&
./make_wo_ppm.sh "dataset/Lady-mutt" "lady" &&

echo "making francis" &&
./make_wo_ppm.sh "dataset/Francis-Bulldog" "francis" &&

echo "making connie" &&
./make_wo_ppm.sh "dataset/Connie-West_Terrier" "connie" &&

echo "making brisa" &&
./make_wo_ppm.sh "dataset/Brisa-Shih_Tzu brisa" &&

echo "making bolt" &&
./make_wo_ppm.sh "dataset/Bolt-Bulldog_Ingles" "bolt" &&

exit 0	