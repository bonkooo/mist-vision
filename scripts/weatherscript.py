# weather_detect_image_out.py
import torch
from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image, ImageDraw, ImageFont
import sys
import os

MODEL = "prithivMLmods/Weather-Image-Classification"

id2label = {
    0: "cloudy/overcast",
    1: "foggy/hazy",
    2: "rain/storm",
    3: "snow/frosty",
    4: "sun/clear"
}

def main(input_path, output_path):
    # Load image
    if not os.path.exists(input_path):
        print(f"Input image not found: {input_path}")
        sys.exit(1)

    img = Image.open(input_path).convert("RGB")

    # Load model + processor
    print("Loading model (first time may download weights)...")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = SiglipForImageClassification.from_pretrained(MODEL).to(device)
    processor = AutoImageProcessor.from_pretrained(MODEL)

    # Preprocess & forward
    inputs = processor(images=img, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0].cpu()

    # Best prediction
    pred_idx = int(torch.argmax(probs).item())
    pred_label = id2label[pred_idx]
    pred_conf = float(probs[pred_idx].item())

    print(f"Predicted weather: {pred_label} ({pred_conf:.3f})")

    # Draw label on image
    draw = ImageDraw.Draw(img)
    text = f"{pred_label} ({pred_conf:.2f})"

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    margin = 8
    rect_x0, rect_y0 = 10, 10
    rect_x1 = rect_x0 + text_w + margin * 2
    rect_y1 = rect_y0 + text_h + margin * 2

    draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=(255, 255, 0, 200))
    draw.text((rect_x0 + margin, rect_y0 + margin), text, fill="black", font=font)

    # Save image
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path)

    print(f"Saved output image to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python weather_detect_image_out.py <input_image> <output_image>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
