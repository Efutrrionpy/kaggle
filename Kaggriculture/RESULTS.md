# 結果：正式 Private 仍 pending

不要把本包的完成或公開封存理解成比賽目標達成。
官方最終 Private GOLD 是唯一成功條件，現在沒有足以宣告金牌的證據。

## 正式提交與時間

- 提交截止：2026-09-30 23:59 UTC（台灣10月1日07:59）。
- 官方時程：10月1日至約10月15日繼續對局，收斂後產生最終排名。
- 截止後 API `deadline` 改為10月14日23:59 UTC，且 `disableSubmissions=true`。
  官方 Timeline 的提交截止仍是9月30日；不是重新開放提交。
- 原 final pair：FlexService **56705674**、AdaptiveMilk **56698261**，均 COMPLETE。
- 本包最新觀察時間與欄位在 `results/official_status.json`；不持續偷偷更新靜態公開包。

10月1日00:08 UTC 曾短暫可見 Public／Private 同列第136/10246名、2420.3分及 SILVER
標籤；當時金牌標籤邊界為第30名、2653.0分。這是**歷史暫列**，不是核實最終銀牌。
之後官方又隱藏 Private，最終核實欄位未設為true。不能把先前暫列名次當成現在名次。

官方來源：[Timeline](https://www.kaggle.com/competitions/kaggriculture/overview/timeline)、
[Evaluation](https://www.kaggle.com/competitions/kaggriculture/overview/evaluation)、
[Leaderboard](https://www.kaggle.com/competitions/kaggriculture/leaderboard)。

## 決策相關比較

勝=1分，和=0.5分。表中不同列通常不是同一批世界，不可拿分母不同的勝率直接排方法。

| 實驗 | 候選 / 對照 | 判讀 |
| --- | --- | --- |
| Farm96 分支，新32世界 | 早期83、後期95 / 原策略95，均128格 | 開發學習訊號沒有穩定轉移 |
| Joint market J_3，新32世界 | 93 / 89，均128格 | 區間跨零，且對Yarn5退步 |
| Current-state service，新8世界 | 46 / 47，均64格 | 有真實增量蛋，沒有競爭增益 |
| AdaptiveMilk，新32世界 | 636 / EconomicFirst595 / Feed501，均704格 | 晉級；636分包含2和局 |
| FlexService，新32世界 | 677 / Adaptive622 / Feed548，均768格 | 晉級；部署證據另列 |
| NativeDeadlines，新32世界17對手 | 1055 / Flex1037，均1088格 | 20救回、2退步；資金視野問題 |
| Committed，兩組共64新世界7對手 | 843 / Flex832，均896格 | 11救回全對舊LateFlock；未提交 |
| CareTrade，新32世界 | 418 / Committed418，均448格 | 沒新增救回，平均分差−28.88；未晉級 |

分組時以世界為單位考慮不確定性，不把雙座位及同祖先對手當作獨立樣本。
本地 best-of-two 是事後選擇的上限診斷，**不是**官方 two-submission 評分的重現。

## 實際封裝與耗時

| 策略 | 原提交SHA256 | 獨立實測最大callback |
| --- | --- | ---: |
| FlexService | `20cff504fee6b78a539bf1bbdcaa90678e2e3db1de2e2ead2dfde8e205c2da87` | 0.1051秒以下 |
| AdaptiveMilk | `c532e7b11701929798a916ddf757411c74ccc256f076a78545bbfcf01b856722` | 0.0491秒以下 |

每個正式版本都在自己的官方驗證對局雙座位重現1438個動作，環境1.32.7。
這證明當時上傳路徑正確，並不證明對所有未來世界永遠不超時或具有金牌實力。
`results/deployment_checks.json` 保存原核對與獨立runtime摘要。

NativeDeadlines／Committed 為未提交本地成果，checksum另存 `manifests/local_artifacts.json`。
Committed 在27條完整留存路徑的callback／stdio/reset檢查通過，最大callback6.878秒，
每局累積overage最高24.267秒（允許60秒）。它明顯比正式Flex慢，不能沿用父版本耗時。

本次清理沒有新增比賽、訓練、上傳或修改策略；只重新重建原提交封裝及核對完整性。
