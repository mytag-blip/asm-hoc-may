# Draft inquiry — DataCedar

**Status:** Draft for the project group to review. Not sent.  
**Intended recipient:** DataCedar sales/data-rights support  
**Date prepared:** 20 November 2026

**Subject:** Confirmation of HOSE daily OHLCV coverage and academic-use rights

Hello DataCedar team,

We are a student team evaluating market-data providers for a non-commercial academic project on clustering and assessing stock-price volatility risk. The intended universe is 43 HOSE-listed companies, and the requested period is **19 November 2021 through 18 November 2026**. We are evaluating the terms before creating an account or paying for a plan; we have not called the API or downloaded data.

Could you please confirm the following in writing?

### 1. Coverage and history

1. Does DataCedar provide daily OHLCV for every ticker in our 43-symbol HOSE universe? We can provide the ticker list if useful.
2. For each symbol, is daily history available continuously from no later than 2021-11-19 through at least 2026-11-18? If not, please identify the symbols and available first/last dates, or explain how we can check coverage before subscribing.
3. The general Pricing page and the historical-data/API documentation appear to state different Quant history windows. Does the Quant plan at USD 29/month provide daily HOSE bars back to listing, including the requested period? Which current contract or plan terms govern?

### 2. Price basis and corporate actions

4. Please confirm the exact semantics of `raw`, `split`, `dividend`, and `all`. What adjustment formula/factor is applied, and are Open, High, Low, and Close adjusted consistently?
5. Which corporate actions are represented and used for adjustment: cash dividends, stock dividends/bonus shares, rights issues, splits, and reverse splits? Does the actions endpoint provide a complete historical event ledger for HOSE, including effective dates and revisions/corrections?
6. Are historical bars revised/back-adjusted when a corporate action or source correction is added? Is there a way to retain the as-of/version context for reproducibility?

### 3. Volume and units

7. The API schema describes `volume` in shares. Does it include matched trades only, negotiated/block transactions, or both? Are separate fields available for these components?
8. Please confirm the currency/price unit for HOSE bars and the timezone/session date represented by a daily bar.

### 4. Storage and academic use

Our planned use is limited to a non-commercial student project. Please confirm whether the applicable plan and source-rights permissions allow us to:

9. Retrieve OHLCV via the API and store the raw response/normalized daily rows on our local project machine.
10. Keep a separate staging copy for development, testing, and reproducibility, and retain it after the subscription ends. If retention is limited, please state the permitted duration and deletion requirements.
11. Use the data to calculate derived statistical features and clustering results, and provide necessary data excerpts or files to our course instructor for assessment.
12. Display charts and aggregate/derived analysis on a Vietnamese-language project demo website. Please distinguish an internal/classroom demo, a restricted-access demo, and a publicly accessible site. We will not republish raw CSVs unless expressly permitted.
13. Export figures/tables to a report and presentation, and what attribution, data-volume, or screenshot restrictions apply?

Please provide the Terms/license applicable to the HOSE data and the current source-rights permissions that govern API responses for these symbols. We understand that API access alone may not grant storage or redistribution rights, so we are seeking explicit clarification before use.

### 5. Plan, price, and access limits

14. Please confirm the total price for 43 HOSE symbols, daily OHLCV, and at least five years of history, including any taxes or other fees. Is the published Quant price of USD 29/month sufficient for this exact scope?
15. Please confirm the current Quant limits for symbols per request, request rate/quota, daily bar page size, cursor pagination, and any retention/export constraints.
16. Does account creation require a brokerage account, identity documents, or personal API credentials beyond a DataCedar account/key? We will not provide brokerage credentials or identity documents unless required and approved by our group.

We have not created an account, paid, called the API, or downloaded any market data. We will consider a read-only test only after the data rights and plan terms are clear and the project group approves it.

Thank you for your help.

Best regards,

**[Group representative]**  
**[University/course]**  
**[Contact email]**
