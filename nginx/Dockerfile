
FROM lielstar1/sticky-nginx:latest


COPY nginx.conf /usr/local/nginx/conf/nginx.conf

RUN mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log && \
    touch /var/log/nginx/error.log

EXPOSE 80


CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]

