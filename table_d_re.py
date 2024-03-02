import json
import os

with open('links_data.json', 'r', encoding='utf-8') as f:
    links_data = json.load(f)

course_info = {}

names = [key for key in links_data.keys()]

for name in names:
    print(links_data[name])

    print(links_data[name]['title'])
    p_title = links_data[name]['title']

    ja_title = p_title.split("[")[0]
    if len(p_title.split("[")) > 1:
        en_title = p_title.split("[")[1].replace("]", "")
    else:
        en_title = ""

    p_teachers = links_data[name]['teacher'].split("], ")
    ja_teachers = [p_teacher.split("[")[0] for p_teacher in p_teachers]
    en_teachers = [p_teacher.split("[")[1].replace("]", "") if len(p_teacher.split("[")) > 1 else "" for p_teacher in p_teachers]
    ja_teacher = ", ".join(ja_teachers)
    en_teacher = ", ".join(en_teachers)

    day_period = []
    if "集中" in links_data[name]['dp']:
        day_period.append("集中")
    
    days = ["月", "火", "水", "木", "金"]
    periods = ["1", "2", "3", "4", "5", "6", "7", "8"]
    found_days = []
    found_periods = []

    for day in days:
        if day in links_data[name]['dp']:
            found_days.append(day)
    for period in periods:
        if period in links_data[name]['dp']:
            found_periods.append(period)

    for day in found_days:
        for period in found_periods:
            day_period.append(day + period)

    course_info[name] = {
        "ja_title": ja_title,
        "en_title": en_title,
        "ja_teacher": ja_teacher,
        "en_teacher": en_teacher,
        "tt_number": name,
        "iki": links_data[name]['iki'],
        "rui": links_data[name]['rui'],
        "quarter": links_data[name]['q'],
        "day_period": ",".join(day_period),
        "link": links_data[name]['link']
    }

with open("course_info.json", "w", encoding="utf-8") as f:
    json.dump(course_info, f, indent=4, ensure_ascii=False)
    print('json_made_sucsessfuly')
