import json
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

def read_serpapi_key():
    key_path = os.path.join(BASE_DIR, "serpapi.key") 
    if not os.path.exists(key_path):
        raise OSError(f"SerpAPI key file not found: {key_path}")
    
    with open(key_path, "r") as key_file:
        return key_file.read().strip()




# 运行搜索查询
def run_query(search_terms):
    """
    使用 SerpAPI 进行 Google 搜索
    参考文档：https://serpapi.com/
    """
    serpapi_key = read_serpapi_key()
    search_url = 'https://serpapi.com/search'

    # 设置请求参数
    params = {
        'q': search_terms,        # 搜索关键词
        'api_key': serpapi_key,   # API Key
        'engine': 'google',       # 指定搜索引擎
        'num': 10                 # 返回 10 个搜索结果
    }

    # 发送请求
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()

    # 解析返回的 JSON 数据
    results = []
    if 'organic_results' in search_results:
        for result in search_results['organic_results']:
            results.append({
                'title': result.get('title', 'No Title'),
                'link': result.get('link', 'No URL'),
                'summary': result.get('snippet', 'No Snippet')
            })
    
    return results


# 测试搜索功能
if __name__ == "__main__":
    query = "树莓派"
    search_results = run_query(query)

    # 打印前 5 个搜索结果
    for i, result in enumerate(search_results[:5]):
        print(f"{i+1}. {result['title']}\n   {result['link']}\n   {result['summary']}\n")
