import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react(),
  ],
  base: "/",
  server: {
    host: "0.0.0.0",
    port: 3000, // Указываем порт 80
    strictPort: true, // Если порт занят, приложение не запустится
    watch: {
      usePolling: true
    }
  }

});