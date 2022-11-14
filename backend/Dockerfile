FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime
RUN python -m pip install --upgrade pip
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile
WORKDIR /backend
COPY . /backend
EXPOSE 8000