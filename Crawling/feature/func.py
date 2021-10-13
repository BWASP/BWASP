from urllib.parse import urlparse, urlunparse

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