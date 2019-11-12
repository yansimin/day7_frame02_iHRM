"""
封装unittest相关实现
"""
# 1.导包
import json
import unittest
import requests

import app
from api.LoginAPI import Login
# 参数化步骤1：导包
from parameterized import parameterized

# 参数化步骤2：解析
def read_json_file():
    # 1.创建空列表
    data = []

    # 2.解析文件流，将数据追加进列表
    with open(app.PRO_PATH + '/data/login_data.json',encoding='utf-8') as f:
        for v in json.load(f).values():
            mobile = v.get('mobile')
            password = v.get('password')
            success = v.get('success')
            code = v.get('code')
            message = v.get('message')
            # 组织成元组
            ele = (mobile,password,success,code,message)
            data.append(ele)

    # 3.返回列表
    return data


# 2.创建测试类（继承unittest.TestCase）：
class Test_Login(unittest.TestCase):

   # 3.初始化函数
    def setUp(self) -> None:
        # 初始化 session
        self.session = requests.session()

        # 初始化api对象
        self.login_obj = Login()

    # 4.资源卸载函数
    def tearDown(self) -> None:
        # 销毁session
        self.session.close()

    # 5.核心：测试函数 - 登陆
    # 5-1参数化
   # 参数化步骤3：调用解析函数
    @parameterized.expand(read_json_file())
    def test_login(self,mobile,password,success,code,message):
        print('-' * 100)
        print('参数化读取的参数：',mobile,password,success,code,message)
        # 5-2 请求业务
        response = self.login_obj.login(self.session,mobile,password)
        print('登陆响应结果：',response.json())

        # 5-3 断言业务
        self.assertEqual(success,response.json().get('success'))
        self.assertEqual(code, response.json().get('code'))
        self.assertIn(message, response.json().get('message'))


    # 编写登陆成功的测试函数
    def test_login_success(self):
        # 1.直接通过提交正向数据发送请求业务
        response = self.login_obj.login(self.session,'13800000002','123456')

        # 2.断言业务
        # 结果：{'success': True, 'code': 10000, 'message': '操作成功！', 'data': '328fac4d-f889-44fd-ae46-87421ee30775'}
        print('登陆成功的结果',response.json())
        self.assertEqual(True,response.json().get('success'))
        self.assertEqual(10000,response.json().get('code'))
        self.assertIn('操作成功',response.json().get('message'))
        # 提取token
        token = response.json().get('data')
        print('登陆后响应的token：',token)
        # 预期允许其他文件调用token，可以扩大token的作用域(将token赋值给app的一个全局变量)）
        app.TOKEN = token


if __name__ == '__main__':
    unittest.main()