import requests
from PIL import Image
from models.image_editing import ImageEditorProxy

class ImageEditingController:
    def __init__(self, view):
        self.view = view
        self.image_path = None

    def set_image_path(self, image_path):
        self.image_path = image_path

    async def edit_image(self):
        if not self.image_path:
            return

        api_key = self.view.api_key_entry.get().strip()
        if not api_key:
            self.view.show_warning("API Key Missing", "Please enter your OpenAI API key.")
            return

        user_prompt = self.view.prompt_entry.get().strip()
        if not user_prompt:
            self.view.show_warning("User Prompt Missing", "Please enter your prompt.")
            return

        mask = self.view.get_mask()

        image_editor = ImageEditorProxy(api_key)

        edited_image_url = await image_editor.edit(self.image_path, mask, user_prompt)
        if not edited_image_url:
            return

        image = Image.open(requests.get(edited_image_url, stream=True).raw)
        self.view.show_image_in_new_window(image)
