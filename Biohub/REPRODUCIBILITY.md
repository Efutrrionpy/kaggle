# 重現說明與邊界

本包是可審查的研究封存，不是可一鍵重訓所有模型的 winning solution。不要把 runtime parity、visible CSV checksum、本地 exposed graph score 與官方 hidden Private 分數混為一談。

## 1. 不需比賽資料的檢查

在本資料夾執行：

```sh
python3 tools/verify_archive.py
python3 -m venv .repro-venv
.repro-venv/bin/pip install -r requirements-test.txt
PYTHONDONTWRITEBYTECODE=1 .repro-venv/bin/python -m pytest tests -p no:cacheprovider -v
```

第一項只用 Python standard library 檢查公開包 manifest；測試只用合成圖，不接觸 ground truth、GPU 或 Kaggle。`requirements-overlay.txt` 記錄原已接受 T4 overlay 的版本，當時 Python 為 3.12.13。Torch／CUDA／完整 base-image 相依閉包未完全盤點，不能將這份 CPU requirements 說成整本 notebook 環境。

## 2. 自有 motion overlay 的精確重放

入口：[src/csv_overlay.py](src/csv_overlay.py)。固定 12 μm 搜尋半徑、最多 8 個 predecessor 候選、32 個鄰近 support pairs 的 robust median motion；只調整符合條件的普通 continuation `source_id`，不增加節點、不使用 GT，不覆蓋已存在的目的檔。

持有合法來源的 baseline CSV 時，可自行指定路徑：

```sh
.repro-venv/bin/python src/csv_overlay.py baseline.csv replay.csv --report replay_receipt.json
```

選取 `56071433` 的既存 visible 輸入為 12,197,672 bytes，SHA256 `052ebbb0c2f582f9bcb94fd914e994a6afa255acaa1ccef422df9c7b025656fe`；原 visible 輸出為 11,963,303 bytes，SHA256 `aa500dfd644e22e44d1d45728a3e9197b89dad71e9f788241cde283388f670fb`。這兩份 CSV 只保留本地，不放 GitHub。公開化當次的實際重放環境、結果與是否 bit-exact 見 [reproduction_checks.json](results/reproduction_checks.json)；不同套件版本／硬體不先承諾一致。

原 accepted T4 visible run：完整 notebook **1454.318 秒**，overlay **44.381 秒**，234,368 CSV rows、20 條 changed edges。這不等於 hidden 全測試集時間保證。

## 3. 完整接受版本與必要模型

本地保留 `55998516`、`56071433` 的 official downloaded notebook、build、visible output、acceptance、terminal／selection receipts 與 upstream provenance。固定 kernels 是：

- `efnutrrionpy/biohub-nusrati0940-private-replay-v1/1`
- `efnutrrionpy/biohub-fixed-collective-motion-v1/1`

它們當時為 private notebook，不能承諾一般讀者有權下載。所有者可透過自己的官方 Kaggle 介面匯出同一固定版本，再比對 manifest；**本公開包不自動上傳、重新提交或要求讀者繞過存取權**。完整 notebooks 含再散布授權未確認的上游程式，因此未直接重發。

必要 public model datasets：

- [pilkwang/biohub-tracking-support-pack-50ep-v1](https://www.kaggle.com/datasets/pilkwang/biohub-tracking-support-pack-50ep-v1)：primary temporal linker、offline wheelhouse。
- [pilkwang/biohub-temporal-unet3d-seed314159-v1](https://www.kaggle.com/datasets/pilkwang/biohub-temporal-unet3d-seed314159-v1)：secondary temporal linker。
- [pilkwang/biohub-deepcenter-unet3d-center-prior-v1](https://www.kaggle.com/datasets/pilkwang/biohub-deepcenter-unet3d-center-prior-v1)：center prior。

來源 metadata 已保存 CC0-1.0 宣告；本包不帶權重。請依來源使用條款合法取得，按 [final_artifacts.json](results/final_artifacts.json) 的 **checkpoint bytes／SHA256** 選版本；同名 latest dataset 不代表固定版本。另有 notebook 附掛的 public figures dataset，不應把它的存在誤認為三模型以外所有檔案都被用到。

官方 runtime metadata：NvidiaTeslaT4、Internet disabled、Python image digest `37c64f7dd9c54116ecd1bcc88817c5469b88387388fade02bfa8bf3fc647d461`。取得受限 competition inputs 必須先接受競賽規則；不公開原影像、標註或衍生逐像素資料。完整 upstream training recipe、所有 transitive licenses 及 hidden runtime 未由本封存獨立驗證；最小包不聲稱完整端到端重訓可重現。

## 4. 研究快取清理後如何理解 receipts

本地逐項刪除舊封裝／解壓測試副本及可由唯一原始資料重建的 `.patches.npy`／`.images.npy`；source pins、geometry、targets、模型、predicted graphs、scores、STARTED／COMPLETE 歷史收據保留。公開包只放聚合研究結果，不含這些逐電影快取。

保留的 COMPLETE 是**歷史完成證據**，不是「被清掉的像素仍存在」。需要重建時須在獨立乾淨副本／輸出位置沿用 pinned source、相同上游輸入及合法本地原始資料；舊 producer 會拒絕原目錄的 COMPLETE，**不能直接對已清理原目錄執行 `--resume`**。此次封存沒有重建這些快取，也不承諾所有探索模型具備最小公開包獨立重訓能力。

詳細本地保存清單、逐項刪除及前後空間統計由 `publication/cleanup_receipt_20261002.json` 管理；該內部收據不隨公開包發布，以免暴露個人路徑或逐電影資料。
