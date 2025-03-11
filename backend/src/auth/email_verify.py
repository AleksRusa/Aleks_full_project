import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "aleksandr27rusakov@gmail.com"
SMTP_PASSWORD = "aleRUsak27421"

async def send_confirmation_email(email: str, token: str):
    confirmation_url = f"http://yourdomain.com/confirm-email?token={token}"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Подтвердите ваш email"
    message["From"] = SMTP_USERNAME
    message["To"] = email

    text = f"Пожалуйста, подтвердите ваш email, перейдя по ссылке: {confirmation_url}"
    html = f"""
    <html>
        <body>
            <p>Пожалуйста, подтвердите ваш email, перейдя по ссылке:</p>
            <a href="{confirmation_url}">Подтвердить email</a>
        </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    async with aiosmtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        await server.starttls()
        await server.login(SMTP_USERNAME, SMTP_PASSWORD)
        await server.send_message(message)