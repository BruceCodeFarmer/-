# 资金管理APP

## 公告
此Python APP程序遇到了一个小问题，控制台进行了警告，不影响正常使用

警告内容如下：

```
E:\...\ui.py:167: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
  self.income_expense = pd.concat([self.income_expense, new_row], ignore_index=True)
```

希望如果有大佬看见可以指点


## 说明
此应用为测试版本阶段，后续会进一步修复所有bug。

应用是**需要输入激活码**制的，完整版本请关注CSDN账号并获得激活码，输入后可以体验到完整版本。

因为功能尚未完全，并没有实现pyinstaller exe文件，请安装好环境后再使用。

如果发现共享激活码和**私自更改**破解版本的，视为侵犯版权，请自重。

CSDN账户链接：https://blog.csdn.net/B20111003

目前实现功能：



* **收入支出记录：**
    * **自定义收入和支出类别：工资、奖金、房租、水电费、购物等。**
    * 支持批量导入数据：从银行对账单、信用卡账单等导入数据。
    * 设置提醒：提醒定期账单的到期日。
* **预算管理：**
    * 设置月度、季度或年度预算。
    * 跟踪实际支出与预算的对比。
    * 自动生成预算分析报告。
* **资产负债管理：**
    * **记录各种资产（房产、车辆、股票等）和负债（贷款、信用卡欠款）。**
    * **计算净资产。**
* **投资管理：**
    * 记录投资收益和亏损。
    * 支持多种投资类型：股票、基金、债券等。
* **报表生成：**
    * **生成自定义的财务报表，如收入支出明细表、资产负债表、现金流量表等。**
    * **支持导出数据为Excel、PDF等格式。**

## 版本更新
### alpha 测试版
#### 1.0.240815.1
2024/08/15版本更新！
首次APP登录Github
激活码自取，大部分功能正常，后续会改进！
#### 1.0.240815.2
版本更新！
加入保留激活状态的代码
暂无bug
#### 1.0.240815.3
版本更新！
加入自动化收支分析功能
解决了几个小问题
暂无bug
#### 1.0.240816.4
版本更新！
全局UI更改！
解决了几个小问题
加入了更加详细的日志输出和log文件

## 版权
CopyRight BruceHanzi和名下小工作室NewSight & NAC Studio开发制作
使用软件python
