# 支付宝

1. 沙箱环境密钥对的配置

   1. 支付宝沙箱页面下载工具, 在本地生成RSA2  app 公私密钥对

   2. 将生成的 app 公钥配置在沙箱环境中, 并得到支付宝的公钥

   3. 在项目中创建 keys 文件夹, 用于存放支付宝的公钥和 app 的私钥文件

      注: txt 文件都以固定的格式开始和结尾

      ```
      alipay_public_key.txt
      -----BEGIN PUBLIC KEY-----
      alipay 的公钥字符串
      -----END PUBLIC KEY-----
      
      app_private_key.txt
      -----BEGIN RSA PRIVATE KEY-----
      app 的私钥字符串
      -----END RSA PRIVATE KEY-----
      ```

2. 实现

   1. 安装 python 包

      ```
      python-alipay-sdk==1.10.1
      ```

   2. 创建支付宝 SDK 工具对象

      ```
      from alipay import AliPay
      
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
      ```

   3. 发起支付请求

      ```
      order_string = alipay_client.api_alipay_trade_wap_pay(
              out_trade_no=str(uuid.uuid4()),  # 我们自己的订单编号
              total_amount='100',  # 订单总金额, 以元为单位
              subject=u"学习支付",  # 展示给用户的订单信息
              return_url=None,  # 支付完成后跳转回的页面路径
              # 可选, 不填则使用默认notify url
              notify_url='http://127.0.0.1:5000/static/return_url.html'  
          )
      ```

      