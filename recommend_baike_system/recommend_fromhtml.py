import os
import get_analysis_url as movie
import json as js

# filepath = "/Users/zhangwei/Desktop/sina_job/html_process/html/"
filepath = "/Users/zhangwei/Desktop/sina_job/html_process/html_test/"
paths = os.listdir(filepath)

filenames = os.listdir(filepath)

with open('./test','w') as f:
# with open('./test', 'a') as f:
    for file in filenames:
        full={}
        full_relation=[]
        movie_dic = {}
        show_dic = {}
        print('======'+file+'======')
        if file == '.DS_Store':
            continue
        path = filepath+file
        # print(path)
        star_name = file
        movieurl=movie.get_movieurl(path)
        showurl=movie.get_showurl(path)
        relation = movie.analysis_relation(path) #list
        # print(urllist)

        # if len(relation)!=0:
        #     print('relation')
        #     full_relation.extend(relation)
        #     print('relation_over')
        if len(relation)!=0:
            tmp_dict={}
            tmp_list=[]
            print('relation')
            for i in relation:
                for j in i.keys():
                    tmp_list.append(i[j])
            tmp_dict['relation']=tmp_list
            full_relation.append(tmp_dict)
            print('relation_over')

        if movieurl != None:
            print('movie')
            movie_set = set()
            # 逐一借些movie的url
            for url in movieurl:
                # print(url)
                tmpset = movie.analysis_movieurl2(url)
                # print(tmpset)
                if tmpset != None and len(tmpset)!=0:
                    movie_set=movie_set | tmpset
                else:
                    continue
            # 把该明星名字从列表中去除
            if movie_set != '' and star_name in movie_set:
                movie_set.remove(star_name)
            movie_list=list(movie_set)
            movie_dic['movie']=movie_list
            if len(movie_dic['movie']) != 0 and movie_dic['movie'] != None:
                full_relation.append(movie_dic)
                print('movie_over')

        if showurl!= None:
            print('show')
            show_set = set()
            for url in showurl:
                # print(url)
                tmpset2 = movie.analysis_showurl(url)
                # print(tmpset2)
                if tmpset2 !=None and len(tmpset2)!=0:
                    show_set=show_set | tmpset2
                else:
                    continue
            show_list=list(show_set)
            # print(show_list)
            show_dic['show'] = show_list
            if len(show_dic['show']) != 0 and show_dic['show'] != None:
                full_relation.append(show_dic)
                print('show_over')


        if len(full_relation)!=0:
            full[star_name]=full_relation
            data = js.dumps(full, ensure_ascii=False)
            f.write(data+'\n')

