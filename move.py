import shutil
import os
import os.path


def move_file(txt_path, old_path, new_path):
    # print(old_path)
    # print(new_path)
    filelist = os.listdir(txt_path)  # 列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    # print(filelist)
    dic = []
    for file in filelist:
        head, tail = os.path.splitext(file)
        jpg_name = head + ".jpg"  # 对应的txt名字，与jpg一致
        src = os.path.join(old_path, jpg_name)
        dst = os.path.join(new_path, jpg_name)
        if os.path.isfile(src):
            # print('src:', src)
            # print('dst:', dst)
            shutil.move(src, dst)
        else:
            dic.append(src)
    print(dic)



def read_name(old_path='./images/val2017', new_path='./val2017.txt'):
    txt_name = open(new_path, 'w')
    filenames = os.listdir(old_path)
    # dic = []
    for filename in filenames:
        filename_p = os.path.join(old_path, filename)
        txt_name.write(filename_p + '\n')
    txt_name.close()

    # for parent, dirname, filenames in os.walk(src):  # 返回的三个参数分别为，父目录，所有文件夹名，所有文件名。
    #     print('parent is:', parent)
    #     print('dirname is:', dirname)


if __name__ == '__main__':
    # move_file(r"/home/gao/datasets/tt100k_2021/labels/val", r"/home/gao/datasets/tt100k_2021/all",
    #           r"/home/gao/datasets/tt100k_2021/images/val")
    read_name()
