import cv2
import numpy as np
import argparse

def process_image(input_path, output_path):
    # 讀取原始影像
    original_image = cv2.imread(input_path)
    if original_image is None:
        raise ValueError(f"無法讀取檔案: {input_path}")

    # 複製原始影像以進行處理
    image = original_image.copy()

    # 轉換為HSV色彩空間
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 根據直方圖分析調整紅色範圍
    lower_red1 = np.array([0, 20, 180])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([160, 20, 180])
    upper_red2 = np.array([180, 255, 255])

    # 創建紅色遮罩
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # 使用形態學操作改善結果
    kernel = np.ones((2,2), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # 將紅色轉為黑色，其他轉為白色
    result = np.full_like(image, 255)
    result[red_mask > 0] = [0, 0, 0]

    # 轉換為灰度圖
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # 使用閾值處理突出文字
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 找到輪廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 創建一個全白的遮罩
    mask = np.full(original_image.shape[:2], 255, dtype=np.uint8)

    # 在原圖上標記文字區域，並在遮罩上填充文字區域
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # 過濾太小的區域
        if w * h > 100:  # 可以調整這個閾值
            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(mask, (x, y), (x + w, y + h), 0, -1)

    # 使用遮罩將原始圖像中的文字區域保留，其他區域變為白色
    result = original_image.copy()
    result[mask == 255] = [255, 255, 255]

    # 保存結果
    cv2.imwrite(output_path, result)
    print(f"output result: {output_path}")

def main():
    # 建立參數解析器
    parser = argparse.ArgumentParser(description='Text detection and masking')
    parser.add_argument('-i', '--input', required=True, help='input path')
    parser.add_argument('-o', '--output', required=True, help='output path')
    
    # 解析命令列參數
    args = parser.parse_args()
    
    try:
        process_image(args.input, args.output)
    except Exception as e:
        print(f"error : {str(e)}")

if __name__ == "__main__":
    main()
