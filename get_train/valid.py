import os

import ddddocr
from PIL import Image

ocr = ddddocr.DdddOcr(
    show_ad=False,
    import_onnx_path=r"..\dddd_trainer\projects\omis\models\omis_1.0_104_4500_2024-08-08-09-50-03.onnx",
    charsets_path=r"..\dddd_trainer\projects\omis\models\charsets.json",
)
imgs = os.listdir("./train")
count = 0
for img in imgs:
    image = Image.open(f"train/{img}")
    result = ocr.classification(image)
    if img.split("_")[0] != result:
        print(img, result)
        count += 1

print(count)
