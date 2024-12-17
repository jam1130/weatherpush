import requests
import datetime
import schedule
import time

# -------------------------- 配置部分 -------------------------- #
# 和风天气 API 配置
HEFENG_API_KEY = "4da911dbf9534137838473f66fcbd2fd"  # 替换为你的和风天气 API Key
CITY = "101040800"  # 北京的城市代码，可根据和风城市列表替换为其他城市代码

# Server酱配置
SCKEY = "SCT265435TMjOl6e15qVEhfLh5KY9AkUW5"  # 替换为你的 Server酱 SendKey
SERVERCHAN_URL = f"https://sctapi.ftqq.com/{SCKEY}.send"

# Hitokoto每日一句 API
HITOKOTO_API = "https://v1.hitokoto.cn/?c=d"  # `c=d`表示日常类名句
# ------------------------------------------------------------ #


# 获取天气信息
def get_weather():
    weather_url = f"https://devapi.qweather.com/v7/weather/now?location={CITY}&key={HEFENG_API_KEY}"
    try:
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            now = data["now"]  # 当前天气相关信息
            temp = now["temp"]  # 当前气温
            description = now["text"]  # 天气描述
            wind = now["windDir"]  # 风向
            feels_like = now["feelsLike"]  # 体感温度
            # 返回处理好的天气信息
            return f"今日天气：{description}，当前气温 {temp}℃，体感温度 {feels_like}℃，风向：{wind}。记得照顾好自己哦！"
        else:
            return "天气 API 请求失败，请检查配置或稍后再试。"
    except Exception as e:
        return f"获取天气信息失败，错误原因：{str(e)}"


# 获取每日一句
def get_daily_sentence():
    try:
        response = requests.get(HITOKOTO_API)
        if response.status_code == 200:
            data = response.json()
            # 返回每日一句
            return f"「{data['hitokoto']}」 —— {data['from']}"
        else:
            return "无法获取每日一句，请稍后再试。"
    except Exception as e:
        return f"获取每日一句失败，错误原因：{str(e)}"


# 推送消息到 Server酱
def push_message_to_wechat(title, content):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "title": title,   # 消息标题
        "desp": content,  # 消息内容（支持Markdown格式）
    }
    try:
        response = requests.post(SERVERCHAN_URL, data=data, headers=headers)
        if response.status_code == 200 and response.json().get("code") == 0:
            print("消息推送成功！")
        else:
            print(f"推送失败：{response.json()}")
    except Exception as e:
        print(f"推送消息出现错误：{str(e)}")


# 主程序
def main():
    today = datetime.date.today().strftime("%Y年%m月%d日")  # 获取当前日期
    weather_info = get_weather()  # 获取天气信息
    daily_sentence = get_daily_sentence()  # 获取每日一句

    # 拼接完整消息
    title = "宝宝早上好，请查看今天的天气预报"
    content = (
        f"### 📅 {today}\n\n"  
        f"#### 今日天气\n\n{weather_info}\n\n"  
        f"#### 每日一句\n\n{daily_sentence}\n\n"  
        "祝欣欣宝宝每天都有好心情！😊"
    )

    # 推送到 Server酱
    push_message_to_wechat(title, content)


# 定时任务调度
def schedule_task():
    # 每天早上 8 点运行任务
    schedule.every().day.at("08:00").do(main)

    print("定时任务已启动，等待运行...")
    while True:
        schedule.run_pending()
        time.sleep(1)


# 程序入口
if __name__ == "__main__":
    schedule_task()