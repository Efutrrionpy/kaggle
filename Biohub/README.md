# Biohub：研究封存與賽後檢討

競賽：[Biohub Cell Tracking during Development](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development)。整理日期：2026-10-02。

**官方 final Private：1714／4020，榜面分數 0.910；未獲金牌。** 最終選取的兩筆提交是 `55998516` 和 `56071433`。前者精確 Private 分數為 **0.91051**，後者為 **0.90743**；較高 Public 不代表較高 Private。這份封存保留研究成果與失敗教訓，不把未達標改寫成成功，也不會自動啟動任何工作。

我們以公開 temporal U-Net／Transformer tracking 基線為起點，先研究 threshold 與 collective-motion 後處理，再測 NCC continuation、native 訓練、learned fork／ownership、五幀與 self-supervision，以及完整圖的校準與候選覆蓋。部分本地階段確有收益，但未轉化成勝過保留提交的官方結果；上游曝光與反覆開發亦限制驗證可信度。

## 內容

- [最終結果與官方來源](FINAL_RESULTS.md)：選取提交、Private 名次、來源與精度區別。
- [研究過程](RESEARCH_HISTORY.md)：方法演進、正負結果、決策及競爭差距。
- [重要結果表](results/research_results.csv)：區分 graph metric、局部 loss、正式分數及驗證限制。
- [重現說明](REPRODUCIBILITY.md)：自有 overlay、已接受 notebook、外部資產與可重現邊界。
- [原創 motion 程式](src/csv_overlay.py)與[測試](tests/)；[檢查結果](results/reproduction_checks.json)。
- [原始完整提示詞](prompts/ORIGINAL_DESIGN.md)、[現行完整提示詞](prompts/CURRENT_DESIGN.md)、[提示詞責任檢討](docs/PROMPT_REVIEW.md)。
- [最終產物 manifest](results/final_artifacts.json)、[來源及授權](THIRD_PARTY_NOTICES.md)、[包內完整性檢查](tools/verify_archive.py)。

## 公開範圍

本包不含原始受限競賽影像／標註、提交 CSV、大型模型權重、憑證、cookie、個人會話紀錄或第三方完整 writeup。外部 notebook 的再散布授權未確立，故只引用來源、固定版本與 checksum；完整接受版本及必要資產保留本地。自有程式依 [MIT](LICENSE) 公開，這不重新授權第三方內容。

`manifest.json` 驗證本包檔案；大型本地產物另以 `results/final_artifacts.json` 引用。後者的 visible CSV 雜湊**不是**官方隱藏重跑輸出的雜湊。最小公開包可重放／測試自有後處理，不能獨立重訓所有外部基線或保證重現官方隱藏分數。

本資料夾供使用者整合至 `Efutrrionpy/kaggle` 的競賽子目錄；整理者沒有自行修改或推送該 GitHub repository。原研究 Goal 保持 paused。
