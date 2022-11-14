# Backend
This is the backend for the project. Currently, it is just a RESTful API written in Python using the FastAPI framework.

## Preqrequisites
> **ATTENTION: If you do not have a CUDA enabled device, some functionality of the backend will be lossed (e.g. image generation)**
1. [Install Python >=3.10.0](https://www.python.org/downloads/)
2. [Install CUDA == 11.6](https://developer.nvidia.com/cuda-downloads)
3. Replace AUTH_TOKEN variable in `backend/auth_token.py` with your Hugging Face user access token with read scope access. [See here](https://huggingface.co/docs/hub/security-tokens) for more information.

## Installation
```bash
cd backend
pip install --user pipenv
pipenv install
pipenv shell
uvicorn main:app
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.