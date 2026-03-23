import math

def calculate_cross_product(x1, y1, x2, y2, x3, y3):
    """計算向量外積，用來判斷點在直線的左邊還是右邊"""
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

def run(entities):
    print("=== ⬆️ 執行：指向線箭頭計算模組 (自動圖層偵測版) ===")
    
    # 定義目標特徵
    target_prefix = '029'
    target_keyword = '指向線'
    
    # 自動篩選符合條件的圖層物件
    layer_items = [
        e for e in entities 
        if getattr(e, 'layer', '').startswith(target_prefix) or target_keyword in getattr(e, 'layer', '')
    ]
    
    # 取得實際命中的圖層名稱清單（供顯示用）
    found_layers = sorted(list(set(getattr(e, 'layer', '') for e in layer_items)))
    
    if not layer_items:
        print(f"⚠️  警告：在圖檔中找不到編號 '{target_prefix}' 或名稱包含 '{target_keyword}' 的圖層。")
        return

    polylines = [e for e in layer_items if e.dxftype == 'LWPOLYLINE']
    
    print(f"✅ 已偵測到符合圖層：{', '.join(found_layers)}")
    print(f"📊 在這些圖層中，共處理了 {len(polylines)} 個多邊形箭頭。")
    
    counts = {
        "直行": 0, 
        "左轉": 0, 
        "右轉": 0, 
        "直行左轉": 0, 
        "直行右轉": 0, 
        "左右轉": 0, 
        "直行+左右轉": 0,
        "未知": 0
    }
    
    for p in polylines:
        pts = [(pt[0], pt[1]) for pt in p.points]
        num_pts = len(pts)
        
        if num_pts < 3:
            continue
            
        # 找出主幹 (最長的那條直線)
        max_dist = 0
        stem_start, stem_end = pts[0], pts[1]
        for i in range(num_pts):
            p1 = pts[i]
            p2 = pts[(i+1) % num_pts]
            dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            if dist > max_dist:
                max_dist = dist
                stem_start = p1
                stem_end = p2
        
        # 判斷主幹方向
        dy = stem_end[1] - stem_start[1]
        is_pointing_up = dy > 0

        # 計算所有點相對於主幹的外積
        cross_values = [calculate_cross_product(stem_start[0], stem_start[1], stem_end[0], stem_end[1], pt[0], pt[1]) for pt in pts]
        
        has_left = any(cv > 1.0 for cv in cross_values)   # 閾值 1.0 避免浮點誤差
        has_right = any(cv < -1.0 for cv in cross_values)
        
        # 根據頂點數量與分佈進行分類
        if num_pts <= 9:
            counts["直行"] += 1
        elif num_pts >= 14:
            # 複合箭頭判斷
            if has_left and has_right:
                if num_pts > 15:
                    counts["直行+左右轉"] += 1
                else:
                    counts["左右轉"] += 1
            elif has_left:
                counts["直行左轉"] += 1
            elif has_right:
                counts["直行右轉"] += 1
            else:
                counts["未知"] += 1
        else:
            # 單一轉彎箭頭
            if has_left:
                counts["左轉"] += 1
            elif has_right:
                counts["右轉"] += 1
            else:
                counts["直行"] += 1

    print("\n📊 【箭頭方向統計結果】")
    for dir_name, count in counts.items():
        print(f"  - {dir_name} 箭頭: {count} 個")
        
    print("-" * 40 + "\n")
