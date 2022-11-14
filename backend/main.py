# FAST API imports
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# STABLE DIFFUSION imports
import torch
from diffusers import StableDiffusionPipeline 
from hashlib import sha256
from io import BytesIO

# MODEL/BUSINESS imports
from models import Styles, Commission
import json
from pathlib import Path
from auth_token import AUTH_TOKEN

# -- SET UP STAGE --

# Stable Diffusion
if torch.cuda.is_available():
  DEVICE = 'cuda'
  try:
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, revision="fp16", use_auth_token=AUTH_TOKEN)
    pipe = pipe.to(DEVICE)
    pipe.safety_checker = lambda images, clip_input: (images, False)
  except Exception as e:
    raise e
else:
  print("WARNING: CUDA not available, restricting plate generation...")

# Create resource paths, if they don't already exist
DATA_PATH = Path('data')
DATA_PATH.mkdir(parents=True, exist_ok=True)

PLATES_PATH = Path.joinpath(DATA_PATH, 'plates')
PLATES_PATH.mkdir(parents=True, exist_ok=True)

# Fast API
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# -- END SET UP STAGE --

# END POINTS
@app.get('/books')
def read_books():
  """
  Fetches a list of supported books
  """
  BOOKS_PATH = Path.joinpath(DATA_PATH, 'books')

  if not BOOKS_PATH.exists(): 
    print("WARNING: No books found")
    return Response(status_code=404)

  return json.loads(Path('data', 'books.json').read_bytes())

@app.get('/styles')
def read_styles():
  """
  Fetches a list of supported styles
  """
  return {"styles": [style.value for style in Styles]}

@app.get('/plates/{id}')
def read_plates(id : str):
  """
  Fetches a generated plate by its ID
  """
  RES_PATH = PLATES_PATH.joinpath(f'{id}.png')

  if not RES_PATH.exists():
    return Response(status_code=404)

  return FileResponse(RES_PATH)

def generate_plate(passage: str, style: Styles):
  """
  Generates a plate from a passage and style using Stable Diffusion
  """
  with torch.autocast(DEVICE):
      return pipe(f"{passage} depicted in the style of ${style}", guidance_scale=8.5).images[0]

@app.post('/imagine', status_code=201)
def create_plate(comm : Commission):
  """
  Creates a plate from book's passage and a supported style
  """

  if not torch.cuda.is_available(): return Response(status_code=503)
  
  # generate image
  image = generate_plate(comm.passage, comm.style)
  
  # create hash based on bytes of generated image
  buffer = BytesIO()
  image.save(buffer, format="PNG")

  image_hash = sha256(buffer.getvalue()).hexdigest()
  
  # create the resource
  URI = Path.joinpath(PLATES_PATH, f'{image_hash}.png')
  image.save(URI)

  return Response(status_code=201, headers={"location": f'\{URI}'})