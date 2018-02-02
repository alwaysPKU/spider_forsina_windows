import load_url as lurl
import get_stardict as star
import analysis as analysis
import json as js
import mkdir as mk
import time
import name_topicid as name_topic
import add_re_relation as ad_re_relation
import count as count
from multiprocessing import Pool
"""
# 从名单直接拼接url爬取所需内容
# 直接输出对应name的推荐列表
每次运行需要修改两个文件名
1. txt文件名
2. 结果写出文件名
"""


# star_url = star.get_mingxingurl_dict(path)  # 明星
# star_url = star.get_yinyueurl_dict(path)  # 音乐
# star_url = star.getmingxingurl_test() # 测试用例
def get_movieset(movie_url, movie_path,star_name):
    movie_set = set()
    n = 0
    for url in movie_url:
        n = n + 1
        file_name = star_name + str("_") + str(n)
        tmpset = analysis.analysis_movieurl(url, movie_path, file_name)
        # print(tmpset)
        if tmpset != None and len(tmpset) != 0:
            movie_set = movie_set | tmpset
        else:
            continue
    return movie_set
def get_showset(show_url, show_path, star_name):
    show_set = set()
    n = 0
    for url in show_url:
        n = n + 1
        # print(url)
        file_name = star_name + str("_") + str(n)
        tmpset2 = analysis.analysis_showurl(url, show_path, file_name)
        # print(tmpset2)
        if tmpset2 != None and len(tmpset2) != 0:
            show_set = show_set | tmpset2
        else:
            continue
    return show_set

def recomend(star_url,star_path,movie_path,show_path,path_res):
    with open(path_res,'a', encoding='UTF-8') as f:

        for k,v in star_url.items():
            p1 = Pool(4)
            star_name = k    #明星名字
            print('======='+star_name+'=======')
            relation_list = [] # 解析的明星relation列表
            movie_url = [] # 解析明星的movieurl列表
            show_url = [] # 解析明星的showurl列表

            full = {} # each line {star_name:full_relation}
            full_relation=[] # 一条总记录
            movie_dic={} # 解析的movie推荐列表
            show_dic={} # 借些的show推荐列表

            # print(v)
            data = lurl.load(v)
            # lurl.write_html(star_name,data,star_path)
            p1.apply_async(lurl.write_html(star_name, data, star_path))
            if data == None:
                with open('log','a',encoding='utf-8') as f1:
                    f1.write('明星url_load失败:')
                    f1.write(k+':'+v+'\n')
                continue
            #解析结果：relation，movieurl，showurl
            # relation_list=analysis.get_relations(data)
            relation_list = p1.apply_async(analysis.get_relations,  args=(data, )).get()
            # movie_url=analysis.get_movieurl(data)
            movie_url = p1.apply_async(analysis.get_movieurl, args=(data, )).get()
            # show_url=analysis.get_showurl(data)
            show_url = p1.apply_async(analysis.get_showurl, args=(data, )).get()
            # print(show_url)
            p1.close()
            p1.join()
            # relation 结果存储 {relation:[name...}
            if len(relation_list)!=0:
                tmp_dict={}
                tmp_list=[]
                print('relation')
                for i in relation_list:
                    for j in i.keys():
                        tmp_list.append(i[j])
                tmp_dict['relation']=tmp_list
                full_relation.append(tmp_dict)
                print('relation_over')

            p2 = Pool(2)
            #load movieurl列表并解析
            if movie_url != None:
                print('movie')

                # 逐一借些movie的url
                movie_set = p2.apply_async(get_movieset,args=(movie_url, movie_path, star_name)).get()
                # 把该明星名字从列表中去除
                if movie_set != '' and star_name in movie_set:
                    movie_set.remove(star_name)
                movie_list=list(movie_set)
                movie_dic['movie']=movie_list
                if len(movie_dic['movie']) != 0 and movie_dic['movie'] != None:
                    full_relation.append(movie_dic)
                    print('movie_over')

            # load showurl列表并解析
            if show_url!= None:
                print('show')
                show_set = p2.apply_async(get_showset,args=(show_url, show_path, star_name)).get()
                # 20171228新加的还没尝试(过滤重复名字)
                if show_set != '' and star_name in show_set:
                    show_set.remove(star_name)
                show_list=list(show_set)
                # print(show_list)
                show_dic['show'] = show_list
                if len(show_dic['show']) != 0 and show_dic['show'] != None:
                    full_relation.append(show_dic)
                    print('show_over')
            p2.close()
            p2.join()
            if len(full_relation)!=0:
                full[star_name]=full_relation
                data = js.dumps(full, ensure_ascii=False)
                f.write(data+'\n')
            else:
                with open('Null_recommend_list','a', encoding='UTF-8') as f3:
                    f3.write(k+':'+v+'\n')


if __name__=='__main__':
    start_time = time.time()
    # 创建写html的路径，以时间为单位 。D:\spider_html\2018_01_05
    star_html = str("D:\\spider_html\\") + time.strftime('%Y_%m_%d', time.localtime(time.time())) \
                + str("\\")+str("star")+str("\\")
    star_movie_html = str("D:\\spider_html\\") + time.strftime('%Y_%m_%d', time.localtime(time.time())) \
                + str("\\") + str("movie") + str("\\")
    star_show_html = str("D:\\spider_html\\") + time.strftime('%Y_%m_%d', time.localtime(time.time())) \
                + str("\\") + str("show") + str("\\")
    path1 = mk.mkdir(star_html)
    path2 = mk.mkdir(star_movie_html)
    path3 = mk.mkdir(star_show_html)

    # 创建url列表
    path = '.\\oid_name_type\\20180107.txt'
    path_res = '.\\res_container\\res13'
    path_recommend = mk.mkdir('.\\recommend_container\\recommend8\\')
    # {starname:url}
    full = []
    full.append(star.get_mingxingurl_dict(path))
    full.append(star.get_yinyueurl_dict(path))

    for i in full:
        recomend(i, path1, path2, path3,path_res)

    name_topic.name_oid(path, path_res, path_recommend)

    ad_re_relation.add_re(path_recommend)

    count.count(path_recommend)

    end_time = time.time()
    print('程序运行了：' + (end_time - start_time) / 60 + '分钟')


