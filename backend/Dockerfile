FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile
WORKDIR /backend
COPY . /backend
EXPOSE 8000