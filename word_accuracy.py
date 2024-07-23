import pytesseract
from PIL import Image
import re


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path, config=''):
    """Extract text from an image using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config=config)
    return text

def clean_text(text):
    """Clean text by removing punctuation and converting to lower case."""
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lower case
    return text

def calculate_word_level_accuracy(extracted_text, reference_text):
    """Calculate word-level accuracy."""
    extracted_words = set(clean_text(extracted_text).split())
    reference_words = set(clean_text(reference_text).split())

    correct_words = extracted_words.intersection(reference_words)
    total_words = len(reference_words)

    accuracy = len(correct_words) / total_words if total_words > 0 else 0
    return accuracy

def main(image_path, reference_text_path):
    with open(reference_text_path, 'r', encoding='utf-8') as file:
        reference_text = file.read()

    extracted_text = extract_text(image_path, config='-l deu')
    accuracy = calculate_word_level_accuracy(extracted_text, reference_text)

    print(f"Extracted Text: {extracted_text}")
    print(f"Reference Text: {reference_text}")
    print(f"Word-Level Accuracy: {accuracy:.2f}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Calculate word-level accuracy of Tesseract OCR output.')
    parser.add_argument('image_path', type=str, help='Path to the image file.')
    parser.add_argument('reference_text_path', type=str, help='Path to the reference text file.')

    args = parser.parse_args()
    main(args.image_path, args.reference_text_path)
