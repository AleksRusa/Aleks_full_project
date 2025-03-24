import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  base: "/",
  server: {
    port: 80, // Указываем порт 80
    strictPort: true, // Если порт занят, приложение не запустится
  }

});