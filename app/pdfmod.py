import fitz
from datetime import datetime


def convertir_couleur(entier_couleur):
    # Convertir en entier non signé 32 bits
    couleur_non_signee = entier_couleur & 0xFFFFFFFF
    
    # Extraire les composantes R, G, B (ordre dépend du PDF)
    r = (couleur_non_signee >> 16) & 0xFF  # Composante rouge
    g = (couleur_non_signee >> 8) & 0xFF   # Composante verte
    b = couleur_non_signee & 0xFF          # Composante bleue
    
    # Normaliser entre 0 et 1 (format attendu par PyMuPDF)
    return (r / 255.0, g / 255.0, b / 255.0)

def detecter_style_et_fond(pdf_path, texte_cible, page_num=0):
    """Détecte le style (police, taille, couleur) et le fond autour du texte."""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    style = {}
    
    # Extraire les propriétés du texte cible
    text_blocks = page.get_text("dict")["blocks"]
    for block in text_blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    if texte_cible in span["text"]:
                        r, g, b = convertir_couleur(span["color"])
                        style = {
                            "font": span["font"],
                            "size": span["size"],
                            "color": (r,g,b),
                            "rect": fitz.Rect(span["bbox"])
                            
                        }
                        break
    
    # Détecter la couleur de fond autour du texte
    if style:
        pix = page.get_pixmap(clip=style["rect"])
        bg_color = pix.pixel(0, 0)  # Couleur du premier pixel (fond)
        style["bg_color"] = (bg_color[0]/255, bg_color[1]/255, bg_color[2]/255)
    
    doc.close()
    return style


# print(detecter_style_et_fond("static/pdfs/devis_template.pdf","Antibes"))

def remplacer_texte_stylise(pdf_path, sortie_path, ancien_texte, nouveau_texte):
    style = detecter_style_et_fond(pdf_path, ancien_texte)
    if not style:
        raise ValueError("Texte non trouvé ou style non détecté.")
    
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Remplacer en masquant avec la couleur de fond
    page.add_redact_annot(style["rect"], fill=style["bg_color"])
    page.apply_redactions()
    
    
    is_bold = "bold" in style["font"].lower()
    font_path = "fonts/" + "NotoSans-Bold" + ".ttf" if is_bold else "fonts/NotoSans-Regular.ttf" 
    font_name = font_path.split("/")[-1].split(".")[0]
    # Insérer le nouveau texte avec le style original
    nouveau_point = fitz.Point(style["rect"].x0, style["rect"].y1 - 2)
    page.insert_text(
        nouveau_point,
        nouveau_texte,
        fontfile=font_path,
        fontname=font_name,
        fontsize=style["size"],
        color=style["color"]
    )
    
    doc.save(sortie_path)
    print(f"PDF modifié : {sortie_path}")

# Utilisation
# print(detecter_style_et_fond("app/devis_template.pdf", "$123"))
# remplacer_texte_stylise("app/devis_template.pdf","app/templatemod.pdf","$123","500€")


def remplacer_texte_stylise_liste(pdf_path, sortie_path, ancien_texte, nouveau_texte):
    """
    Remplace chaque élément de la liste `ancien_texte` par l'élément correspondant dans `nouveau_texte`.
    Les deux listes doivent être de même taille.
    """
    # Vérification des listes
    if len(ancien_texte) != len(nouveau_texte):
        raise ValueError("ancien_texte et nouveau_texte doivent être de même taille.")
    
    doc = fitz.open(pdf_path)
    page = doc[0]
    styles = []

    # Étape 1 : Détecter les styles pour tous les anciens textes
    for texte in ancien_texte:
        style = detecter_style_et_fond(pdf_path, texte)  # Utilisez la version modifiée avec `page`
        if not style:
            raise ValueError(f"Le texte '{texte}' n'a pas été trouvé dans le PDF.")
        styles.append(style)
    
    # Étape 2 : Appliquer toutes les redactions en une fois
    for style in styles:
        page.add_redact_annot(style["rect"], fill=style["bg_color"])
    page.apply_redactions()  # Applique toutes les redactions
    
    # Étape 3 : Insérer tous les nouveaux textes avec leurs styles
    for style, new_text in zip(styles, nouveau_texte):
        is_bold = "bold" in style["font"].lower()
        font_path = "fonts/" + "NotoSans-Bold" + ".ttf" if is_bold else "fonts/NotoSans-Regular.ttf" 
        font_name = font_path.split("/")[-1].split(".")[0]
        print(font_name)
        
        new_width = fitz.get_text_length(new_text, fontsize=style['size'])
        new_x0 = style['rect'].x1 - new_width - 10
        
        nouveau_point = fitz.Point(new_x0, style["rect"].y1 - 4.1)
        page.insert_text(
            nouveau_point,
            new_text,
            fontfile=font_path,
            fontname=font_name,
            fontsize=style["size"],
            color=style["color"]
        )
    
    
    # timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    # sortie_path = f"static/pdfs/devis-{timestamp}.pdf"
    doc.save(sortie_path)
    print(f"PDF modifié enregistré sous : {sortie_path}")
    
# remplacer_texte_stylise_liste("static/pdfs/devis_template.pdf","static/pdfs/devis.pdf",["$123","492","dd-mm-aaaa","Antibes", "1000 €", "700 €", "2 mm"],["500€","500€","le 25/01/2025","La zone", "1500 €", "150 €", "15 mm"])