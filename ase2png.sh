#!/bin/bash
filename=$(basename $1)
filename=${filename%.*}
foldername=$(dirname $1)
tmp_json=$foldername/$filename/__tmp.json
layer_file=$foldername/$filename/layers.txt

# Export png
aseprite -b --split-layers $1 \
    --filename-format '{path}/{title}/{tag}-{group}{layer}.{extension}' \
    --save-as ${1%.*}.png

# Export layer order
aseprite -b --list-layers $1 --data $tmp_json > /dev/null
cat $tmp_json | \
    jq '.meta.layers[] | if .opacity then (.group+ .name) else empty end' | \
    tac | \
    tr -d '"' \
    > $layer_file
rm $tmp_json
