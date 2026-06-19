import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Use relative pathing to ensure links work perfectly when mounted inside assets/
  build: {
    outDir: '../custom_hr_pro/public/hr-dashboard',
    emptyOutDir: true,
  }
})
