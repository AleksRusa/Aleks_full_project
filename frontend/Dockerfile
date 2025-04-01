# Используем официальную Node-образ
FROM node:18

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json /app/

# Устанавливаем зависимости
RUN npm install

# Копируем весь код
COPY . /app/

# Открываем порт для Vite
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "run", "dev", "--", "--host"]
