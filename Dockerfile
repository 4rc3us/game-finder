FROM python:3
LABEL authors="arce"

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

EXPOSE 80

CMD ["scrapyrt", "-p", "80", "-i", "0.0.0.0"]