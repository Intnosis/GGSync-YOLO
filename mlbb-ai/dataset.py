from pathlib import Path
import random
import shutil

source_dir = Path("dataset/raw_frames")
dataset_dir = Path("dataset")

train_ratio = 0.70
valid_ratio = 0.20
test_ratio = 0.10

for split in ["train", "valid", "test"]:
    (dataset_dir / split / "images").mkdir(
        parents=True,
        exist_ok=True
    )

    (dataset_dir / split / "labels").mkdir(
        parents=True,
        exist_ok=True
    )

images = list(source_dir.glob("*.jpg"))

if not images:
    print("Error: No Images found")
    exit()

random.shuffle(images)

total = len(images)

train_end = int(total * train_ratio)
valid_end = train_end + int(total * valid_ratio)


train_images = images[:train_end]
valid_images = images[train_end:valid_end]
test_images = images[valid_end:]

def copy_images(images,split):
    for image in images:
        destination = (
            dataset_dir / split / "images" / image.name
        )

        shutil.copy2(image, destination)

copy_images(train_images, 'train')
copy_images(valid_images, 'valid')
copy_images(test_images, 'test')

yaml_content = f"""path: {dataset_dir.resolve().as_posix()}

train: train/images
val: valid/images
test: test/images

names:
    0: hero
"""

with open(dataset_dir / "data.yaml", "w") as file:
    file.write(yaml_content)

print("Dataset structure created")
print(f"Total images: {total}")
print(f"Total train: {len(train_images)}")
print(f"Total valid: {len(valid_images)}")
print(f"Total test: {len(test_images)}")
print("Created: dataset/data.yaml")