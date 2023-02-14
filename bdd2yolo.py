import json
import os


# 第42行改为 filepath = os.path.join(readpath, file)
# 第10行改为 write = open(writepath + os.sep + "%s.txt" % info["name"], 'w')
def bdd2yolo5(categorys,jsonFile,writepath):
    strs=""
    f = open(jsonFile)
    info = json.load(f)
    #print(len(info))
    #print(info["name"])
    write = open(writepath + "%s.txt" % info["name"], 'w')
    for obj in info["frames"]:
        #print(obj["objects"])
        for objects in obj["objects"]:
            #print(objects)
            if objects["category"] in categorys:
                dw = 1.0 / 1280
                dh = 1.0 / 720
                strs += str(categorys.index(objects["category"]))
                strs += " "
                strs += str(((objects["box2d"]["x1"] + objects["box2d"]["x2"]) / 2.0) * dw)[0:8]
                strs += " "
                strs += str(((objects["box2d"]["y1"] + objects["box2d"]["y2"]) / 2.0) * dh)[0:8]
                strs += " "
                strs += str(((objects["box2d"]["x2"] - objects["box2d"]["x1"])) * dw)[0:8]
                strs += " "
                strs += str(((objects["box2d"]["y2"] - objects["box2d"]["y1"])) * dh)[0:8]
                strs += "\n"
        write.writelines(strs)
        write.close()
        print("%s has been dealt!" % info["name"])

if __name__ == "__main__":
    ####################args#####################
    categorys = ["person", "rider", "car", "bus", "truck", "bike", "motor"]    # 自己需要从BDD数据集里提取的目标类别
    readpath = "/home/gao/Net/Datasets/bdd100k/det_annotations/val/"   # BDD数据集标签读取路径，这里需要分两次手动去修改train、val的地址
    writepath = "/home/gao/Net/Datasets/bdd100k/labels/val/"	# BDD数据集转换后的标签保存路径

    fileList = os.listdir(readpath)
    #print(fileList)
    for file in fileList:
        print(file)
        filepath = readpath + file
        bdd2yolo5(categorys,filepath,writepath)