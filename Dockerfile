#######################################################################
# STAGE 1: Build stage
#######################################################################
FROM python:3.10 as build
LABEL AUTHOR="M. SANCHO <m.sancho@kritical.es>"

# Add Gitlab to known hosts
RUN mkdir ~/.ssh/ && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY requirements.txt /

# install dependencies
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"
RUN pip install --upgrade pip && \
	pip install -r /requirements.txt


#######################################################################
# STAGE 2: Run stage
#######################################################################
FROM python:3.10-slim-buster
LABEL AUTHOR="M. SANCHO <m.sancho@kritical.es>"

# Copy python environment from first stage
COPY --from=build /usr/app/venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

WORKDIR /usr/app

# copy just the necessary sources
COPY src ./src
COPY i18n ./i18n

EXPOSE 8666

CMD ["python", "./src/manage.py", "run"]