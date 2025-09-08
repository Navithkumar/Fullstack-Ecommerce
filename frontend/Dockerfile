# ---------- Stage 1: Build ----------
FROM node:22.16.0-alpine AS build
WORKDIR /app

# Copy package.json + lock file
COPY package*.json ./

# Install ALL deps (including devDependencies)
RUN npm install

# Copy source
COPY . .

# Run Vite build (generates /dist)
RUN npm run build

# ---------- Stage 2: Serve ----------
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
