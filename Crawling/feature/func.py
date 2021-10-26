from urllib.parse import urlparse, urlunparse
import os

def isSameDomain(target_url, visit_url):
    try:
        target = urlparse(target_url)
        visit = urlparse(visit_url)

        if visit.scheme != "http" and visit.scheme != "https":
            return False
        if target.netloc == visit.netloc:
            return True
        else:
            return False
    except:
        return False

def isSamePath(visit_url, previous_urls):
    try:
        visit = urlparse(visit_url)

        for link in previous_urls:
            previous = urlparse(link)

            if (visit.path == previous.path) and (visit.query == previous.query):
                return True

            # https://naver.com 과 https://naver.com/ 는 같은 url 이므로 검증하는 코드 작성.
            visit_path_len = len(visit.path.replace("/", ""))
            previous_path_len = len(previous.path.replace("/", ""))

            if visit_path_len == 0 and previous_path_len == 0:
                return True
        else:
            return False
    except:
        return False

def get_dbpath(repo_name="BWASP",prefix="sqlite:///",sub_path="Web\databases\BWASP.db"):
    repopath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    index = repopath.find(repo_name)
    repopath = repopath[:index+len(repo_name)]
    return (prefix+repopath+"\\"+sub_path).replace("\\","\\\\")

"""
    This function check the extension of url.
        - url: String
        - key: String
        - return: boolean
"""
def isExistExtension(url, key):
    extensions_dict = {
        "image" : ["png", "gif", "jpg", "jpeg", "webp", "tiff", "bmp", "svg", "jpe", "jif", "jfif", "jfi"]
    }

    if not key in list(extensions_dict.keys()):
        return False
    
    extension_list = extensions_dict[key]
    url_extension = url.split(".")[::-1][0]

    if url_extension in extension_list:
        return True
    else:
        return False