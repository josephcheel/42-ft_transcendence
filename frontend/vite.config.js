import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path'; // Import resolve from path module

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'), // Set up the alias for the src directory
    },
  },
  assetsInclude: ['**/*.gltf', '**/*.glb', '**/*.wav', '**/*.mp3'], // Ensure Vite recognizes GLTF and audio files
});
