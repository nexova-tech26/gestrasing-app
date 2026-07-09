# == ETAPA 1: Compilación ==
FROM node:20-alpine AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

# == ETAPA 2: Producción ultra-ligera ==
FROM nginx:stable-alpine AS production-stage

# Copiamos los archivos compilados de la Etapa 1 a Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Sobrescribimos la configuración por defecto de Nginx con la nuestra
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 