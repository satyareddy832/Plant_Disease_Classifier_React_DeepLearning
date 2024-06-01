from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np 
from io import BytesIO
from PIL import Image

import tensorflow as tf

app=FastAPI()

model_version = 1
MODEL = tf.keras.models.load_model("./saved_models/Model.h5")


# img = np.array(Image.open(r"C:\Code\Potato-Disease\api\leaf.JPG"))
# img = np.expand_dims(img, 0)
# print(img.shape)
# print(MODEL.predict(img, verbose=0))

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
    image=tf.expand_dims(image,0)
    print(type(image))
    print(image.shape)
   
    prediction=MODEL.predict(image, verbose=0)
    predicted_class=CLASS_NAMES[np.argmax(prediction[0])]
    confidence=round(100*(np.max(prediction[0])),2)
    return {
        'class':predicted_class,
        'confidence':confidence
    }

if __name__ == "__main__":
    uvicorn.run(app,host='localhost',port=8000)