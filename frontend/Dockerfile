# Используем официальную Node-образ
FROM node:16

# Устанавливаем рабочую директорию
WORKDIR /app/frontend

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь код
COPY . /app/frontend/

# Открываем порт для Vite
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "run", "dev", "--", "--host"]
