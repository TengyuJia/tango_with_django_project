import json
import requests

# 读取 SerpAPI Key
def read_serpapi_key():
    """
    读取 SerpAPI API key，文件命名为 'serpapi.key'
    返回 API Key 字符串
    """
    serpapi_key = None
    try:
        with open('serpapi.key', 'r') as f:
            serpapi_key = f.readline().strip()
    except:
        try:
            with open('../serpapi.key') as f:
                serpapi_key = f.readline().strip()
        except:
            raise IOError('serpapi.key 文件未找到')

    if not serpapi_key:
        raise KeyError('SerpAPI Key 未找到')

    return serpapi_key


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
