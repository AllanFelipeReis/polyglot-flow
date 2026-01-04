# Alteramos para 8.4 para satisfazer o Symfony 8.0/Laravel 12
FROM php:8.4-cli

# Instala extensões para Postgres e Redis
RUN apt-get update && apt-get install -y libpq-dev libzip-dev zip \
    && docker-php-ext-install pdo pdo_pgsql \
    && pecl install redis && docker-php-ext-enable redis

WORKDIR /var/www/html
COPY . .

# Instala o Composer de forma mais limpa
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Rodar o install ignorando requisitos de plataforma apenas para garantir o build
RUN composer install --ignore-platform-reqs

EXPOSE 80

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=80"]