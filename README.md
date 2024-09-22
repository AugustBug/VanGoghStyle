
# Van Gogh Style ComfyUI Workflow

This project contains a custom workflow for converting images to Van Gogh Style, built on top of **ComfyUI**, along with custom nodes to extend functionality. It includes additional models and configurations to enhance your image generation and processing capabilities.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Set Up Conda Environment](#1-set-up-conda-environment)
  - [2. Install Dependencies](#2-install-dependencies)
  - [3. Install ComfyUI](#3-install-comfyui)
  - [4. Install ComfyUI Manager](#4-install-comfyui-manager)
  - [5. Download and Place Required Files](#5-download-and-place-required-files)
  - [6. Install Custom Nodes](#6-install-custom-nodes)
- [Usage](#usage)
- [Explanation](#explanation)

## Introduction

This workflow enhances ComfyUI by adding custom nodes and integrating additional models for advanced image processing and generation. Whether you're looking to perform complex image manipulations or generate high-quality visuals, this setup provides the tools you need.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: Version 3.10 or later
- **Conda**: [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)
- **NVIDIA GPU**: For CUDA support (optional but recommended for accelerated performance)
- **Git**: Installed and configured on your system

## Installation

Follow these steps to set up the Van Gogh Style ComfyUI workflow with all necessary components.

### 1. Set Up Conda Environment

1. **Create a New Conda Environment**:

   Open your terminal (Anaconda Prompt or Command Prompt) and run:

   ```bash
   conda create -n vangogh-env python=3.10
   ```

2. **Activate the Conda Environment**:

   ```bash
   conda activate vangogh-env
   ```

### 2. Install Dependencies

1. **Clone Your Project Repository** (if applicable):

   ```bash
   git clone https://github.com/AugustBug/VanGoghStyle.git
   cd VanGoghStyle
   ```

### 3. Install ComfyUI

1. **Clone the ComfyUI Repository**:

   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI.git
   ```

2. **Navigate to the ComfyUI Directory**:

   ```bash
   cd ComfyUI
   ```

3. **Install ComfyUI Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the ComfyUI Server**:

   ```bash
   python main.py
   ```

   ComfyUI should now be running on [http://localhost:8188](http://localhost:8188).

### 4. Install ComfyUI Manager

1. **Clone the ComfyUI Manager Repository**:

   ```bash
   git clone https://github.com/ltdrdata/ComfyUI-Manager.git
   ```

2. **Move the Manager to ComfyUI's Custom Nodes Directory**:

   ```bash
   mv ComfyUI-Manager /VanGoghStyle/ComfyUI/custom_nodes/
   ```

3. **Restart the ComfyUI Server**:

   This ensures that ComfyUI Manager is loaded correctly.

### 5. Download and Place Required Files

Some additional models and configuration files are required for the workflow to function properly. Follow these steps to download and place them in the correct directories.

1. **Download Required Files**:

   - **ControlNet Models**:
     - [control_sd15_canny.pth](https://huggingface.co/lllyasviel/ControlNet/blob/main/models/control_sd15_canny.pth)

   - **Checkpoint Models**:
     - [stableDiffusionV15Bf16Fp16NoEma_v15NoEma.safetensors](https://civitai.com/models/155256/stable-diffusion-v15-bf16fp16-no-emaema-only-no-vae-safetensors-checkpoint)
	 
   - **LoRA Models**:
     - [Painting.safetensors](https://civitai.com/models/154185/van-gogh-likeness)
	 
   - **VAE Models**:
     - [vae-ft-mse-840000-ema-pruned.safetensors](https://huggingface.co/stabilityai/sd-vae-ft-mse-original/blob/main/vae-ft-mse-840000-ema-pruned.safetensors)

2. **Move the Downloaded Files to Corresponding Directories**:

   ```bash
   mv path/to/downloaded/control_sd15_canny.pth /VanGoghStyle/ComfyUI/models/controlnet/
   ```
   
   
   ```bash
   mv path/to/downloaded/stableDiffusionV15Bf16Fp16NoEma_v15NoEma.safetensors /VanGoghStyle/ComfyUI/models/checkpoints/
   ```
   
   
   ```bash
   mv path/to/downloaded/Painting.safetensors /VanGoghStyle/ComfyUI/models/loras/
   ```
   
   
   ```bash
   mv path/to/downloaded/vae-ft-mse-840000-ema-pruned.safetensors /VanGoghStyle/ComfyUI/models/vae/
   ```


### 6. Install Custom Nodes

1. **Place Custom Node Files in ComfyUI's Custom Nodes Directory**:

   ```bash
   cp -r /custom_nodes/CustomPreprocess /ComfyUI/custom_nodes/
   ```

   ```bash
   cp -r /models/embeddings/EasyNegative.safetensors /ComfyUI/models/embeddings
   ```

2. **Restart the ComfyUI Server**:

   This will load your custom nodes into the ComfyUI interface.

## Usage

Once all components are installed and configured:

1. **Launch ComfyUI**:

   Ensure the ComfyUI server is running. If not, start it with:

   ```bash
   cd ComfyUI
   python main.py
   ```

2. **Access the ComfyUI Interface**:

   Open your web browser and navigate to [http://localhost:8188](http://localhost:8188).

3. **Load Van Gogh Style Workflow**:

   - Drag and drop *vangogh.json* into the workflow editor.
   - Install missing custom nodes by clicking *Manager* button and then *Install Missing Custom Nodes* button in the pop up window.
   - Click *Restart* button after manually install all of the missing nodes.
   - After restart you will view an indicator that the server restarted, now you are free to run the workflow
   
4. **Run Van Gogh Style Workflow**

   - use *choose file to upload* button on Load Image component to load an image(you can use the images on **testImages** folder).
   - use *Queue Prompt* button to run the workflow
   - you can view the result on SaveImage component if everything is ok. the result image will be saved under **output** folder



## Explanation
This workflow uses ControlNet to detect the images structure and Stable Diffusion 1.5 to create images. It uses Canny Edges to represent the outline of the image. 

Van Gogh Style is taken from Painting LoRA which is trained using Van Gogh Paintings. 

For positive prompt it uses WD14 Tagger and creates tags from image and appends keywords to be able to use Painting LoRA effectively.
Some negative prompts are also provided to prevent the model to produce meaningless and low quality outputs.

Some images may need preprocessing steps. For this purpose a CustomPreprocess module is developed. The module takes an image as input and resize it to fit 512 pixels that Stable Diffusion model performs best.
It also has options to appply padding (by adding white pixels around to make the image 512x512), apply equalization (to equalize the intensity levels of the image) and apply Gaussian blur.
This preprocessing component outputs a scale factor for resizing the processed image back to the original resolution. It is used for Upscale Image component to resize the image back.

Some steps use PreviewImage components to track the progress alongside the workflow. And the final image is saved under *output* folder.

## Sample Outputs

**Test-2**
![Input](testImages/test2.jpg?raw=true "Test-2")  ![Input](output/VanGoghStyle_00070_.png?raw=true "Test-2")


**Test-5**
![Input](testImages/test5.jpeg?raw=true "Test-2")  ![Input](output/VanGoghStyle_00037_.png?raw=true "Test-2")


**Test-8**
![Input](testImages/test8.jpg?raw=true "Test-2")  ![Input](output/VanGoghStyle_00045_.png?raw=true "Test-2")


**Test-7**
![Input](testImages/test7.jpg?raw=true "Test-2")  ![Input](output/VanGoghStyle_00041_.png?raw=true "Test-2")


**Test-13**
![Input](testImages/test13.jpg?raw=true "Test-2")  ![Input](output/VanGoghStyle_00086_.png?raw=true "Test-2")


**Test-6**
![Input](testImages/test6.png?raw=true "Test-2")  ![Input](output/VanGoghStyle_00063_.png?raw=true "Test-2")
