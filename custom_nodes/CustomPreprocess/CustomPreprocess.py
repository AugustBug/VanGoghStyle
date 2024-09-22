import torch
import torchvision.transforms as transforms
from PIL import Image, ImageOps, ImageFilter
import numpy as np

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
    
# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
    
    
class CustomPreprocess:
    CATEGORY = "PreProcess"

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "image": ("IMAGE",),
                "baseResolution": ("INT", {"default": 512, "min": 1, "max": 4096, "step": 8}),
                "applyPadding": ("BOOLEAN", {"default": False, "widget": "checkbox"}),
                "applyEqualization": ("BOOLEAN", {"default": False, "widget": "checkbox"}),
                "gaussianBlur": ("FLOAT", {"default": 0, "min": 0, "max": 50, "step": 0.2}),
            }
        }

    RETURN_TYPES = ("IMAGE", "FLOAT", "INT", "INT",)
    FUNCTION = "preprocessImage"
    
    @classmethod
    def VALIDATE_INPUTS(self, baseResolution):
        if(baseResolution < 48):
            return f"baseResolution({baseResolution}) is smaller than expected"
        elif(baseResolution > 4096):
            return f"baseResolution({baseResolution}) is larger than expected"
            
        return True

    def preprocessImage(self, image, baseResolution, applyPadding, applyEqualization, gaussianBlur):
        # check inputs validity
        validity = self.VALIDATE_INPUTS(baseResolution)
        if(validity != True):
            raise Exception(validity)
            
        # get image information
        batch_size, height, width, channels = image.size()
        #print(f"batch_size {batch_size}, channels {channels}, height {height}, width {width}")
        if(width < 48 or height < 48):
            raise Exception("image is too small for operation")
        if(width > 8192 or height > 8192):
            raise Exception("image is too large for operation")
            
        # resize the image to fit baseResolution, apply horizontal based or vertical based resizing depending on the widht/height ratio
        desiredHeight = baseResolution
        desiredWidth = baseResolution
        # scale coef is for resizing image back to original size, this will be used on postprocess phase to resize the image
        scaleCoef = 1
        if(height > width):
            desiredWidth = (int) (baseResolution * width / height)
            scaleCoef = height / baseResolution
        else:
            desiredHeight = (int) (baseResolution * height / width)
            scaleCoef = width / baseResolution
        
        print(f"scale coefficient : {scaleCoef}")
        # convert to PIL image for manipulation
        pilImage = tensor2pil(image)
        
        # Resampling = 'nearest': 0, 'lanczos': 1, 'bilinear': 2, 'bicubic': 3,
        resultImage = pilImage.resize((desiredWidth, desiredHeight), resample=Image.Resampling(3))
        
        # apply padding if selected
        if(applyPadding):
            right = 0
            left = 0
            top = 0
            bottom = 0
            if(desiredWidth > desiredHeight):
                top = (int)((desiredWidth - desiredHeight) / 2)
                bottom = desiredWidth - desiredHeight - top
                desiredHeight = desiredWidth
            elif(desiredHeight > desiredWidth):
                left = (int)((desiredHeight - desiredWidth) / 2)
                right = desiredHeight - desiredWidth - left
                desiredWidth = desiredHeight
                
            # fill with white
            paddedImage = Image.new(resultImage.mode, (desiredWidth, desiredHeight), (255, 255, 255)) 
            paddedImage.paste(resultImage, (left, top)) 
            resultImage = paddedImage
            
        # apply equalization if selected
        if(applyEqualization):
            resultImage = ImageOps.equalize(resultImage, mask = None)
            
        # apply gaussian blur if selected
        if(gaussianBlur > 0):
            resultImage = resultImage.filter(ImageFilter.GaussianBlur(radius=gaussianBlur))
        
        # convert back to tensor
        ppImage = pil2tensor(resultImage)
        
        print(f"Resolution of New Image: {desiredWidth} * {desiredHeight}")
        
        return (ppImage, scaleCoef, desiredWidth, desiredHeight)