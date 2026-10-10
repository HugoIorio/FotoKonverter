import os
from PIL import Image #ImageFile
import shutil
import compressor_utils as cutils

formatos_imagens = ('.png', '.webp', '.bmp', '.avif', '.jpg', '.jpeg')

#ImageFile.LOAD_TRUNCATED_IMAGES = True

def comprimir(dir_entrada, dir_saida, **kwargs):
    quer_redimensionar = kwargs.get("quer_redimensionar", False)
    limite_maior_lado = kwargs.get("limite_maior_lado", 2147483647)
    salvar_exif = kwargs.get("salvar_exif", True)
    copiar_outros = kwargs.get("copiar_outros", True)
    qualidade = kwargs.get("qualidade", 85)
    status_compressao = kwargs.get("status_compressao", None)
    formato_alvo = kwargs.get("formato_alvo", ".jpeg")
    limite_tamanho = kwargs.get("limite_tamanho", 0) * 1024

    for arquivo_imagem in os.listdir(dir_entrada):
        nome_base, extensao = os.path.splitext(arquivo_imagem)
        caminho_entrada = os.path.join(dir_entrada, arquivo_imagem)

        if arquivo_imagem.lower().endswith(formatos_imagens):
            try:
                imagem = Image.open(caminho_entrada)
                imagem.load()

                if extensao == ".jpg":
                    extensao = ".jpeg"

                tamanho_arquivo_origem = os.path.getsize(caminho_entrada)

                deve_comprimir = tamanho_arquivo_origem >= limite_tamanho

                if formato_alvo.lower() in ('.jpeg', '.jpg'):
                    imagem = cutils.tratar_transparencia(imagem)

                caminho_saida = os.path.join(dir_saida, nome_base + formato_alvo)
                contador = 0
                while os.path.exists(caminho_saida):
                    caminho_saida = os.path.join(dir_saida, cutils.avoid_overwrite(nome_base, contador, formato_alvo))
                    contador += 1

                largura, altura = imagem.size
                maior_lado = max(largura, altura)
                if deve_comprimir and quer_redimensionar and maior_lado > limite_maior_lado:
                    imagem = cutils.redimensionar(imagem, limite_maior_lado, maior_lado, largura, altura)

                formato_salvar = formato_alvo.removeprefix(".").upper()

                qualidade_final = qualidade if deve_comprimir else 100

                save_kwargs = {
                    "format": formato_salvar,
                    "quality": qualidade_final,
                    "optimize": True
                }

                if salvar_exif:
                    try:
                        exif = imagem.getexif()
                        if exif:
                            save_kwargs["exif"] = exif
                    except Exception:
                        pass

                imagem.save(caminho_saida, **save_kwargs)
                cutils.exibir_prompt(status_compressao, arquivo_imagem, "OTIMIZADA" if deve_comprimir else "CONVERTIDA")

            except Exception as e:
                cutils.exibir_prompt(status_compressao, arquivo_imagem, f"ERRO (ARQUIVO CORROMPIDO: {e})")
                continue

        elif copiar_outros:
            caminho_saida = os.path.join(dir_saida, arquivo_imagem)
            contador = 0
            while os.path.exists(caminho_saida):
                caminho_saida = os.path.join(dir_saida, cutils.avoid_overwrite(nome_base, contador, extensao))
                contador += 1
            shutil.copyfile(caminho_entrada, caminho_saida)
            cutils.exibir_prompt(status_compressao, arquivo_imagem, "COPIADA")