import os
import json
import argparse
from pycocotools.coco import COCO
from sklearn.model_selection import train_test_split


def parse_args():
    parser = argparse.ArgumentParser(
        description="Split a COCO Annotation Json File to Train, Val and Test"
    )
    parser.add_argument("json", type=str, help="COCO Annotation Json File")
    parser.add_argument(
        "--output",
        "-o",
        default="./demo/dataset",
        type=str,
        help="output json file path",
    )
    parser.add_argument(
        "--ratio",
        "-r",
        type=float,
        nargs="+",
        default=[0.8, 0.1, 0.1],
        help="split ratio for train, val and test",
    )
    parser.add_argument(
        "--reset-id",
        "--reset",
        "-reset",
        action="store_true",
        help="split ratio for train, val and test",
    )
    args = parser.parse_args()

    if len(args.ratio) != 3 and len(args.ratio) != 2:
        parser.error("The number of ratio values must be 3 or 2.")

    ratio_sum = sum(args.ratio)
    if ratio_sum > 1:
        parser.error("The sum of ratio values must be less than 1.")

    if len(args.ratio) == 2:
        args.ratio.append(1 - ratio_sum)

    return args


def main():
    args = parse_args()

    train_ratio, val_ratio, test_ratio = args.ratio

    # Load the COCO annotations
    coco = COCO(args.json)

    # Get image ids
    image_ids = list(coco.imgs.keys())

    # Split the dataset into train, val, and test sets
    train_ids, test_val_ids = train_test_split(
        image_ids, test_size=(val_ratio + test_ratio), random_state=42
    )
    val_ids, test_ids = train_test_split(
        test_val_ids, test_size=(test_ratio / (val_ratio + test_ratio)), random_state=42
    )

    # Create output directories
    os.makedirs(args.output, exist_ok=True)

    # Save the annotations for each split
    for split, ids in zip(["train", "val", "test"], [train_ids, val_ids, test_ids]):
        ids = sorted(ids)
        output_json = f"{split}_annotations.json"
        split_json = {
            "images": [],
            "annotations": [],
            "categories": [coco.dataset["categories"]],
        }
        for new_id, image_id in enumerate(ids):
            img_info = coco.loadImgs(image_id)[0]
            annotations = coco.loadAnns(coco.getAnnIds(imgIds=image_id))

            # Save the annotations
            for annotation in annotations:
                new_annotation = annotation.copy()
                if args.reset_id:
                    new_annotation["image_id"] = new_id  # Reset image_id
                split_json["annotations"].append(new_annotation)
            # Save the image
            new_img_info = img_info.copy()
            if args.reset_id:
                new_img_info["id"] = new_id
            split_json["images"].append(new_img_info)

        with open(os.path.join(args.output, output_json), "w") as outfile:
            json.dump(split_json, outfile, indent=4)
        print(f"{os.path.join(args.output, output_json)} Saved")


if __name__ == "__main__":
    main()
