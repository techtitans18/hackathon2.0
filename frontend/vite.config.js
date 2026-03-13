import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

//https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Allow access from network
    port: 5173,
    strictPort: false,
    //If you need to allow specific hosts:
    allowedHosts: ['localhost', '127.0.0.1',"jo-truing-claudette.ngrok-free.dev"]
  }
})
