# Image Captioning AI

This project combines Computer Vision and Natural Language Processing to generate captions for images.

## Technologies Used
- CNN (Xception)
- LSTM (RNN)
- TensorFlow / Keras

## Files
- main.py → training code
- test.py → caption generation
- model.h5 → trained model

## How to Run
```bash
python test.py

## Output
The model generates captions for input images automatically using a trained CNN + LSTM architecture.

## Note
- Captions may not always be grammatically perfect.
- This is due to the use of a basic LSTM model without attention mechanisms.
- The model is trained on a limited dataset (Flickr8k), which affects language quality.

## Model File

The trained model (`model.h5`) is not included in this repository due to GitHub file size limits.

You can:
- Train the model using `main.py`
- Or use your own trained model file