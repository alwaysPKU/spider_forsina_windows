# 把推荐列表转成topicid形式
import json as js

# 把name——topicid存入词典
def name_oid(path,path_res,path_recommend):
    star_dic = dict()
    with open(path,
              encoding='utf-8') as f:
        line = f.readline()
        while line:
            item = line.split()
            if len(item) == 3 and item[2] == '明星':
                if item[1][0:2] == '演员':
                    print(item[1])
                    star_dic[item[1].lstrip('演员')] = item[0]
                    # print(star_dic)
                elif item[1][0:3] == '小演员':
                    print(item[1])
                    star_dic[item[1].lstrip('小演员')] = item[0]
                    # print(star_dic)
                elif item[1][0:4] == '泰国演员':
                    print(item[1])
                    star_dic[item[1].lstrip('泰国演员')] = item[0]
                    # print(star_dic)
                elif item[1][0:4] == '配音演员':
                    print(item[1])
                    star_dic[item[1].lstrip('配音演员')] = item[0]
                    # print(star_dic)
                # elif item[1][0:4] == '国话演员':
                #     print(item[1])
                #     star_dic[item[1].lstrip('国话演员')] = item[0]
                #     # print(star_dic)
                # elif item[1][0:4] == '上海演员':
                #     print(item[1])
                #     star_dic[item[1].lstrip('上海演员')] = item[0]
                #     # print(star_dic)
                # elif item[1][0:4] == '著名演员':
                #     print(item[1])
                #     star_dic[item[1].lstrip('著名演员')] = item[0]
                #     # print(star_dic)
                # elif item[1][0:5] == '实力派演员':
                #     print(item[1])
                #     star_dic[item[1].lstrip('实力派演员')] = item[0]
                    # print(star_dic)
                else:
                    star_dic[item[1]] = item[0]
            elif len(item) == 3 and item[2] == '音乐':
                    star_dic[item[1]] = item[0]
            line = f.readline()
            # time.sleep(1)

    # 转换name到topicid
    with open(path_res, 'r',
              encoding='utf-8') as f0:
        line = f0.readline()
        # full = {}
        # full_relation=[]

        count_for_all = {}
        count_for_all['relation']=0
        count_for_all['movie']=0
        count_for_all['show']=0
        count_for_id = {}
        count_for_id['relation'] = 0
        count_for_id['movie'] = 0
        count_for_id['show'] = 0
        while line:
            # print(line)
            key = {}
            key.keys()
            data = js.loads(line)

            new_topic_dic={} # 存储topic形式的推荐
            count_topic_dic={} # 存储统计
            lose_topic_id ={}
            for i in data.keys():
                # i就是被推荐明星名字
                relation_list = data[i]

                flag_list=[]  # 存储每个明星的关系
                count_list=[] # 存储每个明星的每个关系的统计量
                lose_list=[] # 存储没有转换的明星关系

                for j in relation_list:
                    # j就是relation或者movie或者show的词典
                    for k in j.keys():
                        # k就是relation或者movie或者show的key
                        flag_dic = {} # 存储三种关系之一的转换结果
                        flag_count = {} # 存储三种关系之一的统计结果
                        flag_lose ={} # 寻出未转换成功的三种关系的结果
                        flag = k
                        name_list=j[k]  # k关系的名单
                        new_name_list = []  # k关系的转换列表
                        lose_name_lise = []  # k关系的未转换成功列表
                        # 统计
                        count_id = 0  # 有topicid的
                        count_all = 0  # 所有的
                        for l in name_list:
                            count_all+=1 #所有明星
                            if l in star_dic.keys():
                                # 有topicid的明星转换并存储
                                count_id+=1
                                item_topic = star_dic[l]
                                new_name_list.append(item_topic)
                            else:
                                # 没有topicid的明星存储
                                lose_name_lise.append(l)
                                continue
                        # 统计总结果：
                        count_for_all[k]+=count_all
                        count_for_id[k]+=count_id
                        # 存储统计
                        itm = str(str(count_id)+'/'+str(count_all))
                        flag_count[k]=itm
                        count_list.append(flag_count)
                        # 存储topic转换结果
                        if len(new_name_list)!=0:
                            flag_dic[k]=new_name_list
                            flag_list.append(flag_dic)
                        # 存储topicid未转换的结果
                        if len(lose_name_lise)!=0:
                            flag_lose[k]=lose_name_lise
                            lose_list.append(flag_lose)
                # 存储统计
                    count_topic_dic[i]=count_list
                # 存储非空的topicid转换结果
                if len(flag_list)!=0:
                    if i in star_dic.keys():
                        topicId = star_dic[i]
                        new_topic_dic[topicId]=flag_list
                    else:
                        new_topic_dic[i]=flag_list
                # 存储未转换topicid的结果：
                if len(lose_list)!=0:
                    lose_topic_id[i] = lose_list
            # 写结果
            if len(new_topic_dic)!= 0:
                data = js.dumps(new_topic_dic,ensure_ascii=False)
                with open(path_recommend+'recommend_list_prior', 'a', encoding='utf-8') as f1:
                    f1.write(data+'\n')

            # 写统计结果
            data_count = js.dumps(count_topic_dic, ensure_ascii=False)
            with open(path_recommend+'recommend_count', 'a', encoding='utf-8') as f2:
                f2.write(data_count+'\n')

            # 写未转换topic的名单
            if len(lose_topic_id)!=0:
                data3 = js.dumps(lose_topic_id, ensure_ascii=False)
                with open(path_recommend+'recommend_lose', 'a', encoding='utf-8') as f3:
                    f3.write(data3+'\n')
            # 循环下一行
            line=f0.readline()

    # 总的结果写出到recommend_list
    data_all = js.dumps(count_for_all, ensure_ascii=False)
    data_id = js.dumps(count_for_id, ensure_ascii=False)
    with open(path_recommend+'recommend_count', 'a', encoding='utf-8' ) as ff:
        ff.write('一共有数据：'+data_all+'\n')
        ff.write('匹配到id的：'+data_id+'\n')
