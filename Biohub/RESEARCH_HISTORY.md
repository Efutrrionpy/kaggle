# Biohub 研究過程與失敗教訓

這份紀錄整理 2026 年 Biohub Cell Tracking during Development 的實際研究成果，而不是勝出方案。最初希望建立有競爭力、能合法重現的細胞偵測與譜系追蹤管線，最後的成功條件是官方 final Private 金牌。官方結果為 **Private 0.910、1714／4020，未獲金牌**；兩筆最終選取提交為 `55998516` 與 `56071433`。研究已結束，本封存不會重啟訓練或提交。

正式結果另見 [FINAL_RESULTS.md](FINAL_RESULTS.md)，重現範圍與外部資產限制見 [REPRODUCIBILITY.md](REPRODUCIBILITY.md)。本篇所有本地數字均沿用已完成紀錄，沒有為封存重新訓練或重算實驗；可讀取的聚合表在 [results/research_results.csv](results/research_results.csv)。

## 如何閱讀這些結果

「官方 Public／Private」是 Kaggle 已評分提交；「released-reference graph metric」是本地使用當時發布的評分程式重建完整圖後所得。後者不能保證與所有伺服器實作細節相同。不同電影集合、偵測節點及上游模型下的分數不能直接相減成方法優劣。

本地使用了數種驗證層次：訓練資料上的擬合診斷、排除某一 residual head 訓練資料的比較、來源分組比較，以及完整圖 readout。許多上游 detector／crop／選模資料已有曝光；**head cross-fitting 不等於整條管線乾淨 OOF**，歷史上反覆使用的電影也不是未觸碰的 lockbox。以下保留這些限制，不把局部正結果改寫成泛化證明。

## 1. 公開基線與保守後處理：先得到能部署的圖

早期以已公開的學習式偵測／追蹤基線為出發點，重建離線輸出、動態電影分塊、穩定 ID／座標與圖約束，逐步研究 gap completion、division threshold、motion relinking 等後處理。這些基線及外部權重的來源、授權與取得限制需依公開 manifest 辨識，不能因本地包裝就稱為自有模型。

最後保留的 threshold hedge `55998516` 是一個既有精確重放版本；motion 主力 `56071433` 則在固定節點、目標端點與輸出契約上加入 collective-motion overlay。選擇兩筆的理由是保留不同失效型態，而不是聲稱它們的 Private 互補性已被驗證。

固定 32 支開發電影上，threshold 0.26 與 0.12 使用 released-reference metric 重算後為 **0.9212566880 → 0.9221065460**。先前 proxy 使用不同 division matching，原本只報出 +0.0000686163；正確重算的差為 +0.0008498581。這是一次重要的評分修正，但 panel 的上游訓練／選模曝光已確認，不能稱為獨立驗證。其唯一新增 division TP 也集中於一支電影，移除該電影後候選相對控制變為負值。

同一固定 panel 上，motion 為 **0.9220957583**，相對 anchor +0.0008390703。部署 notebook 的實際 T4 執行和輸出 parity 成功，Public 為 0.942；這支持「能執行且輸出契約一致」，不代表有金牌能力。最終 threshold hedge Private 0.910，motion Private 0.907；當時較高的 Public 主力不是最終較高的 Private 提交。

## 2. NCC continuation：影像證據能改善連結，但分裂不能被忽略

接著固定節點與候選幾何，補齊 normalized cross-correlation（NCC）影像證據，用同一 continuation policy 比較原圖。舊候選快取中 99.35% NCC 值可精確重用，只計算缺項；這避免將介面修補誤變成重新推論。

在 32 支已使用過的電影上，motion 0.9220957583，允許不發出分裂的 common NCC 為 **0.9242455415**。edge component 改善，但 division term 流失，兩個來源的淨效果方向也不同。因此沒有把「NCC continuation 正向」等同「移除分裂較好」。

之後重建 temporal U-Net 與跨節點 Transformer 的 native 訓練 recipe，並用同一 N／F／C 比較：N 是 native graph，F 保留 immediate fork 並用 NCC 接 continuation，C 是無 fork NCC。epoch 5 的 12 支模型未擬合電影為 **N 0.645376、F 0.679688、C 0.690039**；epoch 20 變為 **0.654290／0.686770／0.696590**。NCC 改善可重現，但更長訓練的平均增益小，條件式 movie bootstrap 區間含零；native 的分裂 precision 仍不足。這些電影有歷史研究曝光，不是完整研究策略 OOF，也不能從弱 recipe 推論整個神經方法的上限。

完整官方 division metric 還檢查 parent／grandchild topology。即使保留兩條 immediate fork edge，改動鄰接 continuation 仍可能改變 division TP；「fork edge 沒變所以分裂分數必不變」是曾被實測排除的假設。

再把固定 fork-NCC overlay 接回較強的部署管線。T4 實測約 23.81 分鐘，NCC 約 89.56 秒；CSV parity 成功。提交 `56181805` Public **0.942**，沒有可見增益，也沒有因此替換最終兩筆選取。三位小數相同不揭露精確隱藏分差，visible runtime 也不是隱藏全測試集的時間保證。

## 3. 學習分裂配置：局部 likelihood 改善不保證完整圖改善

後續嘗試把分裂從固定規則改為 learned configuration：partial supervision、unknown continuation marginalization、pair residual、ownership competition、圖有效的 joint decoding。這不是只有 threshold sweep，也不是完全沒有考慮稀疏標籤或聯合分配。

一個 NCC-preserving pair residual 在 30 支擬合電影上把 conditional NLL **2.107995 → 1.225944**，pair ranking 也稍好；但完整圖從固定 fork incumbent **0.9332279206 降至 0.9196669704**。division TP 4→7，同時 FP 12→121。固定 single-edge potential 不能固定最後選中的 links：新增 pairs 會消耗 child ownership，影響整圖。這指出局部 loss／配置校準與全局選擇的落差，不是「pair learning 永遠無效」。

另一個 ownership pilot 在四支擬合電影改善：H **0.921203**，factorized **0.935216**，joint **0.937003**；但 residual 訓練排除的 15 支電影卻由 H **0.970864** 降至 **0.932039／0.927121**，且兩個來源都退步。訓練樣本偏重分裂、有限正例及推論人口轉移是合理疑點；完整 anchor parity 已排除這一版本的介面數值漂移。該比較仍有固定上游曝光，不能把它當完全 embryo-disjoint 泛化。

決策是記為這些配置 `NEEDS_REDESIGN`，保留有效 supervision／solver 經驗，不把單次 loss、硬體錯誤或包裝失敗升格成永久家族禁令。

## 4. 五幀與 self-supervision：學到時間訊號，仍需驗證決策收益

研究轉向更直接的 dense temporal representation。以相同 root cohort、source-owned normalization 與既有 anchor，比較五幀可訓練 encoder、低維 frozen feature head 及 masked appearance/change SSL。未標註 roots 不自動變成負例；SSL 僅用相應來源的像素。

未 regularize 的五幀版本迅速擬合訓練資料，內部 validation NLL 反而惡化；選中初始 anchor，沒有改善。加入 residual 平方 penalty 後，兩 fold pooled conditional NLL **0.330700 → 0.327215**，weighted AUC **0.966829 → 0.968346**，但低 FP tail 仍是混合結果。此版本每個 root 只加一個 scalar，**intrinsic pair ordering 和 nonfork 分數不變**；模型再大也不能改動所有需要修正的決策。

masked-change SSL 的 reconstruction 與時間順序診斷顯示確實學到訊號。fold 0 的 matched downstream NLL **0.358785 → 0.353003**、AUC **0.972037 → 0.972670**；不同 FP budgets 有得有失，與原模型 margin correlation 高達 0.9986。這是有用的局部結果，不是新獨立 hedge 或官方 graph score。內部選模正例極少、上游 crop／訓練曝光與重複開發仍限制可信度。

整機 OOM 曾由四支完整影片並行解碼引發。之後使用少量 worker、bounded frame cache、逐電影與可續接 receipt，並在 T4 實際檢查 image → NCC → H → dense → solver → CSV。單電影 T4 route 約 **605.89 秒、RSS 1.56 GiB**，現有參考中心下 graph parity 成功；跨硬體浮點輸出不是 bit-exact。這是部署進展，不是準確度改善，也不能把局部 runtime 外推成所有隱藏電影的保證。

## 5. 完整 route 與 scalar calibration：正向 signal 仍未超越已選模型

對同一當前 route 的已保存圖做 199 支完整 readout：baseline **0.91420834 → H 0.91875606 → H＋dense／center 0.92298783**。H→dense division TP **17→24**、FP **41→33**；這說明影像／dense stage 有實質收益，不能說所有新 signal 都被 decoder 抹掉。

但 baseline→dense 的 division TP 總數仍是 24：實際為 shared 16、新增 8、失去 8。舊與新 route 的偵測節點／座標幾乎都不同，detector、averaging、coverage、center 等共同變動，這不是單一 representation 的因果消融。199 支有上游曝光，保護 panel 也被反覆使用。

這條新主力提交 `56593643` 實際為 **Public 0.938、Private 0.904**，均低於保留主力，因此未選取。不能以 exposed local gain 推翻正式 transfer 結果。

另測固定 native agreement shrinkage：全 199 支描述性分數 **0.92298783 → 0.92401391**。但由相反 source／fold 的完整圖指標選權重後，B120 source-owned crossfit **0.93060631 → 0.93015715**，FP 21→26。事後挑出的較高全資料分數不是 held-selection 證據，不能用來宣稱成功。這支持對 scalar calibration 的收益預期重新評估，不排除其他 agreement／representation 方法。

## 6. 擴 gate 的負結果：增加 coverage 不等於救回事件

最後對已觀察到 pre-H gate 失敗的 18 支電影，把幾何候選 root 預算 K500→K1000；只處理新項，重用原 NCC、H 及 dense 依賴。新增 **8,988 H roots、8,260 dense roots**，但完整分數仍為 **0.920656263046**，division **TP5／FP9／FN38** 完全不變。有 graph edge changes，卻沒有 scored gain，因此不能寫成所有輸出相同。

進一步的聚合支持診斷把 151 個 division events 分為：已回收 24、fallback 覆蓋問題 36、pre-H gate 18、可行 pair utility 低於 nonfork 45、window role 不支持 26、positive 但未回收 2。這是局部可行性與損失位置分類，不是可同時達成的召回上界，更不是可部署的 GT-restoration。

結論是單純 gate widening 的這一版本沒有改善；不能因此否定所有影像模型、gate 或 event-native 方法。真正待解的是監督契約、pair／occurrence 信號與 assignment／temporal topology 之間的傳導，而不是繼續盲目增大候選數。

## 7. 賽後公開方案比較與提示詞責任

官方 Private 前五的完整 writeup 在賽後已發布。最初搜尋雖碰過 Writeups 列表，卻在動態頁面／索引失敗後未讀到具體文章便提早收尾；這是我的取證執行失誤，不是使用者禁止調查。補查後才核對完整正文、作者及 Private 名次，撤回「前五完整方法未知」。Public 第一與 Private 第一也不可混用。

以下只用自己的摘要指出差異，不附第三方全文或不明授權程式：

| Private | 已披露的重點 | 對我方檢討的意義 |
| --- | --- | --- |
| [1／Sergio，0.977](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/1st-place-solution) | 擴充分裂監督；學親屬 occupancy 與 identity，再做 greedy 解碼 | 信號的監督目標／覆蓋比是否採用 ILP 更值得追查 |
| [2／Soheil，0.970](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/2nd-place-solution) | 聯學 detection、motion、uncertainty、descriptor，保留弱候選 | detector 與 downstream 契約需一起看，不能只調最後 scalar |
| [3／yu4u，0.967](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/3rd-place-solution) | 分開學 detection／flow／matcher／division，校準評估支持與正確性 | 稀疏標籤語義及 learned evidence 如何轉成完整圖效用要明確量測 |
| [4／Barry，0.962](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/4th-place-solution) | 學得分裂信心控制逐節點 ILP cost，救回弱第二女兒 | 不能只看分類分數，應核對新增／失去事件及 ownership 衝突 |
| [5／Tang，0.954](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/writeups/5th-place-3d-u-net-transformer-linker-multi-s) | 多任務 linker、公開資料預訓練與 confidence-aware ILP | 監督與 representation 可有多種有效路徑，不構成必做方法清單 |

來源讀取為 2026-10-01 UTC；方法是作者披露，不是本封存獨立重跑。其消融常同時改多因素，部分 movie CV 有上游或 embryo 曝光限制，不能把作者改善值相加成可追回的分數。前五與我方 Private 差 **0.044–0.067**，足以確認競爭差距，但不能單憑榜位推論單一敗因。

提示詞原本已有輕量原型、正式指標、方向重估、方法開放及可信驗證要求。研究中自加的 Public-derived local 0.950 gate、任意 non-loss／worst-unit veto，與原文相悖；某些原型前置工程也超過必要程度。一個 Trackastra 版本已有 72 tests／77 release files 卻尚無該版本的科學評分，是需要反思的資源配置，不足以否定其他版本或整個方法。

2026-10-02 的窄幅提示詞修訂只在原研究策略段澄清：主動取得會改變決策的公開證據，比較 supervision／representation／end-to-end effects；追查 improved signal 是否真正改變最終圖與指標；持續低收益時重估 framing 與高價值替代方案。完整原設計、金牌條件與方法開放保留，沒有把 winner 方法變成新檢查清單。這不能證明提示詞造成落後，更不能藉改字免除取證與執行責任。

## 最後留下的教訓

- 同時保留正、負結果：NCC 與 H→dense 的收益是真的，失去既有 divisions、calibration 不轉移及 K 擴張零收益也是真的。
- 量測契約是科學的一部分：metric matching、節點人口、整圖 decoder、upstream ancestry 與資料曝光不可被小 head OOF 洗掉。
- 檢查要服務研究：合理的 integrity／安全測試不能取代競爭差距、完整指標及方向價值；已完成快取不要為包裝反覆重算。
- configuration 失敗不等於 family 失敗；缺 mount／依賴、GPU 掉線及 OOM 要按實際原因記錄，不能作為模型精度證據。
- 這次沒有達成金牌。可公開的成果是可追溯的最後提交、可重現邊界、方法演進與失敗教訓，不是賽後重寫成功故事。

## 結果表的出處

CSV 的 `source_record` 是封存時核對的原研究紀錄名稱，不代表那些包含完整內部紀錄的檔案全數公開；精簡數字與上述限制已在本篇及 CSV 保留。日期以相關研究紀錄的日期標示，不假稱本輪有新實驗。正式分數沿用 2026-10-01 的官方唯讀收據，沒有為整理再次查榜。第三方方案只鏈接合法公開來源，不隨包重發第三方全文、權重或程式。

本地原紀錄主幹：final-selection plan 與官方 Private readback；HEDGE evidence／checkpoint overlap audit；native epoch5／20、legacy common NCC／strong fork-NCC、joint residual／ownership transfer；five-frame／masked-change SSL；full199 transfer、native group calibration、incremental K1000 handoff；2026-10-01／02 原創公開方案及提示詞檢討。最終 artifacts 的來源與 checksum 由公開包 manifest 和重現文件說明。
