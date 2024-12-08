import ddddocr
from PIL import Image

ocr = ddddocr.DdddOcr(
    show_ad=False,
    import_onnx_path=r"dddd_trainer\projects\math\models\math_1.0_27_5000_2024-08-06-21-41-48.onnx",
    charsets_path=r"dddd_trainer\projects\math\models\charsets.json",
)

image = Image.open("valid/2.png")

result = ocr.classification(image)
print(result)
