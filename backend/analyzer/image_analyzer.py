from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime

def extract_metadata(image_path):
    result = {
        'filename': os.path.basename(image_path),
        'file_size_kb': None,
        'format': None,
        'dimensions': None,
        'has_exif': False,
        'camera_make': None,
        'camera_model': None,
        'date_taken': None,
        'gps_location': None,
        'software': None,
        'suspicious': False,
        'suspicious_reasons': []
    }

    try:
        img = Image.open(image_path)
        result['format'] = img.format
        result['dimensions'] = f"{img.width}x{img.height}"
        result['file_size_kb'] = round(os.path.getsize(image_path) / 1024, 2)

        # Extract EXIF data
        exif_data = img._getexif()
        if exif_data:
            result['has_exif'] = True
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'Make':
                    result['camera_make'] = value
                elif tag == 'Model':
                    result['camera_model'] = value
                elif tag == 'DateTime':
                    result['date_taken'] = value
                elif tag == 'Software':
                    result['software'] = str(value)

        # Check for suspicious signs
        if result['software']:
            suspicious_software = ['photoshop', 'gimp', 'lightroom', 'affinity']
            if any(s in result['software'].lower() for s in suspicious_software):
                result['suspicious'] = True
                result['suspicious_reasons'].append(
                    f"Edited with: {result['software']}"
                )

        if not result['has_exif']:
            result['suspicious_reasons'].append("No EXIF data — metadata may have been stripped")

    except Exception as e:
        result['error'] = str(e)

    return result

if __name__ == '__main__':
    # Test with a sample image
    import sys
    if len(sys.argv) > 1:
        print(extract_metadata(sys.argv[1]))
    else:
        print("Usage: python image_analyzer.py <image_path>")
        print("Image analyzer ready! ✅")