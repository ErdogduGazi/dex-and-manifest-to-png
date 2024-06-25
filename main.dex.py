import os
from PIL import Image
import numpy as np

# DEX dosyalarının bulunduğu klasörün yolu
dex_folder = "D:\\Mezuniyet Projesi\\datasets\\samples\\malware\\malwaredex"
# Görüntülerin kaydedileceği klasörün yolu
image_folder = "D:\\Mezuniyet Projesi\\datasets\\samples\\malware\\malwaredexpng"

# Görüntü boyutları (örneğin, 256x256)
image_width = 256
image_height = 256


def dex_to_feature_vector(dex_file_path, image_width, image_height):
    with open(dex_file_path, 'rb') as f:
        dex_bytes = f.read()

    # DEX dosyasının boyutu
    dex_size = len(dex_bytes)

    # Görüntüyü oluşturmak için gereken toplam piksel sayısı
    total_pixels = image_width * image_height

    # DEX dosyasını temsil eden özellik vektörünü oluştur
    # DEX dosyasının her byte'ını [0, 255] aralığına normalize et
    feature_vector = np.zeros(total_pixels)
    for i in range(min(dex_size, total_pixels)):
        feature_vector[i] = dex_bytes[i] / 255.0  # Normalize et

    # Eğer DEX dosyası daha kısa ise, özellik vektörünü sıfırlarla doldur
    if dex_size < total_pixels:
        feature_vector[dex_size:] = np.zeros(total_pixels - dex_size)

    return feature_vector


def feature_vector_to_image(feature_vector, image_width, image_height, save_path):
    # Özellik vektörünü 2 boyutlu bir diziye dönüştür
    image_array = feature_vector.reshape((image_height, image_width)) * 255

    # 2 boyutlu diziyi görüntü olarak kaydet
    image = Image.fromarray(image_array.astype(np.uint8))
    image.save(save_path)


# DEX dosyalarını işle
for filename in os.listdir(dex_folder):
    if filename.endswith(".dex"):
        dex_file_path = os.path.join(dex_folder, filename)
        image_save_path = os.path.join(image_folder, filename.replace(".dex", ".png"))

        # DEX dosyasından özellik vektörünü al
        feature_vector = dex_to_feature_vector(dex_file_path, image_width, image_height)

        # Özellik vektörünü bir görüntüye dönüştür ve kaydet
        feature_vector_to_image(feature_vector, image_width, image_height, image_save_path)