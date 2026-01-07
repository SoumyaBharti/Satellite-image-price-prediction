This project predicts house prices by combining satellite imagery and structured tabular features using a multimodal deep learning approach.
A pretrained ResNet extracts visual features from satellite images, while a fully connected neural network processes tabular data. The fused representation is used to predict log-transformed house prices.

Project Overview

  Traditional house price models rely only on structured data (e.g., number of bedrooms, square footage).
  This project enhances prediction accuracy by incorporating satellite images, allowing the model to learn:

  Neighborhood layout
  
  Surrounding infrastructure
  
  Environmental and spatial context

Model Architecture
  Image Encoder
  
    Backbone: Pretrained ResNet (ResNet50 / ResNet101)
    
    Final classification layer removed
    
    Output embedding size: 2048
  
  CNN head:
  
    Linear(2048 → 256) + SiLU + Dropout
    
    Tabular Encoder
    
    Fully connected network
  
  Architecture:
  
    Input → 128 → 64 → 32
    
    SiLU activations
    
    Batch Normalization
    
    Dropout for regularization
    
    Feature Fusion
    
    Image and tabular embeddings are concatenated
    
    A learnable parameter α (alpha) balances image and tabular contributions
    
    Regression Head
  
  Architecture:
  
    (256 + 32) → 256 → 128 → 1
    
    Dropout applied
  
    Final output predicts log(price)

Dataset
  Inputs
  
    Satellite images (RGB, resized to 224×224)
    
    Tabular features:
    
    bedrooms, bathrooms
    
    sqft_living, sqft_lot
    
    floors, waterfront
    
    view, condition, grade
    
    sqft_above, sqft_basement
    
    latitude, longitude
  
  Target
  
    log(price) (log-transformed for stability)

Data Preprocessing
  Images
  
    Resize to 224 × 224
    
    Normalize using ImageNet statistics
    
    Training-time augmentation:
    
    Random horizontal flip
    
    Random rotation
    
    Color jitter
  
  Tabular Data
  
    Standardized using StandardScaler
    
    Converted to float32

Training Details

  Loss Function: Smooth L1 Loss (Huber Loss)
  
  Optimizer: Adam
  
  Learning Rate Scheduler: ReduceLROnPlateau
  
  Gradient clipping applied
  
  CNN backbone initially frozen, optionally fine-tuned later
  
  Device: GPU (CUDA) / CPU

Evaluation Metrics

  R² Score
  
  Mean Absolute Error (MAE)
  
  Root Mean Squared Error (RMSE)

Model Interpretability

  Grad-CAM is used to visualize which regions of satellite images influence predictions.
  
  Helps verify that the model focuses on meaningful spatial features (roads, buildings, neighborhoods).
