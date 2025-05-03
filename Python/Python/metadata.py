from PIL import Image
import exifread

#Function to extract metadata from images
def get_metadata(image_path):
    try:

        image = Image.open(image_path)
        print(f"Formato de imagen: {image.format}")
        print(f"Tamaño de la imagen: {image.size}")
        print(f"Modo de color: {image.mode}")
        
        with open(image_path, 'rb') as img_file:
            metadata = exifread.process_file(img_file)
            
            if metadata:
                print("\nEXIF Metadata:")
                for tag, value in metadata.items():
                    print(f"{tag}: {value}")
            else:
                print("No se encontraron metadatos EXIF en la imagen.")
    
    except FileNotFoundError:
        print("Error: La imagen no se encontro. Verifica la ruta e intentalo de nuevo.")
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")

if __name__ == "__main__":
    image_path = input("Ingresa la ruta de la imagen: ")
    get_metadata(image_path)
