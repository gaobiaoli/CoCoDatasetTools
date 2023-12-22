import os
import warnings
import argparse
from pycocotools.coco import COCO

def parse_args():
    parser = argparse.ArgumentParser(description="Assert a COCO Annotation Json File\n 1.")
    parser.add_argument("json", type=str, help="COCO Annotation Json File")
    parser.add_argument("--dirs", "-d", type=str, nargs="*", help="Image File Folder")
    parser.add_argument("--root", "-r", default=".", type=str, help="Dataset Root")
    parser.add_argument("--stop", "-s", action="store_true", help="Assert Mode")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    coco = COCO(os.path.join(args.root, args.json))

    file_list = None
    if args.dirs is not None:
        print("reading image folder")
        file_list = []
        for path in args.dirs:
            file_list.extend(os.listdir(os.path.join(args.root, path)))
        print(f"{len(file_list)} contained in folders")

    valid = True
    for img_id in coco.getImgIds():
        img_info = coco.loadImgs(ids=img_id)

        # TODO：Duplicate ID assert
        # if len(img_info) > 1:
        #     valid = False
        #     warnings.warn(f"Duplicate ID in Image {img_id}")

        # Check if each image file exists
        if file_list is not None and img_info[0]["file_name"] not in file_list:
            valid = False
            warnings.warn(f"Missing File in Image {img_id}")
        
        # Check if each image in 'images' has corresponding annotation
        anns_info = coco.getAnnIds(imgIds=[img_id])
        if len(anns_info) == 0:
            valid = False
            warnings.warn(f"Missing Annotations in Image {img_id}")

        if args.stop and not valid:
            raise AssertionError(f"Assert Error in Image {img_id}")

    if valid:
        print(
            "Assertions passed. All images in the COCO JSON file and corresponding files in the image folder are valid."
        )

if __name__ == "__main__":
    main()
    
