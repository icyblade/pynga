#! coding: utf8

from datetime import datetime

def timestamp2str(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    
def split(dataset, ratio):
    """ 按比例分割数据集 """
    n, m = len(dataset), len(ratio)
    offset = int(n*ratio[0])/sum(ratio)
    if m != 1:
        return (dataset[0:offset],)+(split(dataset[offset:], ratio[1:]))
    else:
        return (dataset, )
