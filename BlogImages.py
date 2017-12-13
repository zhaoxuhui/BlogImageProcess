# coding=utf-8
import cv2
import os.path
import datetime
import tinify


# 脚本功能
# 1.批量读取、改名
# 2.批量修改大小
# 3.批量压缩
# 4.自动插入标签

# 读取目录下所有图片的路径，返回一个list
def findAllImages(root_dir):
    paths = []
    # 遍历
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG"):
                paths.append(parent + "\\" + filename)
    print "All images loaded."
    return paths


# 获取当前系统的日期
def getDateString():
    return datetime.datetime.now().strftime('%Y-%m-%d')


# 基于读取的图片路径和当前日期，拼接组成新的符合格式的文件名
def generateFormatName(paths, start_index):
    new_names = []
    root = paths[0][0: paths[0].rfind("\\")] + "\\"
    for i in range(len(paths)):
        new_name = root + getDateString() + "-" + '{:0>2}'.format(i + 1 + start_index) + "." + paths[i].split(".")[1]
        new_names.append(new_name)
    return new_names


# 批量将文件重命名
def renameImages(ori, new):
    for i in range(len(new)):
        os.rename(ori[i], new[i])
    print "All images are renamed."


# 修改图片大小
def resizeImage(img):
    width = img.shape[1]
    new_width = 0
    if width > 650:
        new_width = 650
    elif 650 > width >= 625:
        new_width = 625
    elif 625 > width >= 600:
        new_width = 600
    elif 600 > width >= 575:
        new_width = 575
    elif 575 > width >= 550:
        new_width = 550
    elif 550 > width >= 525:
        new_width = 525
    elif 525 > width >= 500:
        new_width = 500
    elif 500 > width >= 475:
        new_width = 475
    elif 475 > width >= 450:
        new_width = 450
    elif 450 > width >= 425:
        new_width = 425
    elif 425 > width >= 400:
        new_width = 400
    elif 400 > width >= 375:
        new_width = 375
    elif 375 > width >= 350:
        new_width = 350
    elif 350 > width > 325:
        new_width = 325
    elif 325 > width > 300:
        new_width = 300
    elif 300 > width >= 275:
        new_width = 275
    elif 275 > width >= 250:
        new_width = 250
    elif 250 > width >= 225:
        new_width = 225
    elif 225 > width >= 200:
        new_width = 200
    elif 200 > width >= 175:
        new_width = 175
    elif 175 > width >= 150:
        new_width = 150
    elif 150 > width >= 125:
        new_width = 125
    elif 125 > width >= 100:
        new_width = 100
    elif 100 > width >= 75:
        new_width = 75
    elif 75 > width >= 50:
        new_width = 50
    elif 50 > width >= 0:
        new_width = 50

    ratio = new_width * 1.0 / width
    if ratio == 0:
        ratio = 1

    res = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)
    return res


# 批量修改图片大小并输出覆盖原图
def saveImages(new):
    for item in new:
        img = cv2.imread(item)
        img2 = resizeImage(img)
        cv2.imwrite(item, img2)
    print "All images are resized."


# 调用TinyPNG接口进行图像压缩，并替换原图
def tinifyImage(image_paths):
    for i in range(len(image_paths)):
        source = tinify.from_file(image_paths[i])
        source.to_file(image_paths[i])
        print "Compress", format((i * 1.0 / len(image_paths)) * 100, '0.2f'), "% finished.", image_paths[i]
    print "Compress 100% finished."


# 根据文件路径生成img标签
def generateHTML(html1, html2, html3, new_paths, root):
    f = open(root + "\\img_tag.txt", "w")
    for item in new_paths:
        f.write(html1 + item[item.rfind("\\") + 1:] + html2 + cv2.imread(item).shape[1].__str__() + html3 + "\n")
    f.close()
    print "HTML tag generated successfully."


# 根据"<-img"标签自动插入图片Tag
def insertImgTag(html1, html2, html3, new_paths, file_path):
    img_tags = []
    i = 0
    out = ""

    for item in new_paths:
        img_tags.append(
            html1 + item[item.rfind("\\") + 1:] + html2 + cv2.imread(item).shape[1].__str__() + html3 + "\n")

    f = open(file_path)
    lines = f.readlines()
    for line in lines:
        if line.__contains__("<-img"):
            line = img_tags[i]
            i += 1
        out += line
    f.close()
    f = open(file_path.split('.')[-2] + "_auto.md", "w")
    f.writelines(out)
    f.close()


# 你的TinyPNG密钥
tinify.key = "xxxxxxxxxxxxxxxxx"

# HTML img标签
html_part1 = "<img src = \"http://zhaoxuhui.top/assets/images/blog/content/"
html_part2 = "\" width = \""
html_part3 = "\">"

# 用户指定图片所在目录
root_dir = raw_input("Input the parent path of images:\n")

# 第一步，获取目录下所有图片路径
ori = findAllImages(root_dir)

# 第二步，根据规则创建新的文件名
start = raw_input("Input the start index of images:\n")
new = generateFormatName(ori, int(start))

# 第三步，文件批量改名
renameImages(ori, new)

flag1 = raw_input("Resize all images?y/n\n")
if flag1 == "y":
    # 第四步，批量修改文件大小并替换原图
    saveImages(new)

flag2 = raw_input("Tinify all images?y/n\n")
if flag2 == "y":
    # 第五步，调用TinyPNG接口进行图像压缩，并替换原图
    tinifyImage(new)

flag3 = raw_input("Auto insert tags into files?y/n\n")
if flag3 == "y":
    # 第六步，生成每个文件对应的img标签并自动插入
    # 注意文件名不支持中文
    file_path = raw_input("Input the file path:\n")
    insertImgTag(html_part1, html_part2, html_part3, new, file_path)
else:
    # 第六步，生成每个文件对应的img标签
    generateHTML(html_part1, html_part2, html_part3, new, root_dir)
