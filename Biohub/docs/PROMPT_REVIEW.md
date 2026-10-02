# 研究提示詞與執行行為檢討

這是賽後原創檢討，不是重新啟動研究的指令。原 Goal 保持 paused；官方 Private 為 .910、1714／4020，金牌目標未達。不能證明提示詞造成分數落後，也不能靠賽後改字追回結果。

## 保留的完整設計

- [原始設計](../prompts/ORIGINAL_DESIGN.md)：保存的完整 519 行版本，包含金牌、可信驗證、最少方法先驗、失敗配置不封殺家族及使用者暫停權限。
- [現行設計](../prompts/CURRENT_DESIGN.md)：完整 579 行版本，保留原章節與必要澄清，沒有以短摘要取代原設計。
- 兩份是歷史／現行文字的公開快照，**不是本公開包的自動執行入口**。原始版本中的泛用 competition placeholder 亦照原文保留。

公開化只把各自的 `WORKSPACE` 一行替換成 `<competition-workspace>`，沒有複製全域 AGENTS、個人會話紀錄或附件路徑。公開快照的雜湊由包內 manifest 記錄；公開化前的原文 SHA-256 為：

| 快照 | 公開化前來源 SHA-256 |
| --- | --- |
| ORIGINAL_DESIGN | `36e681b57a87f019d805e33e8ba193452f2b97d8b044052b36c642edaf8a7a38` |
| CURRENT_DESIGN | `6649ddfc89e8ab22b426cd361991ec5856119dae2aa58203256fa645cd92aa00` |

## 三個有依據的問題

1. **公開證據取得：原文主動性可澄清，漏查仍是執行責任。**
   原始 `<authority>` 第 59 行允許「consult official rules and legally available public material」，不是禁止查資料。搜尋紀錄顯示曾嘗試 Writeups 列表，卻在未取得正文後提早收尾；官方前五完整方案其實都已發布。這是取證不足，不能寫成「沒有人公開」。現行 `<research_strategy>` 改為主動取得與決策相關、能歸屬作者的公開證據；空白頁或索引 miss 不等於不存在。這屬於原文行為具體程度的澄清，不是把代理失誤歸罪使用者。

2. **信號到最終收益：機制可澄清，但正式指標與方向檢討本來已有要求。**
   原始第 252 行要求 objective 對齊 target structure，第 318 行要求 pooled official validation metric，第 260–261 行提醒不能一直沿單一 ancestry 微調。我方不是沒有時序模型、Transformer 或 joint decoder；五幀 correction 只改 root scalar，部分 pair ranking 固定，後續擴大候選雖改了中間輸出卻沒有增加完整圖分數。前五的可比較差異是監督覆蓋、學習目標及信號如何控制最終選擇，不是 solver 名稱。現行文字把這條傳導與方向重估說清楚；負結果本身仍可算進展，不設新硬門檻。

3. **任意門檻與前置工程：主要是代理自加或未遵守，不能怪原文。**
   原始第 138 行已說「Do not build release-grade manifests for disposable experiments」，第 327–328 行要求探索期輕量紀錄，第 359–360 行反對任意 worst-unit／minimum-gain veto。但執行歷史曾自立 .950 local cutoff、non-loss-count veto，且一個 Trackastra V4 版本先做了 72 項測試／77 個 release files，尚無該版本科學評分。應修正的是代理行為與階段判斷，而不是替清楚的原文再加長章節。已有可靠性與防洩漏要求仍保留。

上述「觀察」來自已保存的搜尋紀錄、原文對照與實驗摘要；「可能改善行為」只是推論，不是提示詞的因果消融。硬體故障、OOM、可用雲端額度、上游資料曝光和截止日也不能單靠提示詞解決。

## 實際窄幅修改：六句

2026-10-02 的最後一次提示詞修訂只在原 `<research_strategy>` 相應段落替換文字，沒有新增日期政策章節、固定檢查頻率或 winner 方法清單。下段共六句，其中一句沿用；project AGENTS 同時刪去直接重複的七行，沒有改 global AGENTS 或 native Goal objective API。

> Actively obtain decision-relevant public evidence from official writeups and attributable code or discussions; failed access or search does not establish non-disclosure. Compare supervision, representations and end-to-end effects with our measured results, without mandating a method. Prioritize attainable official-metric gains against the competitive gap and deployment route, not checks or intermediate metrics alone. Trace whether improved signals change final predictions and the metric; diagnose lost gains before scaling the recipe. Useful diagnoses count as progress, but persistent low yield calls for reassessing the formulation and highest-value alternative even if another small experiment exists. Do not turn Public scores into local promotion cutoffs.

## 前五方案是比較證據，不是必做清單

最終 Private 的 Sergio、Soheil、yu4u、Barry、Tang 使用的監督、偵測與解碼方式並不一致：冠軍用 greedy，其餘有不同 ILP／聯合圖設計。作者 local CV、混合 embryo folds 與多因素階段消融也不等於乾淨因果證明。應用它們找我方實際差距，不把方法名稱、作者分數或多數影片不退步升格為新規則。

完整第三方正文未放入本包；只保留以下公開出處和我們自己的比較：

- [Sergio：1st Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/1st-place-solution)，2026-10-01 發布。
- [Soheil：2nd Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/2nd-place-solution)，2026-09-30 發布。
- [yu4u：3rd Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/3rd-place-solution)，2026-09-30 發布。
- [Barry：4th Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/4th-place-solution)，2026-09-30 發布。
- [Tang：5th Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/5th-place-3d-u-net-transformer-linker-multi-s)，2026-09-30 發布。

本地重要原創檢討、逐隊來源與原文／小 diff 已留存；本公開摘要刻意不附個人 session 路徑、完整第三方文章或未明授權程式。本次歸檔只整理已有成果，不訓練、不提交、不恢復 Goal。
