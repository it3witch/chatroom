const { app, BrowserWindow } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

let mainWindow
let flaskProcess

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    }
  })

  // 加载前端构建的 index.html
  // 这里假设你已经在 chat-frontend 里运行了构建命令，生成 dist 文件夹
  mainWindow.loadFile(path.join(__dirname, 'chat-frontend', 'dist', 'index.html'))
}

app.whenReady().then(() => {
  // 启动 Flask 后端
  flaskProcess = spawn('python', ['chat-backend/main.py'])

  flaskProcess.stdout.on('data', (data) => {
    console.log(`Flask: ${data.toString()}`)
  })

  flaskProcess.stderr.on('data', (data) => {
    console.error(`Flask Error: ${data.toString()}`)
  })

  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (flaskProcess) flaskProcess.kill()
    app.quit()
  }
})