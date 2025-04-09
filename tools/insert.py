import argparse
from pycocotools.coco import COCO
import json

"""
    Example:
    cd $ProjectRoot
    python .\tools\insert.py .\demo.json .\demo1.json --output .\demo2.json
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Merge additional annotations into a COCO Annotation Json File")
    parser.add_argument("json1", type=str, help="Base COCO Annotation Json File")
    parser.add_argument("json2", type=str, help="Additional COCO Annotation Json File")
    parser.add_argument(
        "--output",
        "-o",
        default="./merged.json",
        type=str,
        help="Output json file path",
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    json1_file_path = args.json1
    json2_file_path = args.json2
    output = args.output
    
    # Load COCO datasets
    coco1 = COCO(json1_file_path)
    coco2 = COCO(json2_file_path)
    
    # Build filename to image ID mapping
    file_to_img1 = {img['file_name']: img for img in coco1.dataset['images']}
    file_to_img2 = {img['file_name']: img for img in coco2.dataset['images']}
    
    # Find common images using filenames
    common_filenames = set(file_to_img1.keys()).intersection(set(file_to_img2.keys()))
    
    # Get category ID mapping
    cat_ids1 = set(coco1.getCatIds())
    cat_ids2 = set(coco2.getCatIds())
    new_cats = [cat for cat in coco2.loadCats(list(cat_ids2 - cat_ids1))]
    
    # Update categories
    categories = coco1.dataset['categories'] + new_cats
    cat_id_map = {cat['id']: cat['id'] for cat in coco1.dataset['categories']}
    for new_cat in new_cats:
        new_cat_id = max(cat_id_map.values(), default=0) + 1
        cat_id_map[new_cat['id']] = new_cat_id
        new_cat['id'] = new_cat_id
    
    # Get max annotation ID
    max_ann_id = max([ann['id'] for ann in coco1.dataset['annotations']], default=0)
    
    # Merge annotations for common images using filenames
    new_annotations = []
    for ann in coco2.dataset['annotations']:
        img_filename = file_to_img2[ann['image_id']]['file_name']
        if img_filename in common_filenames and ann['category_id'] in cat_id_map:
            max_ann_id += 1
            new_ann = ann.copy()
            new_ann['id'] = max_ann_id
            new_ann['category_id'] = cat_id_map[ann['category_id']]
            new_ann['image_id'] = file_to_img1[img_filename]['id']
            new_annotations.append(new_ann)
    
    # Update dataset
    coco1.dataset['categories'] = categories
    coco1.dataset['annotations'].extend(new_annotations)
    
    # Save merged dataset
    with open(output, 'w') as f:
        json.dump(coco1.dataset, f, indent=4)
    
    print(f"Merged annotations saved to {output}")
    
if __name__ == "__main__":
    main()
