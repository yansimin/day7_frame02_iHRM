"""
测试套件：
    按照需求组合被执行的测试函数

自动化测试执行顺序：
    增 → 改 → 查 → 删

补充说明：
    关于测试套件的组织，接口业务测试中，需要保证测试套件中接口的执行顺序
    合法实现：suite.addTest(类名('函数名'))
    非法实现：suite.addTest(unittest.makesuite(类名)) 虽然可以一次性添加多个测试函数，但是无法保证执行顺序

如果使用参数传递数据，会调用失败，暂时无解
"""
# 1.导包
import unittest
import app
from case.Test_iHRM_Emp import Test_Emp
from case.Test_iHRM_Login import Test_Login
from tools.HTMLTestRunner import HTMLTestRunner


# 2.实例化套件对象，组织被执行的测试函数
# 并发执行/顺序执行   批量执行一个类就是并发执行，无法预估执行顺序

suite = unittest.TestSuite()
suite.addTest(Test_Login('test_login_success'))  # 组织登录成功的测试函数
suite.addTest(Test_Emp('test_add'))  # 组织员工新增的测试函数
suite.addTest(Test_Emp('test_update'))  # 组织员工修改的测试函数
suite.addTest(Test_Emp('test_get'))  # 组织员工查询的测试函数
suite.addTest(Test_Emp('test_delete'))  # 组织删除的测试函数

# 3.执行套件，生成测试报告
# runner = unittest.TextTestRunner()
# runner.run(suite)
with open(app.PRO_PATH + '/report/report.html','wb') as f:    # jenkins要求文件路径是固定的
    # 创建HTMLTestRunner对象
    runner = HTMLTestRunner(f,title='人力资源管理系统测试报告',description='测试了员工模块的增删改查相关接口')

    # 执行
    runner.run(suite)