export const generateRandomString = (length = 64) => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  };

export const vkConfig = {
    app: 53252724, // Идентификатор приложения
    redirectUrl: 'http://localhost', // Адрес для перехода после авторизации
    scopes: 'email vkid.personal_info', // Список прав доступа
};

export const generateCodeChallenge = (codeVerifier) => {
    // 1. Преобразуем codeVerifier в массив байтов (ASCII)
    const encoder = new TextEncoder();
    const data = encoder.encode(codeVerifier);
  
    // 2. Хэшируем массив байтов с помощью SHA-256
    const hash = crypto.subtle.digest('SHA-256', data);
  
    // 3. Кодируем результат хэширования в Base64 URL-safe
    const base64UrlEncode = (arrayBuffer) => {
      const base64 = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
      return base64
        .replace(/\+/g, '-') // Заменяем '+' на '-'
        .replace(/\//g, '_') // Заменяем '/' на '_'
        .replace(/=+$/, ''); // Удаляем завершающие '='
    };
  
    return base64UrlEncode(hash);
  };