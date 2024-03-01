import json
import os
from bs4 import BeautifulSoup

with open('links_data.json', 'r', encoding='utf-8') as f:
    links_data = json.load(f)

names = [key for key in links_data.keys()]

html_names = [name + '.html' for name in names]

print(html_names)

data = {}

for html_name in html_names:
    with open(f'./htmls/{html_name}', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    je_title = soup.find(id="ctl00_phContents_Detail_lbl_lct_name_double").get_text(strip=True)
    ja_title = je_title.split("[")[0]
    if len(je_title.split("[")) > 1:
        en_title = je_title.split("[")[1].replace("]", "")
    else:
        en_title = ""

    je_teacher = soup.find(id="ctl00_phContents_Detail_lbl_syl_staff_name_link_double").get_text(strip=True)
    ja_teacher = je_teacher.split("[")[0]
    if len(je_teacher.split("[")) > 1:
        en_teacher = je_teacher.split("[")[1].replace("]", "")
    else:
        en_teacher = ""

    course_info = {
        "ja_title": ja_title,
        "en_title": en_title,
        "ja_teacher": ja_teacher,
        "en_teacher": en_teacher,
        "class_number": soup.find(id="ctl00_phContents_Detail_lbl_numbering").get_text(strip=True),
        "tt_number": soup.find(id="ctl00_phContents_Detail_lbl_lct_cd").get_text(strip=True),
        "lct_style": soup.find(id="ctl00_phContents_Detail_lbl_lct_type_name").get_text(strip=True),
        "iki": soup.find(id="ctl00_phContents_Detail_lbl_faculty_name").get_text(strip=True),
        "rui": links_data[html_name.replace('.html', '')]["rui"],
        "teisei": soup.find(id="ctl00_phContents_Detail_lbl_class_size_disp").get_text(strip=True),
        "quarter": soup.find(id="ctl00_phContents_Detail_lbl_lct_term_name").get_text(strip=True),
        "day_period": soup.find(id="ctl00_phContents_Detail_lbl_day_period").get_text(strip=True),
        "credits": soup.find(id="ctl00_phContents_Detail_lbl_credits_disp").get_text(strip=True),
        #"class_style": soup.find(id="ctl00_phContents_Detail_lbl_lct_style_name").get_text(strip=True),
        "target": soup.find(id="ctl00_phContents_Detail_lbl_target").get_text(strip=True),
        "lecture_room_info": soup.find(id="ctl00_phContents_Detail_lbl_lecture_room_infomation").get_text(strip=True),

        "link": links_data[html_name.replace('.html', '')]["link"],
    }

    print(course_info)

    data[html_name.replace('.html', '')] = course_info

with open("course_info.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('course_info.jsonを作成しました。')


