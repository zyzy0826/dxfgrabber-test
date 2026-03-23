def run(entities):
    print("=== 🟨 執行：網狀線與複雜填充區分析模組 (自動圖層偵測版) ===")
    
    # 定義目標特徵
    target_prefix = '013'
    target_keyword = '網狀線'
    
    # 自動篩選符合條件的圖層物件
    layer_items = [
        e for e in entities 
        if getattr(e, 'layer', '').startswith(target_prefix) or target_keyword in getattr(e, 'layer', '')
    ]
    
    # 取得實際命中的圖層名稱清單
    found_layers = sorted(list(set(getattr(e, 'layer', '') for e in layer_items)))
    
    if not layer_items:
        print(f"⚠️  警告：在圖檔中找不到編號 '{target_prefix}' 或名稱包含 '{target_keyword}' 的圖層。")
        return

    # 抓取填充線與聚合線邊框
    hatches = [e for e in layer_items if e.dxftype == 'HATCH']
    polylines = [e for e in layer_items if e.dxftype == 'LWPOLYLINE']
    
    print(f"✅ 已偵測到符合圖層：{', '.join(found_layers)}")
    print(f"📊 在這些圖層中，共找到 {len(layer_items)} 個物件。")
    print(f"   包含 {len(hatches)} 個填充區域(HATCH)，以及 {len(polylines)} 條聚合線邊框(LWPOLYLINE)。")
    
    if hatches:
        print("\n  [填充線資訊範例]")
        for i, h in enumerate(hatches[:2]):
            print(f"  - 填充區域 {i+1}，顏色代碼: {h.color}")
            
    if polylines:
        print("\n  [邊框資訊範例]")
        for i, p in enumerate(polylines[:2]):
            print(f"  - 邊框包含 {len(p.points)} 個頂點")
            
    print("-" * 40 + "\n")
