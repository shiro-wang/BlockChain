## 功能表
### 1. server.py
參數為node本地端PORT

### 2. 其餘program
參數為( node本地端PORT, 指定一同連接的其他node端(ex:127.0.0.1:{A_port}) )

### 3. 將自身資料記錄在json中

## 目前問題
### 1. broadcast_transaction連線
broadcast_transaction後，接收端本身遇到的連線問題 (好像可以忽略)

### 2. prehash掛掉
目前看來transaction能成功廣播了，但卻遇到了preblock_hash不符的問題??
-> transaction接收端認證後，沒問題就加進pending內並broadcast叫其他node也加，但此時會有時間差問題，導致接收端在創建新block的時候放進pending而其他node端還沒接收而沒有放進newblock，導致prehash不合