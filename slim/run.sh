rm -rf /tmp/tfmodel/
rm -f /tmp/tf_log
DATASET_DIR=/home/utagar/tensorflow_new_instrumented/cifar10/alexnet/train_tfrec
python train_image_classifier.py --dataset_name=imagenet --dataset_split_name=train --dataset_dir=${DATASET_DIR} --max_number_of_steps=$1 --batch_size=$2 --model_name=alexnet_v2 > log 2>vlog
cp /tmp/tf_log ./time_stats
a="$(grep -nE 'Epoch 1$' vlog | cut -d: -f1)"
b="$(grep -nE 'Epoch 2$' vlog | cut -d: -f1)"
((a+=1))
((b-=1))
sed -n "${a},${b}p" vlog > tmp
grep Algo: tmp | awk {'print $5,$6'}  > algo1
grep Algo_BackPropData: tmp | awk {'print $5,$6'}  > algo2
grep Algo_BackPropFilter: tmp | awk {'print $5,$6'}  > algo3
rm -f tmp
python parse.py 1 1 > algo_convolution
c="$(wc -l algo2 | awk {'print $1'})"
python parse.py 2 "$c" > algo_convolution_backprop_data
c="$(wc -l algo3 | awk {'print $1'})"
python parse.py 3 "$c" > algo_convolution_backprop_filter
a="$(grep -nE 'Epoch 4$' vlog | cut -d: -f1)"
b="$(grep -nE 'Epoch 5$' vlog| cut -d: -f1)"
((a+=1))
((b-=1))
sed -n "${a},${b}p" vlog > tmp
grep Ker tmp | awk {'print $7,$9,$11,$13'} > ker_stats
grep Mem tmp | awk {'print $7,$9,$11,$13'} > mem_stats
