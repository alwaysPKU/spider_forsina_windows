import json as js
def count(path_recommend):
    with open(path_recommend+'recommend_list') as f:
        n=0
        line = f.readline()
        full_count={}
        full_count['relation']=0
        full_count['movie']=0
        full_count['show']=0
        while line:
            if line != None:
                n += 1
            item = js.loads(line)
            for k,v in item.items():
                for i in v:
                    for k2,v2 in i.items():
                        full_count[k2]=full_count[k2]+len(v2)
            line=f.readline()
    with open(path_recommend+'recommend_count','a',encoding='utf-8') as f2:
        f2.write('增加双向关系后:'+str(n)+js.dumps(full_count))
    print(n, full_count)
