# Build
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# Injecte l’URL de l’API au moment du build (Cloud Build / docker build --build-arg)
ARG VITE_API_BASE_URL=
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Image légère : sert le dossier dist sur le port Cloud Run ($PORT)
FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve@14

COPY --from=build /app/dist ./dist

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "serve -s dist -l tcp://0.0.0.0:${PORT}"]
