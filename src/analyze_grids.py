def run(entities):
    print("=== 🟨 執行：網狀線與複雜填充區分析模組 ===")
    
    # 使用你找到的精確圖層名稱
    target_layer = '013網狀線(黃)'
    layer_items = [e for e in entities if getattr(e, 'layer', '') == target_layer]
    
    # 抓取填充線與聚合線邊框
    hatches = [e for e in layer_items if e.dxftype == 'HATCH']
    polylines = [e for e in layer_items if e.dxftype == 'LWPOLYLINE']
    
    print(f"在 '{target_layer}' 圖層中，共找到 {len(layer_items)} 個物件。")
    print(f"包含 {len(hatches)} 個填充區域(HATCH)，以及 {len(polylines)} 條聚合線邊框(LWPOLYLINE)。")
    
    if hatches:
        print("\n  [填充線資訊範例]")
        for i, h in enumerate(hatches[:2]):
            print(f"  - 填充區域 {i+1}，顏色代碼: {h.color}")
            
    if polylines:
        print("\n  [邊框資訊範例]")
        for i, p in enumerate(polylines[:2]):
            print(f"  - 邊框包含 {len(p.points)} 個頂點")
            
    print("-" * 40 + "\n")