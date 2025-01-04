# 導入必要的套件
from imutils import paths
import argparse
import dlib
import cv2
import os
from datetime import datetime

# 構建參數解析器並解析參數
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required=True, help="訓練好的物件偵測器路徑")
ap.add_argument("-t", "--testing", required=True, help="測試圖片目錄路徑")
args = vars(ap.parse_args())

# 載入偵測器
detector = dlib.simple_object_detector(args["detector"])

# 確保 output 資料夾存在
output_dir = ".\seal_detector\output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 創建報告檔案名稱
report_filename = f"report_{datetime.now().strftime('%y%m%d')}.txt"
report_path = os.path.join(output_dir, report_filename)

# 開啟報告檔案
with open(report_path, 'w') as report_file:
    # 遍歷測試圖片
    for testingPath in paths.list_images(args["testing"]):
        # 載入圖片並進行預測
        image = cv2.imread(testingPath)
        boxes = detector(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # 遍歷邊界框並繪製
        for b in boxes:
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)

        # 生成輸出檔案名稱
        base_name = os.path.basename(testingPath)
        output_filename = f"output_{base_name}"
        output_path = os.path.join(output_dir, output_filename)

        # 儲存圖片
        cv2.imwrite(output_path, image)
        print(f"已儲存圖片：{output_path}")

        # 寫入報告
        result = "found seal" if boxes else "not found seal"
        report_file.write(f"{base_name} {result}\n")

print(f"檢測報告已儲存：{report_path}")
