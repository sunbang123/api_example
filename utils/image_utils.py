from PIL import Image
import io

def convert_image_format(image_path):
    try:
        image = Image.open(image_path)
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        image_size = image.size
        aspect_ratio = image_size[0] / image_size[1]

        max_size = 1024
        if image_size[0] > max_size or image_size[1] > max_size:
            if image_size[0] > image_size[1]:
                new_width = max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(new_height * aspect_ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)

        png_image = io.BytesIO()
        image.save(png_image, format="PNG")
        png_image.seek(0)

        return png_image

    except Exception as e:
        print(f"Error occurred while converting image: {str(e)}")
        return None