import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
import re
import json
import webbrowser

# Fonction pour exécuter l'extraction du texte
def extract_text():
    global texte_reconnu
    if file_path:
        # Ouvrir l'image depuis le chemin du fichier
        image = Image.open(file_path)
        
        # Utiliser Tesseract pour faire de la reconnaissance de texte
        texte_reconnu = pytesseract.image_to_string(image)

        # Afficher le texte extrait dans l'interface
        text_display.config(state="normal")
        text_display.delete(1.0, tk.END)  # Efface le texte précédent
        text_display.insert(tk.END, texte_reconnu)
        text_display.config(state="disabled")

# Fonction pour uploader une image
def upload_image():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        # Afficher le nom du fichier à côté du bouton
        filename_label.config(text=file_path)

# Fonction pour stocker les données extraites dans data.js
def store_data():
    if texte_reconnu:
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

# Fonction pour ouvrir la page web index.html
def open_webpage():
    webbrowser.open('index.html')

# Créez une fenêtre Tkinter
window = tk.Tk()
window.title("Extraction de texte depuis une image")

# Créez un cadre pour regrouper les boutons horizontalement
button_frame = tk.Frame(window)

# Créez des boutons et des étiquettes pour les actions
upload_button = tk.Button(button_frame, text="Uploader une image", command=upload_image)
extract_button = tk.Button(button_frame, text="Extraire le texte", command=extract_text)
store_button = tk.Button(button_frame, text="Stocker les données", command=store_data)
open_button = tk.Button(button_frame, text="Ouvrir la page web", command=open_webpage)
filename_label = tk.Label(window, text="", wraplength=200)  # Étiquette pour afficher le nom du fichier
text_display = tk.Text(window, state="disabled", wrap="none", height=15, width=50)  # Zone de texte pour afficher le texte extrait

# Placez les éléments dans la fenêtre
button_frame.pack()
upload_button.pack(side="left")
extract_button.pack(side="left")
store_button.pack(side="left")
open_button.pack(side="left")
filename_label.pack()
text_display.pack()

# Variable globale pour stocker le chemin du fichier et le texte extrait
file_path = None
texte_reconnu = None

# Exécutez la boucle principale de l'interface
window.mainloop()
