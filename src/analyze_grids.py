def run(entities):
    print("=== 🟨 執行：網狀線與複雜填充區分析模組 ===")
    target_layer = '013網狀線(黃)'
    
    layer_items = [e for e in entities if getattr(e, 'layer', '') == target_layer]
    
    # 區分填充 (HATCH) 與 邊框 (LINE / LWPOLYLINE)
    hatches = [e for e in layer_items if e.dxftype == 'HATCH']
    boundaries = [e for e in layer_items if e.dxftype in ['LINE', 'LWPOLYLINE']]
    
    print(f"在 {target_layer} 中，找到 {len(hatches)} 個填充區域，以及 {len(boundaries)} 條邊框線。")
    
    if hatches:
        print("  - 偵測到網狀線使用了 HATCH (填充) 屬性來繪製")
        
    if boundaries:
        colors = set([e.color for e in boundaries])
        print(f"  - 邊框線顏色代碼包含: {colors}")
        
    print("-" * 40 + "\n")