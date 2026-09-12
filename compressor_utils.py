from PIL import Image

#def converter_formato(formato_alvo, nome_base) - desenvolver isso quando possível

def avoid_overwrite(name_file, counter, img_format):
    new_name = name_file + "_" + str(counter) + img_format
    return new_name


def exibir_prompt(status_processamento, nome_arquivo, tipo_processamento):
    status_processamento.configure(state="normal")
    status_processamento.insert("end", f"[{tipo_processamento}] {nome_arquivo}\n")  # exibe na interface a mensagem ao usuário
    status_processamento.see("end")  # rolar textbox para baixo
    status_processamento.configure(state="disabled")
    status_processamento.update_idletasks()


def redimensionar(imagem, limite_maior_lado, maior_lado, largura, altura):
    proporcao = limite_maior_lado / maior_lado
    nova_largura = int(largura * proporcao)
    nova_altura = int(altura * proporcao)
    imagem = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)
    return imagem


def tratar_transparencia(imagem):
    if imagem.mode in ('RGBA', 'LA') or (imagem.mode == 'P' and 'transparency' in imagem.info): # remover transparência, se houver
        imagem_rgba = imagem.convert('RGBA')
        fundo_branco = Image.new('RGB', imagem.size, (255, 255, 255))
        fundo_branco.paste(imagem_rgba, (0, 0), imagem_rgba)
        imagem_final = fundo_branco

    else: # apenas converter para formato de cores RGB
        imagem_final = imagem.convert('RGB')

    return imagem_final


