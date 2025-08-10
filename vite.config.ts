import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "dist",
    emptyOutDir: false,
    lib: {
      entry: "src/main.ts",
      formats: ["es"],
      fileName: () => "main.js",
    },
    rollupOptions: {
      output: {
        chunkFileNames: "chunks/[name].js",
        assetFileNames: (asset) =>
          asset.name && asset.name.endsWith(".css")
            ? "main.css"
            : "assets/[name][extname]",
      },
    },
  },
});
