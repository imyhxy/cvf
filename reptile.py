# coding=utf-8
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import traceback
import re
import os

conf_list = ['CVPR2019']

prefix = 'http://openaccess.thecvf.com/'

def get_pdf(data):
    href, title, root_dir = data
    name = re.sub(r'[\\/:*?"<>|]', ' ', title) 
    if os.path.isfile("{}/{}.pdf".format(root_dir, name)):
        print("File already exsists, skip %s" % name)
        return
    try:
        content = requests.get(prefix+href).content
        with open(root_dir +"/%s.pdf" % name, 'wb') as f:  # You may change to "path/to/your/folder"
            f.write(content)
        print("Finish downloading %s" % title)
    except:
        print('Error when downloading %s' % href)
        print(traceback.format_exc())

def conf_name(name, num):
    for _ in range(num):
        yield name

if __name__ == '__main__':
    pool = Pool(10)
    for conf in conf_list:
        if not os.path.exists(conf):
            os.mkdir(conf)
        html = requests.get(prefix+'/{}.py'.format(conf)).content
        soup = BeautifulSoup(html, "lxml")
        a_list = soup.findAll('a')
        title_list = soup.findAll("dt", {"class": "ptitle"})
        title_list = [_.text for _ in title_list]
        pdf_list = []
        for everya in a_list:
            if everya.text.strip() == "pdf":
                href = everya.get("href").strip()
                pdf_list.append(href)
        assert len(pdf_list) == len(title_list), "numbers of title and pdf not euqal"
        print("Find %d papers" % len(pdf_list))
        name = conf_name(conf, len(title_list))
        pool.map(get_pdf, zip(pdf_list, title_list, name))
