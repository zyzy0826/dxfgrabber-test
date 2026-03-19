import math

def calculate_cross_product(x1, y1, x2, y2, x3, y3):
    """計算向量外積，用來判斷點在直線的左邊還是右邊"""
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

def run(entities):
    print("=== ⬆️ 執行：指向線箭頭計算模組 (特徵與向量升級版) ===")
    
    target_layer = '029指向線(白)'
    layer_items = [e for e in entities if getattr(e, 'layer', '') == target_layer]
    polylines = [e for e in layer_items if e.dxftype == 'LWPOLYLINE']
    
    counts = {"直行": 0, "倒轉": 0, "左轉": 0, "右轉": 0, "複合": 0, "未知": 0}
    
    for p in polylines:
        pts = [(pt[0], pt[1]) for pt in p.points]
        num_pts = len(pts)
        
        if num_pts < 3:
            continue
            
        # 1. 第一層防護：利用頂點數量抓出「複合箭頭」
        # 從剛才的 log 得知複合箭頭高達 15 個頂點
        if num_pts >= 14:
            counts["複合"] += 1
            continue

        # 2. 第二層防護：找出箭頭的主幹 (最長的那條直線)
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
                
        # 判斷主幹的大方向 (Y軸往上為正)
        dy = stem_end[1] - stem_start[1]
        is_pointing_up = dy > 0  # 簡單判斷是順向還是逆向車道
                
        # 3. 判斷直行或轉彎
        # 頂點數較少 (例如 11 以下) 通常是單純直行箭頭
        if num_pts <= 9:
            if is_pointing_up:
                counts["直行"] += 1
            else:
                counts["倒轉"] += 1
            continue
            
        # 4. 處理轉彎箭頭 (頂點數約 10~13)
        # 尋找離主幹最遠的那個「尖端點」
        max_perp_dist = -1
        farthest_point = None
        
        for pt in pts:
            if pt == stem_start or pt == stem_end:
                continue
            # 利用外積計算點到直線的垂直距離比例
            cross_val = calculate_cross_product(stem_start[0], stem_start[1], stem_end[0], stem_end[1], pt[0], pt[1])
            perp_dist = abs(cross_val) / max_dist
            if perp_dist > max_perp_dist:
                max_perp_dist = perp_dist
                farthest_point = pt
                
        # 利用外積的正負號，一秒判定左右轉 (無視馬路旋轉角度)
        if farthest_point:
            final_cross = calculate_cross_product(stem_start[0], stem_start[1], stem_end[0], stem_end[1], farthest_point[0], farthest_point[1])
            
            if final_cross > 0:
                counts["左轉"] += 1
            elif final_cross < 0:
                counts["右轉"] += 1
            else:
                counts["未知"] += 1

    print(f"在 '{target_layer}' 圖層中，共處理了 {len(polylines)} 個多邊形箭頭。")
    print("\n📊 【箭頭方向統計結果】")
    for dir_name, count in counts.items():
        print(f"  - {dir_name} 箭頭: {count} 個")
        
    print("-" * 40 + "\n")