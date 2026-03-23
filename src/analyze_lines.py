import math
from shapely.geometry import Polygon

def run(entities):
    print("=== 🚦 執行：道路標線分類統計模組 ===")
    
    # 定義類別與其對應的圖層編號前綴
    categories = {
        "行穿線": "021",
        "停止線": "020",
        "機車待轉區": "022",
        "機車停等區": "024",
        "網黃線": "013",
        "公車停靠": "028"
    }
    
    # 統計結果：數量與總面積
    stats = {cat: {"數量": 0, "總面積": 0.0} for cat in categories}
    
    for entity in entities:
        layer = getattr(entity, 'layer', '')
        
        # 尋找匹配的類別
        matched_cat = None
        for cat, prefix in categories.items():
            if layer.startswith(prefix):
                matched_cat = cat
                break
        
        if matched_cat:
            stats[matched_cat]["數量"] += 1
            
            # 如果是多邊形 (LWPOLYLINE)，計算面積
            if entity.dxftype == 'LWPOLYLINE':
                pts = [(p[0], p[1]) for p in entity.points]
                if len(pts) >= 3:
                    try:
                        poly = Polygon(pts)
                        if not poly.is_valid:
                            poly = poly.buffer(0)
                        stats[matched_cat]["總面積"] += poly.area
                    except Exception:
                        pass
    
    print("\n📊 【標線分類統計結果】")
    print(f"{'項目':<12} | {'數量':<6} | {'總面積':<12}")
    print("-" * 35)
    for cat, data in stats.items():
        count = data["數量"]
        area = data["總面積"]
        print(f"{cat:<10} | {count:<6} | {area:.2f} 平方單位")
    
    print("-" * 40 + "\n")
