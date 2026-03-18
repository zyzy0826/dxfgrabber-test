import dxfgrabber
import analyze_lines
import analyze_arrows
import analyze_blocks
import analyze_grids

def main():
    # 設定檔案路徑 (假設執行時的終端機位在 src 資料夾或專案根目錄)
    file_path = "../data/road_markings.dxf" 
    
    print("正在讀取 DXF 檔案...")
    try:
        dxf = dxfgrabber.readfile(file_path)
        print(f"✅ 成功讀取！DXF 版本: {dxf.dxfversion}，總物件數: {len(dxf.entities)}\n")
    except IOError:
        print(f"❌ 找不到檔案，請確認 {file_path} 是否存在。")
        return
    except Exception as e:
        print(f"❌ 讀取發生錯誤: {e}")
        return

    # 取得圖面上的所有物件清單
    all_entities = dxf.entities

    # 依序執行各個分析模組
    analyze_lines.run(all_entities)
    analyze_arrows.run(all_entities)
    analyze_blocks.run(all_entities)
    analyze_grids.run(all_entities)

if __name__ == "__main__":
    main()