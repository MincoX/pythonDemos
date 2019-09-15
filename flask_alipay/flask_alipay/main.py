import os
import logging
import uuid
import requests

from flask import Flask, jsonify, render_template, request, redirect

from alipay import AliPay

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/pay')


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    """
    向支付宝发起支付请求
    :return:
    """
    # 创建支付宝 SDK 的工具对象

    alipay_client = AliPay(
        # 沙箱环境的 appid
        appid='2016101000651095',
        app_notify_url=None,  # 默认支付宝通知url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key"),

        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key"),

        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False, 如果是沙箱模式，debug=True
    )

    # 向支付宝发起手机网站支付的请求
    # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string  # 沙箱环境
    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=str(uuid.uuid4()),  # 我们自己的订单编号
        total_amount='100',  # 订单总金额, 以元为单位
        subject=u"学习支付",  # 展示给用户的订单信息
        return_url="http://127.0.0.1:5000/static/complete_pay.html",  # 支付完成后跳转回的页面路径
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 用户要访问的支付宝链接地址
    logging.debug(order_string)
    pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    resp = requests.post(url=pay_url)
    context = {
        'pay_url': pay_url
    }

    return render_template('index.html', **context)


@app.route('/pay_result', methods=['GET', 'PUT'])
def pay_result():
    alipay_data = request.form.to_dict()

    # 对支付宝的签名进行处理
    alipay_sign = alipay_data.pop('sign')

    # 创建支付宝 SDK 的工具对象
    alipay_client = AliPay(
        # 沙箱环境的 appid
        appid='2016101000651095',
        app_notify_url=None,  # 默认支付宝通知url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key"),

        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key"),

        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False, 如果是沙箱模式，debug=True
    )

    # 借助工具进行参数验证, 将自己生成的签名值和支付宝返回的签名只进行验证处理

    result = alipay_client.verify(alipay_data, alipay_sign)

    if result:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
