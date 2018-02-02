import os
import time
import shutil


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path
    else:
        return path


def get_data_file_path(relative_path):
    """
    取得最新的数据路径
    :return: format:{./oid_name_type/20180117.txt}
    """
    path = mkdir(relative_path)
    files = os.listdir(path)
    files.sort()
    file = files[-1]
    return path+'\\'+file


def res_name_path(relative_path):
    """
    取得抓取明星数据的文件地址
    :param relative_path:
    :return: format{./res_container/res_20180202_120807}
    """
    path = mkdir(relative_path)
    file_name = 'res'+'_'+time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    return path+'\\'+file_name


def recommed_file_path(relative_path):
    """
    取得recommend信息
    :param relative_path:
    :return: format：{./recommend_container/recommend_20180202_121758/}
    """
    path = mkdir(relative_path)
    dir_name = 'recommend'+'_'+time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    return mkdir(path+'\\'+dir_name+'\\')


def format_file():
    """
    清除往期数据，保存最近20个记录
    :return:
    """
    files1 = os.listdir('.\\oid_name_type')
    files2 = os.listdir('.\\recommend_container')
    files3 = os.listdir('.\\res_container')

    while len(files1)>19:
        files1.sort()
        file_name = files1[0]
        file_path = '.\\oid_name_type\\'+file_name
        # print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            files1 = os.listdir('.\\oid_name_type')

    while len(files2)>19:
        files2.sort()
        file_name = files2[0]
        file_path = '.\\recommend_container\\'+file_name
        # print(file_path)
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
            files2 = os.listdir('.\\recommend_container')

    while len(files3)>19:
        files3.sort()
        file_name = files3[0]
        file_path = '.\\res_container\\'+file_name
        # print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            files3 = os.listdir('.\\res_container')
