## 功能表
server.py: 參數為node本地端PORT
其餘program: 參數為( node本地端PORT, 指定一同連接的其他node端(ex:127.0.0.1:{A_port}) )

###目前問題
1. broadcast_transaction後，接收端本身遇到的連線問題 (好像可以忽略)
2. 目前看來transaction能成功廣播了，但卻遇到了preblock_hash不符的問題?? (不太能理解為何錯)