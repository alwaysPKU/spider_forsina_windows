# 通过微博名单得到明星列表
import urllib.request

# 通过处理
def get_mingxingurl_dict(path):
    mark = 'https://baike.baidu.com/item/'
    mingxing_list=[]
    url_dic={}
    with open(path, encoding='UTF-8') as f:
        line = f.readline()
        while line:
            item = line.split()
            if len(item)==3 and item[2]=='明星':
                if item[1][0:2]=='演员':
                    mingxing_list.append(item[1].lstrip('演员'))
                elif item[1][0:3]=='小演员':
                    mingxing_list.append(item[1].lstrip('小演员'))
                elif item[1][0:4]=='泰国演员':
                    mingxing_list.append(item[1].lstrip('泰国演员'))
                elif item[1][0:4]=='配音演员':
                    mingxing_list.append(item[1].lstrip('配音演员'))
                else:
                    mingxing_list.append(item[1])
            line=f.readline()
    for i in mingxing_list:
        tmp = mark+urllib.request.quote(i)
        url_dic[i]=tmp
    return url_dic

def getmingxingurl_test():
    minxinglist=['倪妮','堺雅人', '龚蓓苾','黄志忠','易烊千玺','angelababy']
    mark = 'https://baike.baidu.com/item/'
    url_dic={}

    for i in minxinglist:
        tmp = mark+urllib.request.quote(i)
        url_dic[i]=tmp
    return url_dic

def get_yinyueurl_dict(path):
    mark = 'https://baike.baidu.com/item/'
    yinyue_list = []
    url_dic = {}
    with open(path, encoding='UTF-8') as f:
        line = f.readline()
        while line:
            item = line.split()
            if len(item) == 3 and item[2] == '音乐':
                yinyue_list.append(item[1])
            line = f.readline()
    for i in yinyue_list:
        tmp = mark + urllib.request.quote(i)
        url_dic[i] = tmp
    return url_dic