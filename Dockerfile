FROM python:3.11.1

COPY . /usr/src/idopt

WORKDIR /usr/src/idopt/src

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y netcat python3-venv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Instala as dependências.
RUN pip install --upgrade pip
RUN pip install pip-tools
RUN pip install -r dev-requirements.txt
# RUN pip install -r requirements.txt

# Adiciona um usuário não root.
RUN useradd -m idoptuser
RUN chown -R idoptuser:idoptuser /usr/src/idopt
# USER idoptuser:idoptuser

# Run entrypoint
# RUN sed -i 's/\r$//g' /usr/src/idopt/src/entrypoint.sh
# RUN chmod +x /usr/src/idopt/src/entrypoint.sh

# ENTRYPOINT ["/usr/src/idopt/src/entrypoint.sh"]
ENTRYPOINT ["tail", "-f", "/dev/null"]
