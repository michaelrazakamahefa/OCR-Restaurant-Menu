from PIL import Image
import pytesseract
import re
import json

# Chemin vers l'exécutable Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Assurez-vous d'ajuster le chemin selon votre installation

# Charger l'image
image = Image.open('chez-arnaud-pizza.png')  # Assurez-vous de remplacer 'test.png' par le nom réel de votre image

# Utiliser Tesseract pour faire de la reconnaissance de texte
texte_reconnu = pytesseract.image_to_string(image)

# Patron de recherche pour les prix
pattern_prix = r'(?i)(\d{1,4}([\s,.]*\d{3})*\s*(Ar|Ariary))'  # Recherche de chiffres, espaces, points, virgules et 'Ar' ou 'Ariary' (en ignorant la casse)
prix_tous = re.findall(pattern_prix, texte_reconnu)

# Convertir les prix en nombres
prix = []

for prix_str in prix_tous:
    # Nettoyer la chaîne pour ne garder que les chiffres, les points et les virgules
    prix_clean = re.sub(r'[^\d.,]', '', prix_str[0])

    # Si le prix est vide, on l'ignore
    if prix_clean:
        # Remplacer la virgule par un point si nécessaire
        prix_clean = prix_clean.replace(',', '.')

        # Convertir en nombre
        prix_float = float(prix_clean)
        prix.append(prix_float)

# Patron de recherche pour les URL
pattern_url = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
urls = re.findall(pattern_url, texte_reconnu)

# Stocker les prix et l'URL dans un fichier JavaScript
data = {
    'prices': prix,
    'url': urls[0] if urls else ''  # Prend la première URL trouvée, s'il y en a une
}

with open('data.js', 'w') as js_file:
    js_file.write(f'var extractedData = {json.dumps(data)};')

print('Données extraites et stockées dans data.js')
