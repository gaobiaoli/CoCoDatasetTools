import argparse
from pycocotools.coco import COCO
import json
from pprint import pprint

"""
    Example:
    cd $ProjectRoot
    python .\tools\mergeCat.py .\demo\dataset\demo.json --output .\demo\dataset\ex1.json -cids 1 2 -m 1
"""


def parse_args():
    parser = argparse.ArgumentParser(description="Assert a COCO Annotation Json File")
    parser.add_argument("json", type=str, help="COCO Annotation Json File")
    parser.add_argument(
        "--cat-ids",
        "-cids",
        nargs="+",
        type=int,
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
        "--mergeId",
        "-m",
        type=int,
        help="merge categories to this id",
    )
    args = parser.parse_args()
    return args


def getIdsMapping(ids,mergeId=None):
    mapping={old_id: new_id + 1 for new_id, old_id in enumerate(ids)}
    if mergeId is not None:
        for key in mapping.keys():
            if key!=mergeId:
                mapping[key]=mapping[mergeId]
    return mapping


def main():
    args = parse_args()
    json_file_path = args.json
    output = args.output
    catIds = args.cat_ids
    mergeId=args.mergeId

    coco = COCO(json_file_path)
    catIds = list(set(catIds))

    categories = coco.loadCats(ids=catIds)
    print("Extracted Catetories:")
    pprint(categories)
    ann_ids = coco.getAnnIds(catIds=catIds)
    annotations = coco.loadAnns(ann_ids)
    image_ids = [coco.catToImgs[cat_id] for cat_id in catIds]
    image_ids = sorted(set([id for imageIds in image_ids for id in imageIds]))
    images = coco.loadImgs(image_ids)
    print(f"Extracted Images' Number: {len(images)}")
    print(f"Extracted Annotations' Number: {len(annotations)}")

    cat_ids_mapping = getIdsMapping(catIds,mergeId=mergeId)
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
        "info": coco.dataset['info'] if "info" in coco.dataset.keys() else "",
        "categories": categories,
        "images": images,
        "annotations": annotations,
    }

    with open(output, "w") as json_file:
        json.dump(new_json, json_file, indent=4)


if __name__ == "__main__":
    main()
