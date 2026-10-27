FROM nginx:alpine
# Копируем наш кастомный конфиг Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Копируем статику
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
