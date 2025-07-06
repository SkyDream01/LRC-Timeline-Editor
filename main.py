# main.py
import sys
from PySide6.QtWidgets import QApplication
# 从 main_window.py 导入 resource_path 函数
from main_window import MainWindow, resource_path 

if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        # 使用 resource_path 获取 styles.qss 的正确路径
        qss_path = resource_path('styles.qss')
        with open(qss_path, 'r', encoding='utf-8') as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Warning: styles.qss not found. Using default application style.")

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())