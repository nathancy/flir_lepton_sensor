# Script to open up latest thermal image photo
TOTAL_FILES=$(ls | wc -l)
IMAGE_ID=`expr $TOTAL_FILES - 3`
EXTENTION=".png"
IMAGE=$IMAGE_ID$EXTENTION
links2 -g $IMAGE

