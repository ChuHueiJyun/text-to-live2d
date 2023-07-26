### 前端安裝流程
* 安裝 node.js：https://nodejs.org/dist/v14.17.3/node-v14.17.3-x64.msi
* 至 text-to-live2d\Samples\TypeScript\Demo 目錄下執行： 
  ```
  npm install
  npm start
  ```
* 瀏覽器輸入：http://localhost:5000/Samples/TypeScript/Demo/

### 後端安裝流程
#### 資料庫
* 安裝 MongoDB：
  * https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.7-signed.msi

#### API
* 安裝 Anaconda：https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Windows-x86_64.exe
* 建立虛擬環境：
  ```
  conda create -n <虛擬環境名稱> python=3.7
  ```
* 啟動虛擬環境：
  ```
  activate <虛擬環境名稱>
  ```
* 至 ChatSystem 目錄下執行：
  ```
  pip install -r requirements.txt (跑不起來就自己一個個裝)
  python app.py
  ```