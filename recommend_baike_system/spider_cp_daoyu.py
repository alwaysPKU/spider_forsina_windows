import load_url as lurl

first = 'https://weibo.com/p/100808'
third = '/super_index'
with open('/Users/zhangwei/Desktop/sina_job/recommend/oid_name_type/20171225.txt') as f:
    full_dict = {}
    line = f.readline()
    while line:
        item = line.split()
        # print(item)
        if len(item)==3 and item[2]=='CP':

            full_dict[item[1]]=first+item[0]+third
        line = f.readline()

print(full_dict)



# /Users/zhangwei/Desktop/sina_job/recommend