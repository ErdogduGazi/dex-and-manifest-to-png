import os
from PIL import Image
import numpy as np

# Manifest dosyalarının bulunduğu klasörün yolu
manifest_folder = "D:\\Mezuniyet Projesi\\datasets\\samples\\benign\\benignmanifest"
# Görüntülerin kaydedileceği klasörün yolu
image_folder = "D:\\Mezuniyet Projesi\\datasets\\samples\\benign\\beningmanifestpng"

# Görüntü boyutları (örneğin, 256x256)
image_width = 256
image_height = 256


def manifest_to_feature_vector(manifest_file_path, image_width, image_height):
    with open(manifest_file_path, 'r', encoding='latin-1') as f:
        manifest_text = f.read()

    # Manifest dosyasının boyutu
    manifest_size = len(manifest_text)

    # Görüntüyü oluşturmak için gereken toplam piksel sayısı
    total_pixels = image_width * image_height

    # Manifest dosyasını temsil eden özellik vektörünü oluştur
    # Manifest dosyasının her karakterini [0, 255] aralığına normalize et
    feature_vector = np.zeros(total_pixels)
    for i in range(min(manifest_size, total_pixels)):
        feature_vector[i] = ord(manifest_text[i]) / 255.0  # Normalize et

    # Eğer manifest dosyası daha kısa ise, özellik vektörünü sıfırlarla doldur
    if manifest_size < total_pixels:
        feature_vector[manifest_size:] = np.zeros(total_pixels - manifest_size)

    return feature_vector


def feature_vector_to_image(feature_vector, image_width, image_height, save_path):
    # Özellik vektörünü 2 boyutlu bir diziye dönüştür
    image_array = feature_vector.reshape((image_height, image_width)) * 255

    # 2 boyutlu diziyi görüntü olarak kaydet
    image = Image.fromarray(image_array.astype(np.uint8))
    image.save(save_path)


# Manifest dosyalarını işle
for filename in os.listdir(manifest_folder):
    if filename.endswith(".xml"):
        manifest_file_path = os.path.join(manifest_folder, filename)
        image_save_path = os.path.join(image_folder, filename.replace(".xml", ".png"))

        # Manifest dosyasından özellik vektörünü al
        feature_vector = manifest_to_feature_vector(manifest_file_path, image_width, image_height)

        # Özellik vektörünü bir görüntüye dönüştür ve kaydet
        feature_vector_to_image(feature_vector, image_width, image_height, image_save_path)