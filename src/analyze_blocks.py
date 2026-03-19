def run(entities):
    print("=== 🛵 執行：停等區圖示與圖塊辨識模組 ===")
    target_layer = '026機車停等區(白)'
    layer_items = [e for e in entities if getattr(e, 'layer', '') == target_layer]
    
    # 抓取聚合線外框與機車圖塊
    blocks = [e for e in layer_items if e.dxftype == 'INSERT']
    polylines = [e for e in layer_items if e.dxftype == 'LWPOLYLINE']
    
    print(f"在 '{target_layer}' 圖層中，共找到 {len(layer_items)} 個物件。")
    print(f"其中包含 {len(polylines)} 條聚合線框線，以及 {len(blocks)} 個機車圖塊。")
    
    if blocks:
        print("\n  [圖塊資訊範例]")
        for i, b in enumerate(blocks[:2]):
            print(f"  - 圖塊名稱: '{b.name}', 插入座標: {b.insert}")
            
    if polylines:
        print("\n  [框線資訊範例]")
        for i, p in enumerate(polylines[:2]):
            print(f"  - 聚合線框包含 {len(p.points)} 個頂點")
            
    print("-" * 40 + "\n")