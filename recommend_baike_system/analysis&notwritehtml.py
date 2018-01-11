import bs4
import recommend_baike_system.load_url as lurl
from multiprocessing import Pool
# 这里输入都是load的data
tmp = "https://baike.baidu.com" #拼接前缀
def get_relations(data):
    """
    解析的到relation关系
    :param data:
    :return: list
    """
    # if data == None:
    #     print('timeout:'+url)
    #     return None
    res = []
    soup = bs4.BeautifulSoup(data, 'html.parser')
    tags = soup.find_all('ul', attrs={'class': 'slider maqueeCanvas'})
    for tag in tags:
        soup2 = bs4.BeautifulSoup(str(tag), 'html.parser')
        tag2 = soup2.find_all('div', attrs={'class': 'name'})
        if len(tag2) == 0:
            continue
        dict = {}
        for i in tag2:
            if not i.em:
                continue
            full = i.text
            name = i.em.text
            len1 = len(full)
            len2 = len(name)
            relations = full[0:len1 - len2]
            dict_tmp = {relations: name}
            res.append(dict_tmp)
    # print(relations)
    return res

def get_movieurl(data):
    """
    解析得到movie——url列表
    :param data:
    :return: list
    """
    url = []
    # if data == None:
    #     print('timeout:'+star_url)
    #     return None
    soup = bs4.BeautifulSoup(data, 'html.parser')
    # get_name = soup.find_all('dd', attrs={'class': 'lemmaWgt-lemmaTitle-title'})
    # if len(get_name) == 0:
    #     # print(path1)
    #     continue
    # main_name = get_name[0].h1.text
    # print(main_name)
    tags = soup.find_all('div', attrs={'class': 'star-info-block works'})
    # tags = soup.find_all('ul', attrs={'class':'slider maqueeCanvas'})

    for tag in tags:
        soup2 = bs4.BeautifulSoup(str(tag), 'html.parser')
        tag2 = soup2.find_all('ul', attrs={'class': 'slider maqueeCanvas'})
        if len(tag2) == 0:
            continue
        for i in tag2:
            soup3 = bs4.BeautifulSoup(str(i), 'html.parser')
            tag3 = soup3.find_all('a', attrs={'href': True})
            for j in tag3:
                name = j.text.strip('\n')
                # print(name)
                item = j['href']
                # print(item)
                if item[0] != '/':
                    movie_url = item
                else:
                    movie_url = tmp + item
                # print(movie_url)
                url.append(movie_url)
                # 下载电影html
                # if name == '' or name == None:
                #     continue
                # else:
                #     data = test.load(movie_url)
                #     test.write_html(main_name.replace('/', ' ') + '-' + name.replace('/', ' '), data)
                #     n = n + 1
                #     print(n)
    # print(url)
    return url

def get_showurl(data):
    """
    解析明星html得到show——url列表
    :param data: 明星的html数据
    :return: list
    """
    res = []
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tags1 = soup1.find_all('table', attrs={'class': 'cell-module'})
    if (len(tags1) == 0):
        return None
    tags1 = tags1[0]
    soup2 = bs4.BeautifulSoup(str(tags1), 'html.parser')
    tags2 = soup2.find_all('a', attrs={'href': True})
    if (len(tags2) == 0):
        return None
    for tag2 in tags2:
        # 每个循环一个url（一个show记录），解析并添加到relation_set
        show_name = tag2.text.strip('\n')
        url = tag2['href']
        if url[0] == '/':
            show_url = tmp + url
        elif url[1] == 'h':
            show_url = url
        else:
            continue
        res.append(show_url)
    return res


# get_movie
def analysis_movieurl(url,movie_path, file_name):
    """
    接卸movie——url并且写html文件
    :param url: movie的url
    :param movie_path: 写html的路径
    :param file_name: html的文件名
    :return: set
    """
    relation = set()
    data = lurl.load(url)
    if data == None:
        print('timeout:'+url)
        with open('log','a',encoding='utf-8') as f:
            f.write('movie_url load 失败：' + str(file_name) + '>----->' + url + '\n')
        return None
    # lurl.write_html(file_name, data, movie_path)
    # p.apply_async(lurl.write_html, args = (file_name,data,movie_path))
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tag1 = soup1.find('div',attrs={'class':'basic-info cmn-clearfix'})
    num=-1
    if not tag1:
        return None
    # else:
    soup2 = bs4.BeautifulSoup(str(tag1), 'html.parser')
    tags2 = soup2.find_all('dt',attrs={'class':'basicInfo-item name'})
    tags3 = soup2.find_all('dd',attrs={'class':'basicInfo-item value'})

    for tag2 in tags2:
        # print(tag2.text.strip('\n'))
        if tag2.text != '主    演' and num==len(tags2)-2:
            num=-1
        else:
            if tag2.text == '主    演':
                # print('here')
                num=num+1
                break
            else:
                num=num+1
    # print(num)
    if num!=-1:
        zhuyan = tags3[num]
    else:
        return None
    list = zhuyan.text.strip('\n').split('，')
    relation=set(list)
    return relation

# get_show
def analysis_showurl(url, show_path, file_name):
    """
    解析showurl并写html
    :param url: 要解析的url
    :param show_path: 写html的路径
    :param file_name: 写html的文件名
    :return: set
    """
    # p = Pool(1)
    data = lurl.load(url)
    if data == None:
        print('timeout:'+url)
        with open('log','a',encoding='utf-8') as f:
            f.write('show_url load 失败：' + str(file_name) + '>----->' + url + '\n')
        return None
    # lurl.write_html(file_name, data, show_path)
    # p.apply_async(lurl.write_html,args=(file_name,data,show_path))
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    # print(soup1)
    tag1 = soup1.find('dl', attrs={'class': 'basicInfo-block basicInfo-left'})
    # tag1 = soup1.find('div', attrs={'class': 'basic-info cmn-clearfix'})
    if not tag1:
        return None
    relation = set()
    num = -1
    soup2 = bs4.BeautifulSoup(str(tag1), 'html.parser')
    tags2 = soup2.find_all('dt', attrs={'class': True})
    # print(tags2)
    tags3 = soup2.find_all('dd', attrs={'class': True})
    # print(tags3)
    for tag2 in tags2:
        if tag2.text.strip('\n') != '主持人' and num == len(tags2) - 2:
            num = -1
        else:
            if tag2.text.strip('\n') == '主持人':
                num = num + 1
                break
            else:
                num = num + 1
                # print(num)
    # print(num)
    if num != -1:
        zhuchiren = tags3[num]
        # print(zhuchiren)
    else:
        return None
    list = zhuchiren.text.strip('\n').split('、')
    # print(list)
    relation = set(list)
    return relation