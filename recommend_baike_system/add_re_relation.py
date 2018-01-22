import json as js

# full_list= []
# with open('/Users/zhangwei/PycharmProjects/recommend_baike_system/recommend2/recommend_list') as f:
#     data = f.readlines()
#     for item in data:
#         full_list.append(js.loads(item))
#     # print(full_list[0])
def add_re(path_recommend):
    with open( path_recommend+'recommend_list_prior', encoding='utf-8') as f1:
        full_dic={}
        line = f1.readline()
        while line:
            line_data = js.loads(line)
            item = {}
            for k, v in line_data.items():
                tmp = {}
                for v_data in v:
                    for i in v_data.keys():
                        tmp[i] = v_data[i]
                full_dic[k] = tmp
            # # # print(type(line_data))
            # # for key,value_list in line_data.items():
            # #     itm_set = set()
            # #     for i in value_list:
            # #         item_set2 = set()
            # #         for j in i:
            # #             item_set2=set(i[j])
            # #         itm_set = itm_set | item_set2
            # #     full_dic[key] = itm_set
            # for key in line_data.keys():
            line = f1.readline()

    n=0
    with open(path_recommend+'recommend_list','a',encoding='utf-8') as f2:
        with open(path_recommend+'recommend_list_prior',encoding='utf-8') as f3:
            line = f3.readline()
            full_count={}
            full_count['relation']=0
            full_count['movie']=0
            full_count['show']=0
            while line:
                line_data = js.loads(line)
                item={}
                for k,v in line_data.items():
                    tmp = {}
                    for v_data in v:
                        for i in v_data.keys():
                            tmp[i]=v_data[i]
                    item[k]=tmp
                    # print(item)
                for k,v in item.items():
                    for re_k,compare_v in full_dic.items():
                        for mark_3, id_list in compare_v.items():
                            if k in id_list:
                                if mark_3 in item[k].keys() and re_k not in item[k][mark_3]:
                                    item[k][mark_3].append(re_k)
                                    full_count[mark_3]=full_count[mark_3]+1
                                elif mark_3 not in item[k].keys():
                                    tmp=[]
                                    tmp.append(re_k)
                                    item[k][mark_3]=tmp
                                    full_count[mark_3]=full_count[mark_3]+1
                # 改回以前的格式
                newdata={}
                newlist=[]
                for k,v in item.items():
                    for m3,v in v.items():
                        tmp={}
                        tmp[m3]=v
                        newlist.append(tmp)
                    newdata[k]=newlist


                write_data=js.dumps(newdata)
                f2.write(write_data+'\n')

                line=f3.readline()
    with open(path_recommend+'recommend_count','a',encoding='utf-8') as f4:
        f4.write('增加双向关系量:'+js.dumps(full_count)+'\n')
    print('增加的双向关系量：', full_count)