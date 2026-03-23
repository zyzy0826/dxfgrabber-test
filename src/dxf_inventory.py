import dxfgrabber
from shapely.geometry import Polygon

def run_inventory(file_path):
    print(f"🔍 正在對圖檔進行全盤點掃描：{file_path} ...\n")
    dxf = dxfgrabber.readfile(file_path)
    
    # 建立一個大字典來存放盤點資料
    # 結構: { '圖層名稱': { '材質(形狀)': {'數量': 0, '總面積': 0.0} } }
    inventory = {}
    
    for entity in dxf.entities:
        # 1. 取得圖層名稱
        layer = getattr(entity, 'layer', '未知圖層')
        
        # 2. 取得材質 (實體類型 dxftype)
        shape_type = entity.dxftype
        
        # 初始化字典結構
        if layer not in inventory:
            inventory[layer] = {}
        if shape_type not in inventory[layer]:
            inventory[layer][shape_type] = {'數量': 0, '總面積': 0.0}
            
        # 數量 +1
        inventory[layer][shape_type]['數量'] += 1
        
        # 3. 計算面積 (針對能算面積的材質)
        if shape_type == 'LWPOLYLINE':
            pts = [(p[0], p[1]) for p in entity.points]
            # 至少要 3 個頂點才能構成多邊形並計算面積
            if len(pts) >= 3:
                poly = Polygon(pts)
                # 預防圖形畫歪導致自我交叉，用 buffer(0) 自動修復
                if not poly.is_valid:
                    poly = poly.buffer(0)
                inventory[layer][shape_type]['總面積'] += poly.area
                
        elif shape_type == 'CIRCLE':
            import math
            inventory[layer][shape_type]['總面積'] += math.pi * (entity.radius ** 2)

    # 4. 印出漂漂亮亮的盤點報告
    print("================ 📊 DXF 圖層與材質盤點報告 ================")
    
    # 按照圖層名稱排序印出
    for layer_name in sorted(inventory.keys()):
        print(f"📂 圖層: 【{layer_name}】")
        
        for shape_type, data in inventory[layer_name].items():
            count = data['數量']
            total_area = data['總面積']
            
            # 判斷這個材質是不是能算面積的
            if shape_type in ['LWPOLYLINE', 'CIRCLE']:
                # 把面積四捨五入到小數點後兩位
                print(f"   ├── 材質: {shape_type:<12} | 數量: {count:<5} | 總面積: {total_area:.2f} 平方單位")
            elif shape_type in ['LINE', 'ARC', 'POINT']:
                print(f"   ├── 材質: {shape_type:<12} | 數量: {count:<5} | (線段無面積)")
            else:
                print(f"   ├── 材質: {shape_type:<12} | 數量: {count:<5} | (複雜圖塊/無法直接計算)")
                
        print("-" * 60)

if __name__ == "__main__":
    # 直接執行這支檔案測試看看
    run_inventory("../data/road_markings.dxf")