import dxfgrabber
from shapely.geometry import Polygon

def run_inventory(file_path):
    print(f"🔍 正在對圖檔進行全盤點掃描：{file_path} ...\n")
    dxf = dxfgrabber.readfile(file_path)
    
    # 建立一個大字典來存放盤點資料
    # 結構: { '圖層名稱': { '材質(形狀)': { '顏色(代碼)': {'數量': 0, '總面積': 0.0} } } }
    inventory = {}
    
    for entity in dxf.entities:
        # 1. 取得圖層名稱
        layer = getattr(entity, 'layer', '未知圖層')
        
        # 2. 取得材質 (實體類型 dxftype)
        shape_type = entity.dxftype
        
        # 3. 取得顏色 (0-255 為索引色, 256 為 ByLayer, 0 為 ByBlock)
        color = getattr(entity, 'color', 256)
        color_str = f"Color {color}" if color != 256 else "ByLayer"
        
        # 初始化字典結構
        if layer not in inventory:
            inventory[layer] = {}
        if shape_type not in inventory[layer]:
            inventory[layer][shape_type] = {}
        if color_str not in inventory[layer][shape_type]:
            inventory[layer][shape_type][color_str] = {'數量': 0, '總面積': 0.0}
            
        # 數量 +1
        inventory[layer][shape_type][color_str]['數量'] += 1
        
        # 4. 計算面積 (針對能算面積的材質)
        area = 0.0
        if shape_type == 'LWPOLYLINE':
            pts = [(p[0], p[1]) for p in entity.points]
            if len(pts) >= 3:
                poly = Polygon(pts)
                if not poly.is_valid:
                    poly = poly.buffer(0)
                area = poly.area
                
        elif shape_type == 'CIRCLE':
            import math
            area = math.pi * (entity.radius ** 2)
            
        inventory[layer][shape_type][color_str]['總面積'] += area

    # 5. 印出漂漂亮亮的盤點報告
    print("================ 📊 DXF 圖層、材質與顏色盤點報告 ================")
    
    # 按照圖層名稱排序印出
    for layer_name in sorted(inventory.keys()):
        print(f"📂 圖層: 【{layer_name}】")
        
        for shape_type in sorted(inventory[layer_name].keys()):
            for color_name, data in inventory[layer_name][shape_type].items():
                count = data['數量']
                total_area = data['總面積']
                
                # 判斷這個材質是不是能算面積的
                if shape_type in ['LWPOLYLINE', 'CIRCLE']:
                    print(f"   ├── 材質: {shape_type:<12} | 顏色: {color_name:<10} | 數量: {count:<5} | 總面積: {total_area:.2f} 平方單位")
                elif shape_type in ['LINE', 'ARC', 'POINT']:
                    print(f"   ├── 材質: {shape_type:<12} | 顏色: {color_name:<10} | 數量: {count:<5} | (線段無面積)")
                else:
                    print(f"   ├── 材質: {shape_type:<12} | 顏色: {color_name:<10} | 數量: {count:<5} | (複雜圖塊/無法直接計算)")
                
        print("-" * 60)

if __name__ == "__main__":
    # 直接執行這支檔案測試看看
    run_inventory("../data/road_markings.dxf")