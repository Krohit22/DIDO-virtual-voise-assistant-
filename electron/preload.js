const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
    launchDIDO: () => ipcRenderer.send('dido'),
    closeDIDO: () => ipcRenderer.send('closeDido'),
})
