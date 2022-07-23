## Title
主要參考: https://devs.tw/post/401
Notion: https://www.notion.so/8-7e41c61aca474b228b641bdf0bc4b8a5
## 功能表
### 1. server.py

參數為node本地端PORT

### 2. blocktrain.py

參數為( node本地端PORT, 指定一同連接的其他node端IP:Port(ex:127.0.0.1:{A_port}->任一即可) )

1. Mining

開始挖礦

2. Add tramsaction

其中Receiver填目標的IP:Port，Amout為給對方多少金額，Fee為此交易小費(高則優先放入new block)，Message為訊息

3. Show balance
顯示自身金額

4. Try add fake transaction

添加未經驗證transaction到block並開始挖礦，嘗試比別人早挖到並將包含假交易紀錄的block館廣播出去

### 3. 將自身資料記錄在json中

以利之後要查詢

### 4. 可以自由加入/退出node list

為了能邊挖邊查看，可以利用不同port去執行，另外自行退出不會導致程式崩潰了

### 5. 事前注意事項

1. 請先修改class BlockChain 中 __init__的 self.socket_host，將此改為自己的IP

2. 注意要連線的node端的IP:Port填對就可以成功clone

## 目前問題
### 1. broadcast_transaction連線

broadcast_transaction後，接收端本身遇到的連線問題 (好像可以忽略)

### 2. prehash掛掉 (fixed)

目前看來transaction能成功廣播了，但卻遇到了preblock_hash不符的問題??

1. transaction接收端認證後，沒問題就加進pending內並broadcast叫其他node也加，但此時會有時間差問題，導致接收端在創建新block的時候放進pending而其他node端還沒接收而沒有放進newblock，導致prehash不合

2. 不只是transaction，在挖block時偶爾(非常少見)會有[相近時間挖到]加上[newblock傳送時間差]的機緣巧合下，導致出錯

### 3. 本身程式碼問題 (fixed)

接收block_broadcast時不須重作刪除pending_transaction，在add_transaction_to_block就已經做過，會導致加入block chain出問題，進而導致prehash出錯

## Debug
### v1.0.1

1. 修正minings啟動時將pending_transaction移除，其他node才clone，導致transaction沒辦法被複製到

2. 為了驗證方便，將difficulty上限限制在6

### v1.0.2

1. 修正使用其他功能時，無法跟著調整difficulty導致hash不符
