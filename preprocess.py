import os
import json
import argparse

from pycocotools.coco import COCO

OUTPUT_FILE_NAME = 'train.txt'

def preprocess(config_path):
    cfg = None
    with open(config_path) as reader:
        cfg = json.load(reader)

    anno_file_path = cfg['annotation_file_path']
    coco = COCO(anno_file_path)

    images = coco.dataset['images']
    image_ids = list(map(lambda image: [image['id']], images))
    all_annotations = list(map(lambda image_id: coco.loadAnns(coco.getAnnIds(image_id)), image_ids))

    images_dir_path = cfg['images_dir_path']

    print('Creating str annotation for images...')
    datasets = list()
    for image, annotations in zip(images, all_annotations):
        bbox_strs = list()
        for annotation in annotations:
            bbox_str = list(map(str, annotation['bbox']))
            cls_str = str(annotation['category_id'])
            bbox_str.append(cls_str)
            if len(bbox_str) > 0:
                bbox_strs.append(",".join(bbox_str))
            else:
                bbox_strs.append("")

        anno_str = ' '.join(bbox_strs)

        image_file_name = image['file_name']

        image_file_path = os.path.join(images_dir_path, image_file_name)

        dataset = '{} {}'.format(image_file_path, anno_str)

        datasets.append(dataset)

    datasets_str = '\n'.join(datasets)

    save_dir_path = cfg['output_dir_path']
    save_file_path = os.path.join(save_dir_path, OUTPUT_FILE_NAME)

    print('Saving str datasets...')
    with open(save_file_path, 'w') as f:
        f.write(datasets_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, required=True)
    args = parser.parse_args()

    preprocess(args.config_path)
