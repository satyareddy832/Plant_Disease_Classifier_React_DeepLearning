// src/ImageUpload.js
import React, { useState } from 'react';
import './ImageUpload.css';

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewSrc, setPreviewSrc] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setResult(null);
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewSrc(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setSelectedFile(null);
    setPreviewSrc(null);
    setResult(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Please select an image file first");
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    console.log(selectedFile.type)

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      console.log(data)
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="image-upload-container">
      <form onSubmit={handleSubmit}>
        {!previewSrc && (
          <label className="custom-file-input">
            Choose Image
            <input type="file" accept="image/*" onChange={handleFileChange} />
          </label>
        )}
        {previewSrc && (
          <>
            <img src={previewSrc} alt="Image Preview" className="image-preview" />
            <div className="change-remove-buttons">
              <label className="custom-file-input change-button">
                Change
                <input type="file" className='change-button' accept="image/*" onChange={handleFileChange} />
              </label>
              <button type="button" className="remove-button" onClick={handleRemoveImage}>
                Remove
              </button>
            </div>
          </>
        )}
        <button type="submit">Upload and Predict</button>
      </form>
      {result && (
        <div className="result">
          <h3>Prediction Result</h3>
          <p><strong>Prediction:</strong> {result.class}</p>
          <p><strong>Confidence:</strong> {result.confidence}</p>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
