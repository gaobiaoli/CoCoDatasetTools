import os
import warnings
import argparse
from pycocotools.coco import COCO
import json
from pprint import pprint


def parse_args():
    parser = argparse.ArgumentParser(description="Assert a COCO Annotation Json File")
    parser.add_argument("json", type=str, help="COCO Annotation Json File")
    parser.add_argument(
        "--cat-nms",
        "-cnms",
        type=str,
        default=".",
        help="category names needs to extract",
    )
    parser.add_argument(
        "--cat-ids",
        "-cids",
        action="store_true",
        help="category ids need to extract",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./demo/dataset",
        type=str,
        help="output json file path",
    )
    parser.add_argument(
        "--reset-id",
        "--reset",
        "-reset",
        action="store_true",
        help="split ratio for train, val and test",
    )
    args = parser.parse_args()
    return args


def getIdsMapping(ids):
    return {old_id: new_id + 1 for new_id, old_id in enumerate(ids)}


def main():
    json_file_path = r"D:\git\CoCoDatasetTools\demo\dataset\demo.json"
    output = r"D:\git\CoCoDatasetTools\demo\dataset\extract.json"
    reset = True
    catIds = [1]
    catNms = ["category_3"]
    coco = COCO(json_file_path)
    catIds = list(set(catIds).union(set(coco.getCatIds(catNms=catNms))))

    categories = coco.loadCats(ids=catIds)
    print("Extract Catetories:")
    pprint(categories)
    ann_ids = coco.getAnnIds(catIds=catIds)
    annotations = coco.loadAnns(ann_ids)
    image_ids = sorted(coco.getImgIds(catIds=catIds))
    images = coco.loadImgs(image_ids)
    if reset:
        cat_ids_mapping = getIdsMapping(catIds)
        img_ids_mapping = getIdsMapping(image_ids)
        ann_ids_mapping = getIdsMapping(ann_ids)
        for image in images:
            image["id"] = img_ids_mapping[image["id"]]
        for annotation in annotations:
            annotation["image_id"] = img_ids_mapping[annotation["image_id"]]
            annotation["id"] = ann_ids_mapping[annotation["id"]]
            annotation["category_id"] = cat_ids_mapping[annotation["category_id"]]
        for category in categories:
            category["id"] = cat_ids_mapping[category["id"]]

    new_json = {
        "info": coco.info(),
        "categories": categories,
        "images": images,
        "annotations": annotations,
    }

    with open(output, "w") as json_file:
        json.dump(new_json, json_file, indent=4)


# file_list = None
# if args.dirs is not None:
#     print("reading image folder")
#     file_list = []
#     for path in args.dirs:
#         file_list.extend(os.listdir(os.path.join(args.root, path)))
#     print(f"{len(file_list)} contained in folders")

# valid = True
# for img_id in coco.getImgIds():
#     img_info = coco.loadImgs(ids=img_id)

#     # TODO：Duplicate ID assert
#     # if len(img_info) > 1:
#     #     valid = False
#     #     warnings.warn(f"Duplicate ID in Image {img_id}")

#     # Check if each image file exists
#     if file_list is not None and img_info[0]["file_name"] not in file_list:
#         valid = False
#         warnings.warn(f"Missing File in Image {img_id}")

#     # Check if each image in 'images' has corresponding annotation
#     anns_info = coco.getAnnIds(imgIds=[img_id])
#     if len(anns_info) == 0:
#         valid = False
#         warnings.warn(f"Missing Annotations in Image {img_id}")

#     if args.stop and not valid:
#         raise AssertionError(f"Assert Error in Image {img_id}")

# if valid:
#     print(
#         "Assertions passed. All images in the COCO JSON file and corresponding files in the image folder are valid."
#     )


if __name__ == "__main__":
    main()
