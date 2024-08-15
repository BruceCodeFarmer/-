import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel,
    QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox, QDialog, QFormLayout,
    QDialogButtonBox
)
import matplotlib.pyplot as plt
import os


class FinanceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isActivate = self.check_activation_status()
        self.code = "sk-bh-maap2408153921037524181615203537"
        self.data = pd.DataFrame(columns=["日期", "类别", "收入", "支出", "备注"])
        self.assets = pd.DataFrame(columns=["资产名称", "类型", "价值"])
        self.liabilities = pd.DataFrame(columns=["负债名称", "类型", "金额"])
        self.investments = pd.DataFrame(columns=["投资名称", "类型", "收益", "亏损"])
        self.budgets = pd.DataFrame(columns=["周期", "预算金额", "实际支出", "差异"])
        self.reminders = pd.DataFrame(columns=["项目", "到期日", "金额"])
        self.initUI()

        if not self.isActivate:
            self.activateFeatures()
        else:
            QMessageBox.information(self, "提示", "功能已激活，无需重复激活。")

    def initUI(self):
        self.setWindowTitle('资金管理系统')
        self.setGeometry(100, 100, 1000, 800)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)

        self.label = QLabel('欢迎使用资金管理系统', self)
        self.mainLayout.addWidget(self.label)

        # 添加收入/支出记录
        self.addIncomeExpenseButton = QPushButton('添加收入/支出记录', self)
        self.addIncomeExpenseButton.clicked.connect(self.addIncomeExpense)
        self.mainLayout.addWidget(self.addIncomeExpenseButton)

        # 批量导入数据
        self.importButton = QPushButton('导入数据', self)
        self.importButton.clicked.connect(self.importData)
        self.mainLayout.addWidget(self.importButton)

        # 设置预算
        self.budgetButton = QPushButton('设置预算', self)
        self.budgetButton.clicked.connect(self.setBudget)
        self.mainLayout.addWidget(self.budgetButton)

        # 管理资产负债
        self.assetLiabilityButton = QPushButton('资产负债管理', self)
        self.assetLiabilityButton.clicked.connect(self.manageAssetsLiabilities)
        self.mainLayout.addWidget(self.assetLiabilityButton)

        # 投资管理
        self.investmentButton = QPushButton('投资管理', self)
        self.investmentButton.clicked.connect(self.manageInvestments)
        self.mainLayout.addWidget(self.investmentButton)

        # 生成报表
        self.reportButton = QPushButton('生成报表', self)
        self.reportButton.clicked.connect(self.generateReport)
        self.mainLayout.addWidget(self.reportButton)

        # 设置提醒
        self.reminderButton = QPushButton('设置提醒', self)
        self.reminderButton.clicked.connect(self.setReminder)
        self.mainLayout.addWidget(self.reminderButton)

        # 激活功能
        self.activateButton = QPushButton('激活功能', self)
        self.activateButton.clicked.connect(self.activateFeatures)
        self.mainLayout.addWidget(self.activateButton)

        # 数据表格
        self.tableWidget = QTableWidget(self)
        self.mainLayout.addWidget(self.tableWidget)

    def check_activation_status(self):
        """ 检查激活状态 """
        if os.path.exists("status.txt"):
            with open("status.txt", "r") as f:
                status = f.read().strip()
                return status == "true"
        return False

    def activateFeatures(self):
        """ 激活功能 """
        if self.isActivate:
            QMessageBox.information(self, "提示", "功能已激活，无需重复激活。")
            return
        try:
            code, ok = QInputDialog.getText(self, "激活功能", "请输入激活码:")
            if ok and code:
                if self.verifyActivationCode(code):
                    self.isActivate = True
                    with open("status.txt", "w") as f:
                        f.write("true")
                    QMessageBox.information(self, "激活成功", "激活成功，您现在可以使用所有功能。")
                else:
                    QMessageBox.warning(self, "激活失败", "激活码错误，请重试。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"激活功能时发生错误: {e}")

    def verifyActivationCode(self, code):
        return code == self.code

    def addIncomeExpense(self):
        try:
            form, ok = self.openFormDialog("收入/支出记录", ["日期 (YYYY-MM-DD)", "类别", "收入", "支出", "备注"])
            if ok:
                new_row = pd.DataFrame([form], columns=self.data.columns)
                self.data = pd.concat([self.data, new_row], ignore_index=True)
                self.displayData(self.data)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"添加收入/支出记录时发生错误: {e}")

    def importData(self):
        if not self.isActivate:
            QMessageBox.warning(self, "提示", "请先激活功能以使用此功能。")
            return
        try:
            filePath, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
            if filePath:
                if filePath.endswith('.csv'):
                    data = pd.read_csv(filePath, encoding='utf-8')
                elif filePath.endswith('.xlsx'):
                    data = pd.read_excel(filePath)
                self.data = pd.concat([self.data, data], ignore_index=True)
                self.displayData(self.data)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入数据时发生错误: {e}")

    def setBudget(self):
        if not self.isActivate:
            QMessageBox.warning(self, "提示", "请先激活功能以使用此功能。")
            return
        try:
            form, ok = self.openFormDialog("设置预算", ["周期", "预算金额", "实际支出", "差异"])
            if ok:
                new_row = pd.DataFrame([form], columns=self.budgets.columns)
                self.budgets = pd.concat([self.budgets, new_row], ignore_index=True)
                self.budgets["差异"] = self.budgets["预算金额"].astype(float) - self.budgets["实际支出"].astype(float)
                self.displayData(self.budgets)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置预算时发生错误: {e}")

    def manageAssetsLiabilities(self):
        if not self.isActivate:
            QMessageBox.warning(self, "提示", "请先激活功能以使用此功能。")
            return
        try:
            form, ok = self.openFormDialog("资产负债管理", ["资产名称/负债名称", "类型", "价值/金额", "备注"])
            if ok:
                if form["类型"] == "资产":
                    new_row = pd.DataFrame(
                        [{"资产名称": form["资产名称/负债名称"], "类型": form["类型"], "价值": form["价值/金额"]}],
                        columns=self.assets.columns)
                    self.assets = pd.concat([self.assets, new_row], ignore_index=True)
                elif form["类型"] == "负债":
                    new_row = pd.DataFrame(
                        [{"负债名称": form["资产名称/负债名称"], "类型": form["类型"], "金额": form["价值/金额"]}],
                        columns=self.liabilities.columns)
                    self.liabilities = pd.concat([self.liabilities, new_row], ignore_index=True)
                self.displayData(pd.concat([self.assets, self.liabilities], ignore_index=True))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"管理资产负债时发生错误: {e}")

    def manageInvestments(self):
        if not self.isActivate:
            QMessageBox.warning(self, "提示", "请先激活功能以使用此功能。")
            return
        try:
            form, ok = self.openFormDialog("投资管理", ["投资名称", "类型", "收益", "亏损"])
            if ok:
                new_row = pd.DataFrame([form], columns=self.investments.columns)
                self.investments = pd.concat([self.investments, new_row], ignore_index=True)
                self.displayData(self.investments)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"管理投资时发生错误: {e}")

    def generateReport(self):
        if not self.isActivate:
            QMessageBox.warning(self, "提示", "请先激活功能以使用此功能。")
            return
        try:
            # 示例报表生成
            self.data.to_csv('financial_report.csv', index=False)
            QMessageBox.information(self, "报表生成", "报表已生成并保存为 'financial_report.csv'.")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成报表时发生错误: {e}")

    def setReminder(self):
        if not self.isActivate:
            QMessageBox.warning(self, "提示", "请先激活功能以使用此功能。")
            return
        try:
            form, ok = self.openFormDialog("设置提醒", ["项目", "到期日 (YYYY-MM-DD)", "金额"])
            if ok:
                new_row = pd.DataFrame([form], columns=self.reminders.columns)
                self.reminders = pd.concat([self.reminders, new_row], ignore_index=True)
                self.displayData(self.reminders)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置提醒时发生错误: {e}")

    def openFormDialog(self, title, fields):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QFormLayout(dialog)
        inputs = {}
        for field in fields:
            line_edit = QLineEdit(dialog)
            inputs[field] = line_edit
            layout.addRow(QLabel(field, dialog), line_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        layout.addWidget(button_box)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return {field: line_edit.text() for field, line_edit in inputs.items()}, True
        return None, False

    def displayData(self, df):
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FinanceManager()
    window.show()
    sys.exit(app.exec_())
