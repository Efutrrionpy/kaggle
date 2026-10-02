# 重現範圍與命令

## 三種不同的重現

1. **重建最後策略：完整提供。** `strategies/` 含原上傳所有檔案，兩個策略只依賴
   Python標準函式庫與隨附政策JSON。不用私人路徑、網路或外部模型權重。
2. **重新計算公開結果表：完整提供。** `results/*_cells.json` 是研究生成的逐場
   精簡結果；`tools/recompute_tables.py` 可重新計算世界／對手／座位分組分數。
3. **完整重跑原比較：本地保留，不在公開包虛稱一鍵完整。** 某些對手來源沒有足以
   再散布的授權，完整官方回放也不放入公開包。所有原始來源、固定plan、程式與重要
   最後批次軌跡留在本地。公開包提供來源指紋、種子／座位與結果；沒有那些對手時，
   不能把自對弈或random對手當成原論文式比較的重現。

## 環境

原研究：Linux x86_64、CPython3.11.15、`kaggle-environments==1.32.7`。
原壓縮封裝使用zlib1.3.1；若Python／zlib不同，tar成員相同仍可能得到不同gzip位元。
重建工具同時检查成員hash與原壓縮包hash，不悄悄接受不同的正式提交。
正式策略推論本身不用 NumPy、GPU、Kaggle套件或API登入。

以下從本公開包根目錄執行：

```sh
python3.11 tools/verify.py
python3.11 tools/rebuild_submissions.py --output /tmp/kaggriculture-rebuilt
python3.11 tools/recompute_tables.py
```

輸出資料夾必須尚未存在；命令不覆蓋已有成果、不提交到Kaggle。
本次封存實際使用原環境重建並匹配兩個原壓縮包，結果見 `results/archive_checks.json`。

## 推論介面

每一行輸入是官方 observation 和 configuration，標準輸出每行一個動作JSON：

```sh
python3.11 -I -S strategies/flex_service/main.py < requests.jsonl > actions.jsonl
python3.11 -I -S strategies/adaptive_milk/main.py < requests.jsonl > actions.jsonl
```

`requests.jsonl` 由自己的合法本地模擬產生，不是本包藏有的評估資料。
策略在step0重設實例；不要把两個策略匯入同一全域模組名稱空間混用。
可用官方引擎建立本地對局，但這會是新的測試，不是既有成績證據。

```sh
python3.11 -m venv /tmp/kaggriculture-env
/tmp/kaggriculture-env/bin/pip install kaggle-environments==1.32.7
```

欲取得公開示範或官方自己提交的驗證回放，可在遵守Kaggle規則及自己的帳號權限下使用
官方CLI `kaggle competitions replay EPISODE_ID`。官方部署核對episode：Flex115743049、
Adaptive115611747。示範來源與hash另見 `manifests/source_provenance.json`；
取得的回放不是推論時的依賴，也不要將對手private觀察輸入策略。

## 大型本地成果與清理

最終封裝、被選政策的重現閉包、官方來源、原設計、結果與重要失败案例保留本地。
未提交 NativeDeadlines／Committed 的封裝與指紋也保留，不冒稱它們是正式提交。
不再需要的生成軌跡已依逐項清單刪除，保留每方法／對手／座位／勝負的極端代表；
完整分數、seed、配置與程式未刪。大量舊逐場plan是母計畫加上五個逐場選擇欄位；
清理前已逐項產生完全相同的位元組並核對SHA256，保留母計畫、選擇欄位、hash及
本地 `archive_cleanup_20261002.py restore-plans --path ...` 重建命令後，才刪除副本。
不是改寫實驗或移除hash檢查。重建被刪對局軌跡仍要重新計算，並非從回收桶還原。

清理完整收據留在工作站 `publication/cleanup_receipt_20261002.json`，不放進公開包，
因其中包含工作站路徑與程序資訊。公開包的 `SHA256SUMS` 是檔案完整性清單，不是
數位簽章、最終獎牌認證或第三方授權的替代品。
