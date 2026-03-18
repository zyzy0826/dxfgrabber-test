def run(entities):
    print("=== 🛵 執行：停等區圖示與圖塊辨識模組 ===")
    target_layer = ' 026機車停等區(白)'
    
    layer_items = [e for e in entities if getattr(e, 'layer', '') == target_layer]
    
    # 在 DXF 結構中，插入的圖塊 (如機車圖示) 稱為 'INSERT'
    blocks = [e for e in layer_items if e.dxftype == 'INSERT']
    lines = [e for e in layer_items if e.dxftype == 'LINE']
    
    print(f"機車停等區圖層內，包含 {len(lines)} 條外部框線，以及 {len(blocks)} 個圖塊(圖示)。")
    
    for i, b in enumerate(blocks[:2]):
        print(f"  - 發現圖塊名稱: '{b.name}'，插入座標: {b.insert}")
        
    print("-" * 40 + "\n")