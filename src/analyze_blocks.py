def run(entities):
    print("=== 🛵 執行：停等區圖示與圖塊辨識模組 (自動圖層偵測版) ===")
    
    # 定義目標特徵
    target_prefix = '026'
    target_keyword = '機車停等區'
    
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

    # 抓取聚合線外框與機車圖塊
    blocks = [e for e in layer_items if e.dxftype == 'INSERT']
    polylines = [e for e in layer_items if e.dxftype == 'LWPOLYLINE']
    
    print(f"✅ 已偵測到符合圖層：{', '.join(found_layers)}")
    print(f"📊 共找到 {len(layer_items)} 個物件。")
    print(f"   其中包含 {len(polylines)} 條聚合線框線，以及 {len(blocks)} 個機車圖塊。")
    
    if blocks:
        print("\n  [圖塊資訊範例]")
        for i, b in enumerate(blocks[:2]):
            print(f"  - 圖塊名稱: '{b.name}', 插入座標: {b.insert}")
            
    if polylines:
        print("\n  [框線資訊範例]")
        for i, p in enumerate(polylines[:2]):
            print(f"  - 聚合線框包含 {len(p.points)} 個頂點")
            
    print("-" * 40 + "\n")
