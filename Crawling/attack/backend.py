import json
import os 

json_path="../wappalyzer/"
categories_path="../wappalyzer/categories.json"
default_allow_cat={12,18,27,22}
default_check_cat={12,18,27,22}



def extractJson(check_cat={12,18,27,22},allow_cat={12,18,27,22}):
    #12(javascript framework),18(Web frameworks),22(web server),27(Programming Language)
    check_cat = set(check_cat)
    json_list = os.listdir(json_path)
    json_list.remove("categories.json")
    result={}
    for line in json_list:
        with open(json_path+line,encoding='UTF8') as json_file:
            json_data = json.load(json_file)
            for name in json_data:
                if set(check_cat) & set(json_data[name]['cats']):
                    #print(json_data[name])
                    result[name]=json_data[name]
    return result



def extractPriority(cat=[12,18,27,22]):
    cat = sorted(cat)
    cat_priority={}
    print("extractprirority")
    with open(categories_path,encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        print(cat)
        for eachcat in cat:
            cat_priority[eachcat] = json_data[str(eachcat)]['priority']
    return cat_priority

#cat priority가 클수록 ,  같을 경우  카테고리가 번호가 우선 순위가 높다가정해서 선택 
def retCatrepresnt(check_cat,allow_cat):
    if len(check_cat) == 1:
        return check_cat
    else:
        cat_priority=extractPriority(check_cat)
        #cat_represent 우선 순위로 정해진 대표 cat 번호
        cat_reprent = -1
        while not cat_reprent in allow_cat:
            cat_reprent=max(cat_priority,key=cat_priority.get)
            del[cat_priority[cat_reprent]]
        #카테고리(cat) 번호 반환
        return cat_reprent

# retCatname(1) => cat 1 에 해당하는 이름 반환
def retCatname(singlecat):
    #12(javascript framework),18(Web frameworks),22(web server),27(Programming Language)
    with open(categories_path,encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        return json_data[str(singlecat)]#['name']

#retCatsname([12,13])으로 호출 가능 , name 반환   
def retCatsname(cat):
    #12(javascript framework),18(Web frameworks),22(web server),27(Programming Language)
    cat_name={}
    with open(categories_path,encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        for eachcat in cat:
            cat_name[eachcat] = json_data[str(eachcat)]['name']
    return cat_name


if __name__ == '__main__':
     print(extractJson())
     #print(retCatsname([12,18,27,22]))
     #print(18,retCatname(18))