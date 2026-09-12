import os # biblioteca para manipulação de recursos do sistema operacional - usar receber caminho de arquivos
from PIL import Image # biblioteca para manipulação de imagens
import shutil # biblioteca para copiar arquivos sem alterar dados
import compressor_utils as cutils # favor desenvolver função para conversão de formatos de imagem quando possível nessa biblioteca, isto deveria ser opcional, e não o padrão

formatos_imagens = ('.png', '.webp', '.bmp', '.avif', '.jpg', '.jpeg') # formats taken as images


def comprimir(dir_entrada, dir_saida, quer_redimensionar, limite_maior_lado, converter_outros, salvar_exif, copiar_outros, qualidade, status_compressao, formato_alvo):

    for image_file in os.listdir(dir_entrada):

        base_name, extension = os.path.splitext(image_file)  # separat file name from extension
        input_path = os.path.join(dir_entrada, image_file)

        if image_file.lower().endswith(formatos_imagens):  # check if image_file is, in fact, an image

            if extension == ".jpg": 
                extension = ".jpeg"

            imagem = Image.open(input_path)

            if extension == formato_alvo:

                caminho_saida = os.path.join(dir_saida, image_file)

                counter = 0

                while os.path.exists(caminho_saida):
                    caminho_saida =  os.path.join(dir_saida, cutils.avoid_overwrite(base_name, counter, formato_alvo))
                    counter += 1

                if formato_alvo == ".jpeg":
                    imagem = cutils.tratar_transparencia(imagem)

                largura, altura = imagem.size
                maior_lado = max(largura, altura)

                if quer_redimensionar and maior_lado > limite_maior_lado:
                    imagem = cutils.redimensionar(imagem, limite_maior_lado, maior_lado, largura, altura)  # redimensiona a imagem

                formato_salvar = formato_alvo.removeprefix(".").upper()  # adaptar formato para salvar image_file corretamente

                if salvar_exif:  # se o usuário quiser salvar metadados

                    exif = imagem.getexif()

                    imagem.save(
                        caminho_saida,
                        formato_salvar,
                        quality=qualidade,
                        optimize=True,
                        exif=exif
                    )

                else:

                    imagem.save(
                        caminho_saida,
                        formato_salvar,
                        quality=qualidade,
                        optimize=True
                    )

                cutils.exibir_prompt(status_compressao, image_file, "OTIMIZADA")

            else:

                caminho_saida = os.path.join(dir_saida, base_name + formato_alvo)

                counter = 0

                while os.path.exists(caminho_saida):
                    caminho_saida = os.path.join(dir_saida, cutils.avoid_overwrite(base_name, counter, formato_alvo))
                    counter += 1

                if converter_outros:
                    if formato_alvo == ".jpeg":
                        imagem = cutils.tratar_transparencia(imagem)

                    largura, altura = imagem.size
                    maior_lado = max(largura, altura)

                    if quer_redimensionar and maior_lado > limite_maior_lado:
                        imagem = cutils.redimensionar(imagem, limite_maior_lado, maior_lado, largura, altura)  # redimensiona a imagem

                    formato_salvar = formato_alvo.removeprefix(".").upper()  # adaptar formato para salvar image_file corretamente

                    if salvar_exif:  # se o usuário quiser salvar metadados

                        exif = imagem.getexif()

                        imagem.save(
                            caminho_saida,
                            formato_salvar,
                            quality=qualidade,
                            optimize=True,
                            exif=exif
                        )

                    else:

                        imagem.save(
                            caminho_saida,
                            formato_salvar,
                            quality=qualidade,
                            optimize=True
                        )

                    cutils.exibir_prompt(status_compressao, image_file, "OTIMIZADA")

                elif copiar_outros:
                    caminho_saida = os.path.join(dir_saida, image_file)
                    counter = 0
                    while os.path.exists(caminho_saida):
                        caminho_saida = os.path.join(dir_saida, cutils.avoid_overwrite(base_name, counter, extension))
                        counter += 1
                    shutil.copyfile(input_path, caminho_saida)
                    cutils.exibir_prompt(status_compressao, image_file, "COPIADA")

        else:

            if copiar_outros:
                caminho_saida = os.path.join(dir_saida, image_file)
                shutil.copyfile(input_path, caminho_saida)
                cutils.exibir_prompt(status_compressao, image_file, "COPIADA")