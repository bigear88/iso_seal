以下是根據您提供的內容生成的 GitHub README.md 文件排版：

# iso_seal

印鑑識別作業

## boldseal\red2bold.py

執行方式：

```bash
python red2bold.py -i img_orig.jpg -o img_out.jpg
```

- `img_orig.jpg`: 含有紅色印鑑的文件
- `img_out.jpg`: 框出紅色印鑑之處

## detectorseal 

### 標注訓練圖集

```bash
imglab -c Seal_detector\seal_annotations.xml Seal_detector\Seals
imglab seal_annotations.xml
```

### 利用dlib來訓練一個自紅色印鑑檢測器

```bash
python train_seals_detector.py --xml .\Seal_detector\seal_annotations.xml --detector .\Seal_detector\Sealdetector.svm
```

### 識別紅色印鑑位置

```bash
python test_seals_detector.py --dector .\Seal_detector\Sealdetector.svm --testing .\Seal_detector\Testing
```
