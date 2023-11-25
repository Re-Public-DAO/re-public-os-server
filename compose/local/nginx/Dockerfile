FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

#COPY ./compose/local/nginx/nginx.conf /etc/nginx/nginx.conf
#COPY ./compose/local/nginx/localhost.conf /etc/nginx/conf.d/localhost.conf

CMD ["nginx", "-g", "daemon off;"]