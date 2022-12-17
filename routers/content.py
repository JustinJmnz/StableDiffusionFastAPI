import torch
from diffusers import StableDiffusionPipeline

from fastapi import APIRouter, Depends, Response, HTTPException, Form
from sqlmodel import Session
from Models.Content import Content
from DataAccess.DatabaseService import get_session
from io import BytesIO
import base64

router = APIRouter(prefix='/api/content')


pipeline = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-5")
#pipeline = pipeline.to('cuda')
#pipeline.enable_sequential_cpu_offload()
pipeline.enable_attention_slicing()

@router.get('/{id}')
def get_content(id: int, session: Session = Depends(get_session)):
    data = session.get(Content, id)

    if data:
        return Response(content=data.content, media_type='image/png')
    
    return HTTPException(404, f'Content {id} does not exist')

@router.post('/', responses = {
        200: {
            'description': 'Image',
            'content': { 'image/png': {} }
        },
        400: {
            'description': 'Bad request'    
        },
    },
    response_class=Response
)
def post_content(prompt: str, session: Session = Depends(get_session)):
    if not prompt:
        return HTTPException(400, 'Bad request')
    
    image = pipeline(prompt, num_images_per_prompt=1).images[0]

    # Generate the bytes of the image
    stream = BytesIO()
    image.save(stream, format="PNG")
    imageBytes = stream.getvalue()

    data = Content(text=prompt, content=imageBytes)
    session.add(data)
    session.commit()
    session.refresh(data)

    return Response(status_code=200, content=base64.b64encode(data.content), media_type='image/png')

@router.delete('/{id}')
def delete_content(id: int, session: Session = Depends(get_session)):
    content = session.get(Content, id)

    if content:
        session.delete(content)
        session.commit()
        return Response(status_code=204)
    
    return HTTPException(404, f'Content {id} does not exist')
