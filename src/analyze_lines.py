def run(entities):
    print("=== 🚦 執行：一般標線與停止線分析 ===")
    target_layers = ['021行穿線(白)', '020停止線(白)']
    
    # 篩選出目標圖層內的「直線 (LINE)」物件
    lines = [e for e in entities if getattr(e, 'layer', '') in target_layers and e.dxftype == 'LINE']
    
    print(f"在行穿線與停止線圖層中，共找到 {len(lines)} 條獨立線段。")
    
    if lines:
        # 收集這些線段使用的顏色代碼 (256 通常代表 ByLayer)
        colors = set([e.color for e in lines])
        print(f"這些線段使用的顏色代碼包含: {colors}")
        
        # 印出第一條線的座標當範例
        first_line = lines[0]
        print(f"[範例] 第一條線段起點: {first_line.start}, 終點: {first_line.end}")
        
    print("-" * 40 + "\n")