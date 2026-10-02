# 來源與授權邊界

- 本包原創 motion overlay、合成測試、封存檢查程式及原創文件按根專案已有 MIT 宣告整理，見 [LICENSE](LICENSE)。這不把第三方模型、notebook、競賽資料或 writeup 重新授權為 MIT。
- 原始 temporal tracking baseline 來源包含 [nusrati/0-940](https://www.kaggle.com/code/nusrati/0-940) 與選取版本保存的 public-notebook provenance；完整上游 notebook 的 code-license 未由既存 metadata 確立，所以不在本包重發。本文的來源連結不是已取得再散布權的宣稱。
- 三組必要 pilkwang model dataset 於保存 metadata 宣告 CC0-1.0；只引用來源、bytes 與 SHA256，不重發權重、wheelhouse 或外部 source tree。dataset 授權不自動涵蓋其他作者 notebook。
- 外部 `kaggle-cell-tracking-competition` source tree 有 BSD-3-Clause notice；本包沒有複製該 tree。將來若另行重發必須保留其 notice，不能以 dataset CC0 取代 code notice。
- NumPy、SciPy、Polars 由使用者自行安裝，依各套件授權；本包不內嵌 wheels。已盤點 wheel metadata 不代表整個 Torch／CUDA／base-image 法律閉包均驗證完成。
- 官方前五方案只以我們自己的比較摘要與直接原文連結引用；不附完整第三方 writeup、未明授權程式或作者權重。
- 原始 competition 影像／GEFF、逐電影像素 cache、visible CSV、原始 API 全量榜單及個人 runtime/session 記錄均不公開；本地保存與公開授權是兩個不同問題。

來源與授權不明時，本封存選擇「可追溯引用、保留本地、清楚限制」，不宣稱完整自由再散布。上述為既存來源紀錄的整理，非法律意見。
