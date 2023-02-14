import os
import cv2
import json
import shutil

os.makedirs('annotations', exist_ok=True)
# 存放数据的父路径
parent_path = '/home/gao/datasets/tt100k_2021'

# 读TT100K原始数据集标注文件
with open(os.path.join(parent_path, 'annotations_all.json')) as origin_json:
    origin_dict = json.load(origin_json)
    classes = origin_dict['types']
# 建立统计每个类别包含的图片的字典
sta = {}
for i in classes:
    sta[i] = []

images_dic = origin_dict['imgs']

# 记录所有保留的图片
saved_images = []
# 遍历TT100K的imgs
for image_id in images_dic:
    image_element = images_dic[image_id]
    image_path = image_element['path']

    # 添加图像的信息到dataset中
    image_path = image_path.split('/')[-1]
    obj_list = image_element['objects']

    # 遍历每张图片的标注信息
    for anno_dic in obj_list:
        label_key = anno_dic['category']
        # 防止一个图片多次加入一个标签类别
        if image_path not in sta[label_key]:
            sta[label_key].append(image_path)

# 只保留包含图片数超过100的类别
result = {k: v for k, v in sta.items() if len(v) >= 100}

for i in result:
    print("the type of {} includes {} images".format(i, len(result[i])))
    saved_images.extend(result[i])

saved_images = list(set(saved_images))
print("total types is {}".format(len(result)))

type_list = list(result.keys())
result = {"type": type_list, "details": result, "images": saved_images}
print(type_list)
# 保存结果
json_name = os.path.join(parent_path, 'annotations/statistics.json')
with open(json_name, 'w', encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

os.makedirs('dataset/annotations', exist_ok=True)
# 存放数据的父路径
parent_path = '/home/gao/datasets/tt100k_2021'

# 读TT100K原始数据集标注文件
with open(os.path.join(parent_path, 'annotations_all.json')) as origin_json:
    origin_dict = json.load(origin_json)

with open(os.path.join(parent_path, 'annotations/statistics.json')) as select_json:
    select_dict = json.load(select_json)
    classes = select_dict['type']

train_dataset = {
    'info': {
    }, 'licenses': [], 'categories': [], 'images': [], 'annotations': []}
val_dataset = {
    'info': {
    }, 'licenses': [], 'categories': [], 'images': [], 'annotations': []}
test_dataset = {
    'info': {
    }, 'licenses': [], 'categories': [], 'images': [], 'annotations': []}
label = {
}  # 记录每个标志类别的id
count = {
}  # 记录每个类别的图片数
owntype_sum = {
}

info = {

    "year": 2021,  # 年份
    "version": '1.0',  # 版本
    "description": "TT100k_to_coco",  # 数据集描述
    "contributor": "Tecent&Tsinghua",  # 提供者
    "url": 'https://cg.cs.tsinghua.edu.cn/traffic-sign/',  # 下载地址
    "date_created": 2021 - 1 - 15
}
licenses = {

    "id": 1,
    "name": "null",
    "url": "null",
}

train_dataset['info'] = info
val_dataset['info'] = info
test_dataset['info'] = info
train_dataset['licenses'] = licenses
val_dataset['licenses'] = licenses
test_dataset['licenses'] = licenses

# 建立类别和id的关系
for i, cls in enumerate(classes):
    train_dataset['categories'].append({
        'id': i, 'name': cls, 'supercategory': 'traffic_sign'})
    val_dataset['categories'].append({
        'id': i, 'name': cls, 'supercategory': 'traffic_sign'})
    test_dataset['categories'].append({
        'id': i, 'name': cls, 'supercategory': 'traffic_sign'})
    label[cls] = i
    count[cls] = 0
    owntype_sum[cls] = 0

images_dic = origin_dict['imgs']

obj_id = 1

# 计算出每个类别共‘包含’的图片数
for image_id in images_dic:

    image_element = images_dic[image_id]
    image_path = image_element['path']
    image_name = image_path.split('/')[-1]
    # 在所选的类别图片中
    if image_name not in select_dict['images']:
        continue

    # 处理TT100K中的标注信息
    obj_list = image_element['objects']
    # 记录图片中包含最多的实例所属的type
    includes_type = {
    }
    for anno_dic in obj_list:
        if anno_dic["category"] not in select_dict["type"]:
            continue
        # print(anno_dic["category"])
        if anno_dic["category"] in includes_type:
            includes_type[anno_dic["category"]] += 1
        else:
            includes_type[anno_dic["category"]] = 1
    # print(includes_type)
    own_type = max(includes_type, key=includes_type.get)
    owntype_sum[own_type] += 1

# TT100K的annotation转换成coco的
for image_id in images_dic:

    image_element = images_dic[image_id]
    image_path = image_element['path']
    image_name = image_path.split('/')[-1]
    # 在所选的类别图片中
    if image_name not in select_dict['images']:
        continue
    print("dealing with {} image".format(image_path))
    # shutil.copy(os.path.join(parent_path,image_path),os.path.join(parent_path,"dataset/JPEGImages"))

    # 处理TT100K中的标注信息
    obj_list = image_element['objects']
    # 记录图片中包含最多的实例所属的type
    includes_type = {
    }
    for anno_dic in obj_list:
        if anno_dic["category"] not in select_dict["type"]:
            continue
        # print(anno_dic["category"])
        if anno_dic["category"] in includes_type:
            includes_type[anno_dic["category"]] += 1
        else:
            includes_type[anno_dic["category"]] = 1
    # print(includes_type)
    own_type = max(includes_type, key=includes_type.get)
    count[own_type] += 1
    num_rate = count[own_type] / owntype_sum[own_type]

    # 切换dataset的引用对象，从而划分数据集
    if num_rate < 0.7:
        dataset = train_dataset
    elif num_rate < 0.9:
        dataset = val_dataset
    else:
        print("dataset=test_dataset")
        dataset = test_dataset

    for anno_dic in obj_list:
        if anno_dic["category"] not in select_dict["type"]:
            continue
        x = anno_dic['bbox']['xmin']
        y = anno_dic['bbox']['ymin']
        width = anno_dic['bbox']['xmax'] - anno_dic['bbox']['xmin']
        height = anno_dic['bbox']['ymax'] - anno_dic['bbox']['ymin']
        label_key = anno_dic['category']

        dataset['annotations'].append({

            'area': width * height,
            'bbox': [x, y, width, height],
            'category_id': label[label_key],
            'id': obj_id,
            'image_id': int(image_id),
            'iscrowd': 0,
            # mask, 矩形是从左上角点按顺时针的四个顶点
            'segmentation': [[x, y, x + width, y, x + width, y + height, x, y + height]]
        })
        # 每个标注的对象id唯一
        obj_id += 1

    # 用opencv读取图片，得到图像的宽和高
    im = cv2.imread(image_path)
    H, W, _ = im.shape
    # 添加图像的信息到dataset中
    dataset['images'].append({
        'file_name': image_name,
        'id': int(image_id),
        'width': W,
        'height': H})

# 保存结果
for phase in ['train', 'val', 'test']:
    json_name = os.path.join(parent_path, 'dataset/annotations/{}.json'.format(phase))
    with open(json_name, 'w', encoding="utf-8") as f:
        if phase == 'train':
            json.dump(train_dataset, f, ensure_ascii=False, indent=1)
        if phase == 'val':
            json.dump(val_dataset, f, ensure_ascii=False, indent=1)
        if phase == 'test':
            json.dump(test_dataset, f, ensure_ascii=False, indent=1)

