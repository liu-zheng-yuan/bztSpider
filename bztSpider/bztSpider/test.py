import requests
# ?channel=xiaocong-channel&client=pc&cursor=1544592877&limit=50&first_page=false&accept_symbols=coin
#API分析 https://api-prod.wallstreetcn.com/apiv1/content/lives
#channel 怀疑是频道 必须有 保持
#client 登录端 保持？
#cursor 快讯的时间戳 可改 下次request要修改时间戳
#limit 一次返回的快讯数量
#first_page 是否首页
r = requests.get("https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=xiaocong-channel&client=pc&cursor=1545211375&limit=25&first_page=false");
print(r.json())
print(len(r.json()['data']['items']))