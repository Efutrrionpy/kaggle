# 面試敘事版本

## 30 秒版本

我主導了一個 AI-assisted Kaggle 地質序列預測專案：從 773 口井、約 509 萬列資料中，
預測每口井未知區段的 TVT。最大的挑戰是避免同井與空間鄰井洩漏，所以我建立完整井
分組的五折 OOF，並用 Particle Filter、CatBoost、物理座標投影和 HMM 做混合模型，將
本地 RMSE 從 15.91 降到 8.52。最終 Private 得分 8.889、排名 444/6191，獲得銅牌，
距銀牌線約 0.308。最大的反思是高上限的 dense alignment 應更早投入，而不是後期花
太多時間在治理與部署。

## 2–3 分鐘版本

這場比賽要根據水平井軌跡、Gamma Ray、已知的 `TVT_input` 前綴以及配對 typewell，
預測後段未知 TVT。資料有 773 口訓練井、約 509 萬列，其中約 378 萬列需要納入驗證
評分。

第一步不是建模型，而是解決驗證。若隨機切 rows，同井序列、空間鄰井與 typewell 會
造成嚴重洩漏；同時官方可見的三口 test wells 都能在 train 找到相同合法輸入，所以
Public leaderboard 特別容易誤導。

我建立了五折 complete-well OOF：每口井只能存在於一個 fold，所有 preprocessing、
空間鄰居、地質面和模型只能使用 fit wells。每個方法都必須產生完整 773 口井、約
378 萬 scored rows 的預測，再依官方 row-weighted RMSE 評分；另外檢查 target
poisoning、fold overlap、mask、row order 與 finite output。

模型從 carry-forward baseline 的 15.91 開始。接著用 Particle Filter 將水平井 GR 與
typewell GR 對齊，加入空間地質面和 residual boosting，再把預測轉換到比較平滑的
`U=TVT+Z` 座標做 robust quartic projection。最後 V71 使用 290 個 inference-legal
features 訓練 query-local CatBoost。

最終 F57 是固定組合：

```text
50% V71 + 45% U projection + 5% raw HMM
```

內部 hybrid cross-fit RMSE 是 8.5186。部署則必須符合 Kaggle 無網路與九小時限制，
所以我建立 deterministic inference、novel-ID full-data routing、submission alignment
以及 200 口井壓力測試。

最終 F57 Private 是 8.889、排名 444/6191，得到銅牌；銀牌線是 8.581，所以差 0.308。
OOF 與 Private 只差 0.370，表示驗證大致可信。相反地，Public 6.449 的候選因可見井
重疊而被刻意排除，最後 Private 是 9.565。

最大的失誤是把一次弱 SDF 配方失敗過度解讀成整個 dense-alignment 家族無效，而且
後期投入太多時間在 hard gates、manifests 與監控。下一次會更早投入 task-native
high-capacity model、保留 untouched lockbox，並將研究與 release engineering 分流。

## AI 使用方式

建議誠實描述：

> 這是我主導的 AI-assisted ML research project。我負責任務定義、驗證設計、實驗
> 優先級、模型選擇與結果責任；Codex agents 協助大量程式實作、執行和測試，Claude
> 用於獨立挑戰研究假設與尋找盲點。

不要宣稱所有模型和程式都是自己逐行手寫。面試重點應放在能否親自解釋：為何使用
complete-well CV、如何防止 leakage、為何不追 Public 6.449、為何選 F57，以及下一次
如何調整研究資源。
