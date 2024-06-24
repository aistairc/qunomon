FROM openresty/openresty:1.25.3.1-3-focal

# install dependencies
RUN ["luarocks", "install", "lua-resty-session", "3.10-1"]
RUN ["luarocks", "install", "lua-resty-http"]
RUN ["luarocks", "install", "lua-resty-jwt"]

## ADD lib/resty/openidc.lua /usr/local/openresty/lualib/resty/openidc.lua
RUN cd /usr/local/openresty/lualib/resty && \
    wget https://raw.githubusercontent.com/zmartzone/lua-resty-openidc/master/lib/resty/openidc.lua

# EXPOSE 80

# COPY ./nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
# COPY ./conf.d/ /etc/nginx/conf.d
COPY ./ssl/cert/server.crt /etc/nginx/cert/
COPY ./ssl/cert/server.key /etc/nginx/cert/

