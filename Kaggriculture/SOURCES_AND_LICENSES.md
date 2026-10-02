# 來源、授權與公開邊界

本包只包含本研究產生的策略、政策參數、敘述和精簡結果，以及必要的已知授權引擎摘錄。
不把「網頁可以看」等同於「程式可以再散布」。

| 內容 | 來源與處理 |
| --- | --- |
| `strategies/*/engine_core.py` | 從 Kaggle Environments1.32.7 選取必要工人／動物／雇工原語，保留同目錄Apache-2.0 LICENSE及NOTICE；不是自行宣稱完整原創 |
| 最後策略的其他Python模組 | 本研究編寫的資源回饋、合法資訊邊界、路線、經濟評估與政策組合；原始檔案與checksum逐位元保留 |
| `*_actions.json`、`*_targets.json`、`policy.json` | 從公開Kaggriculture示範編譯出的離線行動／己方資源目標及固定路由參數，不是對手私人控制器程式碼、原始完整回放或執行時未來資訊 |
| 對手notebook／第三方writeup | 不再散布，完整來源僅本地保存；公開包保留識別與hash，沒有把未知授權改標MIT或Apache |
| 官方分數與回放 | 僅保留必要分數、submission／episode ID與來源摘要；不提供完整原始回放或credentials |
| 原Goal與研究敘述 | 使用者任務設計及本研究自行整理；未貼完整第三方文章或Oracle答案 |

上游引擎：[Kaggle/kaggle-environments](https://github.com/Kaggle/kaggle-environments)，
[Apache-2.0 LICENSE](https://github.com/Kaggle/kaggle-environments/blob/master/LICENSE)。
競賽：[Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)，
[規則](https://www.kaggle.com/competitions/kaggriculture/rules)。
實際使用的授權文字隨策略保存，不以會變動的master頁面代替本地版本證據。

公開示範取自submission56614976；選用的episode及實際檔案hash列於
`manifests/source_provenance.json`。我們未取得或附帶該作者的私人agent程式。
學到的政策仍可能與示範同祖先，因此不以它們當作多個完全獨立強對手。

本封存沒有替未知外部內容新增授權。自有部分的公開授權由使用者整合repo的授權
設定處理；若上層repo採其他授權，仍須保留引擎Apache-2.0條款與NOTICE，不得把
整個包無差別改標為完全自有作品。大型本地成果以manifest引用，不因存於本機就
推定可供他人取得。公開包不含瀏覽器cookie、個人session路徑、API金鑰或原始受限資料。
