import bs4
import os
import load_url as lurl



tmp = "https://baike.baidu.com"

#从下载好的html解析movie的url列表
def get_movieurl(html):
    url = []
    with open(html) as f:
        soup = bs4.BeautifulSoup(f, 'html.parser')
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

# 从star的url借些出movie的url列表
def get_movieurl_fromurl(star_url):
    url = []
    data = lurl.load(star_url)
    if data == None:
        print('timeout:'+star_url)
        return None
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

# 第一版解析电影的url，发现没有解析完整，例如易烊千玺那样的...因为这种没有title里主要演员介绍
def analysis_movieurl(url):
    relation = set()

    data = lurl.load(url)

    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tags1 = soup1.find_all('a', attrs={'class': 'actor-name '})
    if (len(tags1) == 0):
        tags2 = soup1.find_all('p', attrs={'class': 'actorName'})
        if (len(tags2) == 0):
            return None
        for tag2 in tags2:
            relation_star = tag2.text.strip()
            # if relation_star == real_name:
            #     continue
            # else:
            relation.add(relation_star)
    else:
        for tag1 in tags1:
            relation_star = tag1.text.strip()
            # if relation_star == real_name:
            #     continue
            # else:
            relation.add(relation_star)

    return relation

# 第二版解析，试试是不是可以增量。从基本信息的列表里解析
def analysis_movieurl2(url):
    relation = set()
    data = lurl.load(url)
    if data == None:
        print('timeout:'+url)

        return None
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

# 从下载好的html文件借些showurl列表
def get_showurl(html):
    res = []
    with open(html) as f:
        soup1 = bs4.BeautifulSoup(f, 'html.parser')
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
            # n = n + 1
            # print(n)
            # print(star_name)
            # data = lurl.load(show_url)
            # st.write_html(star_name.replace('/',' ')+'-'+show_name.replace('/',' '),data)
            # list = ansis.show_html_analysis(data)
            # if list != None:
            #     for name in list:
            #         realation_set.add(name)
            # else:
            #     continue
    # print(res)
    # print(res)
    return res

# 从start_url解析showurl列表
def get_showurl_fromurl(star_url):
    res = []
    data = lurl.load(star_url)
    if data == None:
        print('timeout:'+star_url)
        return None
    soup1 = bs4.BeautifulSoup(f, 'html.parser')
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
        # n = n + 1
        # print(n)
        # print(star_name)
        # data = lurl.load(show_url)
        # st.write_html(star_name.replace('/',' ')+'-'+show_name.replace('/',' '),data)
        # list = ansis.show_html_analysis(data)
        # if list != None:
        #     for name in list:
        #         realation_set.add(name)
        # else:
        #     continue
    # print(res)
    # print(res)
    return res

def analysis_showurl(url):
    data = lurl.load(url)
    if data == None:
        print('timeout:'+url)
        return None
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
        if tag2.text.strip('\n') != '主持人' and num==len(tags2)-2:
            num=-1
        else:
            if tag2.text.strip('\n') == '主持人':
                num=num+1
                break
            else:
                num=num+1
        # print(num)
    # print(num)
    if num != -1:
        zhuchiren = tags3[num]
        # print(zhuchiren)
    else:
        return None
    list = zhuchiren.text.strip('\n').split('、')
    # print(list)
    relation=set(list)
    return relation

# 稍微修改
def analysis_showurl2(url):
    data = lurl.load(url)
    if data == None:
        print('timeout:'+url)
        return None
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    # print(soup1)
    # tag1 = soup1.find('dl', attrs={'class': 'basicInfo-block basicInfo-left'})
    # 在这里修改了
    tag1 = soup1.find('div', attrs={'class': 'basic-info cmn-clearfix'})
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
        if tag2.text.strip('\n') != '主持人' and num==len(tags2)-2:
            num=-1
        else:
            if tag2.text.strip('\n') == '主持人':
                num=num+1
                break
            else:
                num=num+1
        # print(num)
    # print(num)
    if num != -1:
        zhuchiren = tags3[num]
        # print(zhuchiren)
    else:
        return None
    list = zhuchiren.text.strip('\n').split('、')
    # print(list)
    relation=set(list)
    return relation

# 这个是解析下载到文件夹里的html文件
def analysis_relation(html):
    res = []
    with open(html) as f:
        soup = bs4.BeautifulSoup(f, 'html.parser')
        # get_name = soup.find_all('dd', attrs={'class': 'lemmaWgt-lemmaTitle-title'})
        # if len(get_name) == 0:
        #     print(path1)
        #     m = m + 1
        #     continue
        # main_name = get_name[0].h1.text
        # print(main_name)

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

# 直接解析url
def analysis_relation2_fromurl(url):
    res = []
    data  = lurl.load(url)
    if data == None:
        print('timeout:'+url)
        return None
    soup = bs4.BeautifulSoup(data, 'html.parser')
    # get_name = soup.find_all('dd', attrs={'class': 'lemmaWgt-lemmaTitle-title'})
    # if len(get_name) == 0:
    #     print(path1)
    #     m = m + 1
    #     continue
    # main_name = get_name[0].h1.text
    # print(main_name)

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

