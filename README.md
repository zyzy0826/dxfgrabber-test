# DXF 交通標線分析工具

## 專案目標

本專案旨在透過分析 DXF 繪圖檔，自動識別並統計交通標線資訊，包含圖層盤點、標線分類統計及幾何特徵分析。

## 專案結構

```text
dxfgrabber-test/
├── README.md
├── data/
│   ├── road_markings.dwg
│   └── road_markings.dxf
└── src/
    ├── analyze_arrows.py
    ├── analyze_blocks.py
    ├── analyze_grids.py
    ├── analyze_lines.py
    ├── dxf_inventory.py
    └── main.py
```

## 可提取資訊統計表

透過此工具，您可以從 DXF 檔案中獲得以下資訊：

| 資訊類別 | 子類別 / 詳情 | 來源圖層編號 | 實體類型 | 統計指標 |
| :--- | :--- | :--- | :--- | :--- |
| **圖層資訊** | 圖層名稱、物件分佈 | 所有圖層 | 所有類型 | 數量、實體清單 |
| **行穿線** | 斑馬線段 | 021 | LINE, LWPOLYLINE | 數量、總面積 |
| **箭頭** | 直行、左轉、右轉、複合型 | 029 | LWPOLYLINE | 數量、方向分類 |
| **停止線** | 車道停止線 | 020 | LINE, LWPOLYLINE | 數量、總面積 |
| **機車待轉區** | 待轉區邊界 | 022 | LWPOLYLINE | 數量、總面積 |
| **機車停等區** | 停等區方框 | 024 | LWPOLYLINE | 數量、總面積 |
| **網黃線** | 禁停網格 | 013 | HATCH, LWPOLYLINE | 數量、總面積 |
| **公車停靠** | 公車停靠區標線 | 028 | LWPOLYLINE | 數量、總面積 |

---

## 現有模組說明

### `src/main.py`
主程式進入點，整合各項分析模組。

### `src/dxf_inventory.py`
基礎盤點模組，提供全圖層的物件種類與數量統計。

### `src/analyze_lines.py`
標線統計模組，針對行穿線、停止線、待轉區等進行分類與面積計算。

### `src/analyze_arrows.py`
箭頭幾何分析模組，利用向量外積與頂點數判斷箭頭方向。支援：
- 單向：直行、左轉、右轉
- 複合：直行左轉、直行右轉、左右轉、直行+左右轉

### `src/analyze_grids.py` & `src/analyze_blocks.py`
分別處理網格狀標線與圖塊（INSERT）物件的識別。

---

## 安裝與執行

### 環境需求
- Python 3.13+
- pip

### 安裝套件
```bash
pip install dxfgrabber shapely
```

### 執行分析
```bash
python src/main.py
```
