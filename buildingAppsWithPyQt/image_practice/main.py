from PIL import Image, ImageFilter, ImageEnhance

with Image.open('/Users/balogunishaq/Desktop/Python Zero to Knowing Tutorial/buildingAppsWithPyQt/image_practice/customers.png') as picture:
    # picture.show()
    
    black_white = picture.convert("L")
    black_white.save("gray.png")
    
    mirror = picture.transpose(Image.FLIP_LEFT_RIGHT)
    mirror.save("mirror.png")
    
    blur = picture.filter(ImageFilter.BLUR)
    blur.save("blur.png")
    
    # Image Enhance
    contrast = ImageEnhance.Contrast(picture)
    contrast = contrast.enhance(2.5)
    contrast.save("contrast.png")
    
    color = ImageEnhance.Color(picture).enhance(2.5)
    color.save("color.png")