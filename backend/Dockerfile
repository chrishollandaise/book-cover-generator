FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile
WORKDIR /backend
COPY . /backend
EXPOSE 8000