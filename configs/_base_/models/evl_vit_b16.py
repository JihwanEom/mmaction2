# model settings
model = dict(
    type='Recognizer2D',
    backbone=dict(
        type='EVLTransformer',
        num_frames=32,
        decoder_qkv_dim=768,
        decoder_num_heads=12,
        backbone_name='ViT-B/16-Inpre'
        ),
    cls_head=dict(
        type='EVLHead',
        num_classes=51,
        in_channels=768,
        ),
    # model training and testing settings
    train_cfg=None,
    test_cfg=dict(average_clips='prob'))
