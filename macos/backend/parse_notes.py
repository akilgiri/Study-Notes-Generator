# Qwen2.5VL model (https://github.com/QwenLM/Qwen2.5-VL/blob/main/cookbooks/document_parsing.ipynb)
# Marker (https://github.com/VikParuchuri/marker)

# from marker.converters.pdf import PdfConverter
# from marker.models import create_model_dict
# from marker.output import text_from_rendered

# from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
# from qwen_vl_utils import process_vision_info

import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

from pdf2image import convert_from_path
import os
# from PIL import Image

# Trying Marker
# def parse_pdf():
#     converter = PdfConverter(
#         artifact_dict=create_model_dict(),
#     )

#     rendered = converter("../study_data/04a-regex2dfa.pdf")
#     text, _, images = text_from_rendered(rendered)

#     print(f"Text: {text}")

#     print(f"_: {_}")

#     print(f"Images: {images}")

#     with open("../study_data/04a-regex2dfa.md", "w") as f:
#         f.write(text + "\n")


def parse_handwriting(output_folder, pdf_path):
    # Load the model
    model_path = "mlx-community/Qwen2.5-VL-3B-Instruct-4bit"
    model, processor = load(model_path)
    config = load_config(model_path)

    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    pdf_name = os.path.split(pdf_path)[-1].replace(".pdf", "")

    # Convert pdf to images
    print("Converting pdf to images...")
    images = convert_from_path(pdf_path)
    image_files = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"{pdf_name}_{i}.jpg")
        image.save(image_path, "JPEG")
        print(f"Image saved at {image_path}")
        image_files.append(image_path)

    # image = image_files
    output_path = os.path.join(output_folder, f"{pdf_name}.md")

    # Iterate over each image and generate notes
    for image in image_files:
        print("Processing Image: ", image)
        prompt = "Create notes based on the information in the provided image. If an image contains structured information such as flowcharts or diagrams, explain it."
        # prompt = "If the provided image contains structured information such as flowcharts or diagrams, explain it. Otherwise extract the text from the image."
        use_image = [image]
        # Apply chat template
        formatted_prompt = apply_chat_template(
            processor, config, prompt, num_images=len(use_image)
        )

        # Generate output
        output = generate(model, processor, formatted_prompt, use_image, verbose=False)
        print(output)

        # Save notes to output folder
        with open(output_path, "a") as f:
            f.write(output)


# if __name__ == "__main__":
#     # parse_pdf()
#     parse_handwriting("/Users/akil/Documents/Coding Projects/WatAI/Onboarding Task/Study Helper Bot/study_data/test_output7", "/Users/akil/Documents/Coding Projects/WatAI/Onboarding Task/Study Helper Bot/study_data/04a-regex2dfa.pdf")
