def run(entities):
    print("=== ⬆️ 執行：指向線箭頭計算模組 ===")
    target_layer = '029指向線(白)'
    
    # 找出該圖層的所有物件
    layer_items = [e for e in entities if getattr(e, 'layer', '') == target_layer]
    
    # 箭頭通常是由連續折線/多邊形 (LWPOLYLINE) 構成
    polylines = [e for e in layer_items if e.dxftype == 'LWPOLYLINE']
    
    print(f"在 {target_layer} 圖層中，共找到 {len(layer_items)} 個物件。")
    print(f"其中包含 {len(polylines)} 個聚合線(多邊形)圖形。")
    
    # 列出前三個圖形的頂點數量，可作為後續計算面積或分辨左右轉箭頭的基礎
    for i, p in enumerate(polylines[:3]):
        print(f"  - 箭頭形狀 {i+1} 包含了 {len(p.points)} 個頂點")
        
    print("-" * 40 + "\n")