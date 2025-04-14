import { globalShortcut, ipcMain, Menu, Tray } from 'electron'
import { app, BrowserWindow } from 'electron/main'
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';


let isQuiting
let pythonProcess

const filepath = fileURLToPath(import.meta.url)
const __dirname = path.dirname(filepath)

// production
const pythonScriptPath = path.join(process.resourcesPath, 'python-script.py')

app.whenReady().then(() => {

    pythonProcess = spawn('python', ['python_backend/main_model.py']);
      
      pythonProcess.stdout.on('data', (data) => {
        console.log(`Python Output: ${data}`);
      });
      
      pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
      });
      
      pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
      });

    // -------------------------system tray-------------------------
    // system tray and context menu creation
    const tray = new Tray('public/whitelogo.png')
    const menu = Menu.buildFromTemplate([
        { label: 'exit', type: 'normal', click: ()=>{
            isQuiting = true
            app.quit()
        } }
    ])
    tray.setContextMenu(menu)
    tray.setToolTip("DiDo")


    tray.addListener('click', ()=>{
        win.show()
    })


    // -------------------------window-------------------------
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        autoHideMenuBar: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            // devTools: false
        }
    })
    win.maximize()
    win.hide()
    win.loadURL('http://localhost:5173/')


    // -------------------------overriding shortcuts-------------------------
    win.webContents.on('before-input-event', (event, input) => {
        const blockedShortcuts = [
            'Ctrl+Shift+I', // Ctrl+Shift+I / Cmd+Shift+I
            'F12', // F12 key
            'Ctrl+Shift+C', // Ctrl+Shift+C / Cmd+Shift+C
            'Ctrl+Shift+J', // Ctrl+Shift+J / Cmd+Shift+J
            'Ctrl+Shift+K', // Ctrl+Shift+K / Cmd+Shift+K
            'Ctrl+U', // Ctrl+U / Cmd+U (View Source)
            'Ctrl+R', // Ctrl+U / Cmd+U (View Source)
            'Ctrl+W' // Ctrl+U / Cmd+U (View Source)
        ];

        // Construct the shortcut string
        const shortcut = `${input.control ? 'Ctrl+' : ''}${input.shift ? 'Shift+' : ''}${input.alt ? 'Alt+' : ''}${input.key.toUpperCase()}`;

        // Check if the shortcut is blocked
        /* if (blockedShortcuts.includes(shortcut)) {
            event.preventDefault(); // Block the shortcut
            console.log(`${shortcut} is disabled within the app`);
        }   */
    });


    // -------------------------window hide/close-------------------------
    // hide window on close and quit program when clicked on exit in tray
    win.on('close', (e)=>{
        
        if(isQuiting){
            if(pythonProcess){ //kill python script only if it isn't already killed
                pythonProcess.kill('SIGTERM')
            }
            app.quit()
        } else {
            // prevents from closing and just hides window
            e.preventDefault()
            win.hide()
        }
    })

  
})

//listening to event from front-end
ipcMain.on('dido', ()=>{
    if(!pythonProcess){
        pythonProcess = spawn('python', ['python_backend/main_model.py']);
    }
})
ipcMain.on('closeDido', ()=>{
  pythonProcess.kill('SIGTERM')
  pythonProcess = null
})
