# Gebruik een officiële Python runtime als een ouder-image
FROM python:3.8-slim

# Stel de werkdirectory in (waar je applicatie in de container zal leven)
WORKDIR /app

# Kopieer de huidige directory-inhoud naar de werkdirectory in de container
COPY . /app

# Installeer alle benodigde packages gespecificeerd in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Maak de poort beschikbaar voor de wereld buiten deze container
EXPOSE 5000

# Definieer environment variabele
ENV ZAMMAD_URL=https://ENDPOINT-ZAMMAD-INTEGRATION

# Voer app.py uit wanneer de container wordt gelanceerd
CMD ["python", "app.py"]
