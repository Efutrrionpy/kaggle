# 官方最終結果

## 我方結果：未達金牌

2026-10-01 15:54:53–15:54:55 UTC 以 Kaggle 官方唯讀 leaderboard API 取得已公開的 **Private** 榜：Efnutrrionpy **1714／4020**，顯示分數 **0.910**，該列沒有 medal 標記。官方 competition metadata 同時確認 Private 榜已顯示、可授予 medal；截止時間為 2026-09-29 23:59 UTC。金牌目標未達，不是僅等待 Public 刷新。

來源：[官方排行榜](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/leaderboard)；讀取 endpoint 為 `https://www.kaggle.com/api/i/competitions.LeaderboardService/GetLeaderboard`，request `{"competitionId":136605}`。包內 [official_evidence.json](results/official_evidence.json) 是已讀官方回覆的精簡轉錄，不冒充 raw API dump。

## 兩筆最終選取

| Submission | 策略／固定 notebook 版本 | Public | Private | 狀態 |
| --- | --- | ---: | ---: | --- |
| 55998516 | nusrati 0.940 精確 replay／threshold hedge，v1 | 0.94094 | **0.91051** | COMPLETE、最終選取 |
| 56071433 | 固定 collective-motion overlay，v1 | **0.94218** | 0.90743 | COMPLETE、最終選取 |

精確五位分數來自既存 2026-10-02 06:37:02.336218 UTC 官方 submission readback；榜面三位顯示並非不同實驗。完整結果及來源在 [final_artifacts.json](results/final_artifacts.json)。封存沒有重新提交或更改選擇。

較晚的 native／H／dense 路線 `56593643` 已 COMPLETE，保存的三位顯示為 Public 0.938／Private 0.904，因此未選取。`56181805` 的 fork-NCC Public 顯示為 0.942，曾是官方 Public best submission，**不等於**最終選取提交或 Private best。

## 正確的 Private 前五

| Private 名次 | 隊伍／作者 | 顯示分數 | 官方公開方案 |
| --- | --- | ---: | --- |
| 1 | Sergio Alvarez／sersasj | 0.977 | [1st Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/1st-place-solution) |
| 2 | Soheil Ayati／soheilayati | 0.970 | [2nd Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/2nd-place-solution) |
| 3 | yu4u／ren4yu | 0.967 | [3rd Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/3rd-place-solution) |
| 4 | Barry／songqizhou | 0.962 | [4th Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/4th-place-solution) |
| 5 | Tang／hirotetsu | 0.954 | [5th Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/5th-place-3d-u-net-transformer-linker-multi-s) |

五隊均為官方 Gold。方案發布於 2026-09-30／10-01，全文已在 10-01 讀取並核對作者及 Private 名次；本包只保留自己的分析及來源。Private 分差約 **0.044–0.067**（按榜面顯示），不能視為單一方法的因果收益。Public yu4u 第一不是 Private 第一。

方法差距詳見 [研究過程](RESEARCH_HISTORY.md#7-賽後公開方案比較與提示詞責任)。原先「前五完整方法未知」的查找結論已撤回：動態空白頁與搜尋索引失敗不能證明方案未公開。
