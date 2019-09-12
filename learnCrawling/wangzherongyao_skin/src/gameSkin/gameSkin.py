#爬取王者荣耀英雄图片
#导入所需模块
import requests
import re
import os
#导入json文件（里面有所有英雄的名字及数字）
url='http://pvp.qq.com/web201605/js/herolist.json'
#英雄的名字
jsonhead={'User-Agent':'xdhead'}
html = requests.get(url,headers = jsonhead)
html=requests.get(url)
html_json=html.json()
#提取英雄名字和数字
hero_name=list(map(lambda x:x['cname'],html_json))
#名字
hero_number=list(map(lambda x:x['ename'],html_json))
#数字

def gameSkin():
    #用于下载并保存图片
    ii=0
    for v in hero_number:
        os.mkdir("D:\database\\" + hero_name[ii])
        #换成你自己的
        os.chdir("D:\database\\" + hero_name[ii])
        #换成你自己的
        ii=ii+1
        for u in range(12):
            onehero_links='http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(v)+'/'+str(v)+'-bigskin-'+str(u)+'.jpg'
            im = requests.get(onehero_links)
            if im.status_code == 200:
                iv=re.split('-',onehero_links)
                open(iv[-1], 'wb').write(im.content)

if __name__ == "__main__":
    gameSkin()
