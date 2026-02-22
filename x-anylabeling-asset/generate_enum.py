import json
import re
import keyword
from pathlib import Path

COCO_JSON_PATH = r"./assets/coco_detection.json"
OUTPUT_PATH = r"./src/data/features.py"


def normalize_field_name(name: str) -> str:
    # 转小写
    name = name.lower()

    # 非字母数字替换成 _
    name = re.sub(r"[^0-9a-z]+", "_", name)

    # 合并多个 _
    name = re.sub(r"_+", "_", name)

    # 去掉首尾 _
    name = name.strip("_")

    if not name:
        name = "empty"

    # 如果是关键字
    if keyword.iskeyword(name):
        name += "_"

    # 如果数字开头
    if name[0].isdigit():
        name = "_" + name

    return name



def main():
    with open(COCO_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = data["categories"]

    lines = ["from enum import Enum\n\n", "class FeatureList(str, Enum):\n"]

    for cat in categories:
        raw_name = cat["name"]
        enum_name = normalize_field_name(raw_name)
        lines.append(f'    {enum_name} = "{raw_name}"\n')

    output_path = Path(OUTPUT_PATH)

    # ✅ 如果父目录不存在则创建
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text("".join(lines), encoding="utf-8")

    print("✅ features.py 已生成")


if __name__ == "__main__":
    main()
