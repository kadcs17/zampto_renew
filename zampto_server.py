import os
import time
import traceback
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
export HTTP_PROXY="https://72.213.88.134:443"

app = Flask(__name__)

def renew_zampto(email, password, domain):
    proxy_server = os.getenv("HTTP_PROXY")  # ✅ 从环境变量读取代理
    proxy = {"server": proxy_server} if proxy_server else None

    with sync_playwright() as p:
        # ✅ 使用代理启动浏览器
        browser = p.chromium.launch(
            headless=True,
            proxy=proxy
        )

        context = browser.new_context()
        page = context.new_page()
def renew_zampto(email, password, domain):
    # ✅ 新增代理设置
    proxy_server = os.getenv("HTTP_PROXY")
    proxy = {"server": proxy_server} if proxy_server else None

    with sync_playwright() as p:
        # ✅ 加上 proxy 参数
        browser = p.chromium.launch(headless=True, proxy=proxy)
        context = browser.new_context()
        page = context.new_page()


        try:
            print(f"[*] 打开 Zampto 登录页面...")
            page.goto("https://zampto.com/login")

            page.fill('input[name="email"]', email)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
            page.wait_for_timeout(3000)

            print(f"[*] 登录成功，进入域名页面...")
            page.goto("https://zampto.com/domains")
            page.wait_for_timeout(3000)

            print(f"[*] 查找域名 {domain} ...")
            page.locator(f"text={domain}").click()
            page.wait_for_timeout(2000)

            print("[*] 点击 Renew 按钮")
            page.locator('text=Renew').click()
            page.wait_for_timeout(3000)

            print("[✅] 域名续期完成！")
            browser.close()
            return True

        except Exception as e:
            print("[❌] 续期失败:", e)
            traceback.print_exc()
            browser.close()
            return False

@app.route('/renew', methods=['POST'])
def renew():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    domain = data.get("domain")

    if not (email and password and domain):
        return jsonify({"success": False, "msg": "缺少必要参数"}), 400

    ok = renew_zampto(email, password, domain)
    return jsonify({"success": ok})

if __name__ == '__main__':
    # ✅ 可以在启动时设置代理
    export HTTP_PROXY="https://72.213.88.134:443"
    # python zampto_server.py
    app.run(host='0.0.0.0', port=5000)

