import re

class keywordCmp:
    def keywordCmp_SQL(self, tag_name_list, cmp_sql_check):
        data_list = list()
        with open("./Crawling/feature/SQLi.txt", 'r', encoding='UTF-8') as f:
            while True:
                param = f.readline().replace("\n", "")
                if not param:
                    break
                data_list.append(param)

        for i in range(len(tag_name_list)):
            for j in range(len(data_list)):
                if re.search(data_list[j], tag_name_list[i].lower()) and "(SQLi)" not in tag_name_list[tag_name_list.index(tag_name_list[i])]:
                    tag_name_list[tag_name_list.index(tag_name_list[i])] = tag_name_list[tag_name_list.index(tag_name_list[i])] + " (SQLi)"
                    cmp_sql_check = True

        return cmp_sql_check

    def keywordCmp_SQL_XSS(self, tag_name_list, cmp_sql_xss_check):
        data_list = list()
        with open("./Crawling/feature/XSS.txt", 'r', encoding='UTF-8') as f:
            while True:
                param = f.readline().replace("\n", "")
                if not param:
                    break
                data_list.append(param)

        for i in range(len(tag_name_list)):
            for j in range(len(data_list)):
                if re.search(data_list[j], tag_name_list[i].lower()) and "(XSS)" not in tag_name_list[tag_name_list.index(tag_name_list[i])]:
                    tag_name_list[tag_name_list.index(tag_name_list[i])] = tag_name_list[tag_name_list.index(tag_name_list[i])] + " (XSS)"
                    cmp_sql_xss_check = True

        return cmp_sql_xss_check

    def keywordCmp_Logic(self, tag_name_list, cmp_logic_check):
        data_list = list()
        with open("./Crawling/feature/LOGIC.txt", 'r', encoding='UTF-8') as f:
            while True:
                param = f.readline().replace("\n", "")
                if not param:
                    break
                data_list.append(param)

        for i in range(len(tag_name_list)):
            for j in range(len(data_list)):
                if re.search("^"+data_list[j], tag_name_list[i].lower()) and "(Logic)" not in tag_name_list[tag_name_list.index(tag_name_list[i])]:
                    tag_name_list[tag_name_list.index(tag_name_list[i])] = tag_name_list[tag_name_list.index(tag_name_list[i])] + " (Logic)"
                    cmp_logic_check = True

        return cmp_logic_check



'''
    def keywordCmp_SQL_XSS(self, tag_name_list, cmp_sql_xss_check):
        data_list = ["search", "text", "query"]

        for i in range(len(data_list)):
            for j in range(len(tag_name_list)):
                if tag_name_list[j] in data_list[i]:
                    tag_name_list[j] = tag_name_list[j] + " (SQL)"
                    cmp_sql_xss_check = True
        return cmp_sql_xss_check
'''