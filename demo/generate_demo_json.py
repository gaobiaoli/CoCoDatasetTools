import os
import json
import random
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a Random Coco Json Annotation File for Testing"
    )
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        default="./demo/dataset",
        help="COCO Annotation Json File",
    )
    parser.add_argument(
        "--filename",
        "-f",
        type=str,
        default="demo.json",
        help="COCO Annotation Json File",
    )
    parser.add_argument(
        "--num-image", "-ni", type=int, default=100, help="number of images"
    )
    parser.add_argument(
        "--num-category", "-nc", type=int, default=5, help="number ofcategories"
    )
    args = parser.parse_args()
    return args


def main(output_path="coco_annotations.json"):
    args = parse_args()
    # COCO categories
    categories = [
        {"id": i, "name": f"category_{i}", "supercategory": "object"}
        for i in range(1, args.num_category + 1)
    ]

    # COCO images and annotations
    images = []
    annotations = []
    image_id = 1
    annotation_id = 1

    for i in range(args.num_image):
        # Generate random image information
        image_info = {
            "id": image_id,
            "file_name": f"image_{image_id}.jpg",
            "width": 640,
            "height": 480,
            "license": 1,
            "flickr_url": "",
            "coco_url": "",
            "date_captured": "2023-01-01 00:00:00",
        }

        # Generate random annotations for the image
        num_objects = random.randint(1, 5)
        for j in range(num_objects):
            annotation = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": random.randint(1, args.num_category),
                "segmentation": [[]],  # Random segmentation data (empty for simplicity)
                "area": random.randint(100, 1000),
                "bbox": [
                    random.randint(0, 640),
                    random.randint(0, 480),
                    random.randint(10, 100),
                    random.randint(10, 100),
                ],
                "iscrowd": 0,
            }
            annotations.append(annotation)
            annotation_id += 1

        images.append(image_info)
        image_id += 1

    # COCO dataset dictionary
    coco_data = {
        "info": {},
        "licenses": [],
        "categories": categories,
        "images": images,
        "annotations": annotations,
    }

    # Save to JSON file
    output_path = os.path.join(args.path, args.filename)
    with open(output_path, "w") as json_file:
        json.dump(coco_data, json_file, indent=2)

    print(f"Generated COCO annotations: {output_path}")


if __name__ == "__main__":
    main()
