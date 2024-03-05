_base_ = '../mmdetection/configs/swin/mask-rcnn_swin-t-p4-w7_fpn_ms-crop-3x_coco.py'

model = dict(
    roi_head=dict(
        type='StandardRoIHead',
        bbox_head=dict(
            type='Shared2FCBBoxHead',
            num_classes=1,
        ),
        mask_head=dict(
            type='FCNMaskHead',
            num_classes=1,
        )))

data_root = '/content/dataset/'
metainfo = {
    'classes': ('receipt', ),
    'palette': [
        (220, 20, 60),
    ]
}

train_pipeline = [
    dict(type='LoadAnnotations', with_bbox=False, with_mask=True),
]

train_dataloader = dict(
    batch_size=3,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='train/_annotations.coco.json',
        data_prefix=dict(img='train/')))
val_dataloader = dict(
    batch_size=3,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='valid/_annotations.coco.json',
        data_prefix=dict(img='valid/')))
test_dataloader = dict(
    batch_size=1,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='test/_annotations.coco.json',
        data_prefix=dict(img='test/')))

val_evaluator = dict(ann_file=data_root + 'valid/_annotations.coco.json')
test_evaluator = dict(ann_file=data_root + 'test/_annotations.coco.json')

train_cfg = dict(max_epochs=5)

load_from = "/content/mmdetection/work_dirs/my_model/epoch_8.pth"
