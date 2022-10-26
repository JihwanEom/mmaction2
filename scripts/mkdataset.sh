seeds=(0 1 2 3 4 5 6 7 8 9)
num_classes=10
for seed in ${seeds[@]}
    do
    python generate_SC_dataset.py data/jester/ tools/data/jester/label_map.txt SC_jester_${num_classes}cls_12_samples_seed_${seed} \
    --n_classes ${num_classes} --n_samples 12 --n_train_ratio 0.5 --n_min_frames 30 --seed ${seed}
    done

for seed in ${seeds[@]}
    do
    python generate_SC_dataset.py data/hmdb51/ tools/data/hmdb51/label_map.txt SC_hmdb51_${num_classes}cls_12_samples_seed_${seed} \
    --n_classes ${num_classes} --n_samples 12 --n_train_ratio 0.5 --seed ${seed}
    done

for seed in ${seeds[@]}
    do
    python generate_SC_dataset.py data/ucf101/ tools/data/ucf101/label_map.txt SC_ucf101_${num_classes}cls_12_samples_seed_${seed} \
    --n_classes ${num_classes} --n_samples 12 --n_train_ratio 0.5 --seed ${seed}
    done