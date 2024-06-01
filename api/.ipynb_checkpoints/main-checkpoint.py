from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np 
from io import BytesIO
from PIL import Image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

app=FastAPI()

model_version = 1

# Load the saved model
MODEL = tf.keras.models.load_model("./saved_models/4.keras")

# Get the prediction function from the 'serving_default' signature
# infer = MODEL.signatures["serving_default"]
CLASS_NAMES=['Early Blight',"Late Blight","Healthy"]

@app.get("/ping")
async def ping():
    return "hello"

def read_file_as_image(data):
    image=np.array(Image.open(BytesIO(data)))
    return image
    
    

@app.post("/predict")
async def predict(
    file:UploadFile=File(...)
):
    
    image=  read_file_as_image(await file.read())
    image=image.tensor
    print(image)
    
    MODEL.predict(tf.expand_dims(image,0))
    
    return "predicted"

if __name__ == "__main__":
    uvicorn.run(app,host='localhost',port=8000)