import zipfile
import os

# Create dummy XML if missing
os.makedirs('annotations', exist_ok=True)
with open('annotations/Alice.xml', 'w') as f:
    f.write('<root><image name="road_01.jpg"><tag label="complex_urban" /><tag label="night_dark" /><tag label="blurred" /></image></root>')

with open('annotations/Bob.xml', 'w') as f:
    f.write('<root><image name="road_01.jpg"><tag label="complex_highway" /><tag label="night_dark" /></image></root>')

# Create Zips
with zipfile.ZipFile('annotations/Alice_Zip.zip', 'w') as z:
    z.write('annotations/Alice.xml', arcname='Alice_annotation.xml')

with zipfile.ZipFile('annotations/Bob_Zip.zip', 'w') as z:
    z.write('annotations/Bob.xml', arcname='inner/Bob_annotation.xml')

# Remove initial xmls to test zip extraction
os.remove('annotations/Alice.xml')
os.remove('annotations/Bob.xml')
print("✅ Created Alice_Zip.zip and Bob_Zip.zip")
