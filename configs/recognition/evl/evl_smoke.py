_base_ = ['../../_base_/default_runtime.py']
num_classes = 2
num_frames = 8
num_strides = 4
# model settings
model = dict(
    type='Recognizer2D',
    backbone=dict(
        type='EVLTransformer',
        num_frames=num_frames,
        decoder_qkv_dim=768,
        decoder_num_heads=12,
        backbone_name="ViT-B/16-lnpre",
        backbone_path='ViT-B-16.pt'
        ),
    cls_head=dict(type='EVLHead', num_classes=num_classes, in_channels=768),
    # model training and testing settings
    train_cfg=None,
    test_cfg=dict(average_clips='prob'))


# dataset settings
dataset_type = 'RawframeDataset'
data_root = 'data/smoke/rawframes'
data_root_val = 'data/smoke/rawframes'
ann_file_train = f'data/smoke/rawframes/train_list_rawframes.txt'
ann_file_val = f'data/smoke/rawframes/val_list_rawframes.txt'
ann_file_test = f'data/smoke/rawframes/val_list_rawframes.txt'
# split = 1
# dataset_type = 'RawframeDataset'
# data_root = 'data/hmdb51/rawframes'
# data_root_val = 'data/hmdb51/rawframes'
# ann_file_train = f'data/hmdb51/hmdb51_train_split_{split}_rawframes.txt'
# ann_file_val = f'data/hmdb51/hmdb51_val_split_{split}_rawframes.txt'
# ann_file_test = f'data/hmdb51/hmdb51_val_split_{split}_rawframes.txt'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_bgr=False)

train_pipeline = [
    dict(type='SampleFrames', clip_len=num_frames, frame_interval=num_strides, num_clips=1),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='RandomResizedCrop'),
    dict(type='Resize', scale=(224, 224), keep_ratio=False),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='pytorchvideo.RandAugment'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
val_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=num_frames,
        frame_interval=num_strides,
        num_clips=1,
        test_mode=True),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
test_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=num_frames,
        frame_interval=num_strides,
        num_clips=1,
        test_mode=True),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]

data = dict(
    videos_per_gpu=32,
    workers_per_gpu=8,
    test_dataloader=dict(videos_per_gpu=1),
    train=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        data_prefix=data_root,
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        data_prefix=data_root_val,
        pipeline=val_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        data_prefix=data_root_val,
        pipeline=test_pipeline))

evaluation = dict(
    interval=1, metrics=['top_k_accuracy', 'mean_class_accuracy'], save_best='top1_acc')

# optimizer
optimizer = dict(
    type='AdamW',
    lr=4e-4,
    weight_decay=0.05,
)
optimizer_config = dict(grad_clip=dict(max_norm=40, norm_type=2))

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0)
total_epochs = 15

# runtime settings
checkpoint_config = dict(interval=1, max_keep_ckpts=3)
fp16=dict(loss_scale='dynamic')
# runtime settings
work_dir = './work_dirs/EVL_smoke_ViT-B-16_SC'
load_from='k400_vitb16_8f_dec4x768_mm.pth'