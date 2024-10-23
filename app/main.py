from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = FastAPI()

@app.post("/montar-imagem/")
async def montar_imagem():
    # URLs das imagens
    url_imagem1 = "https://tainanfideliscom.s3.sa-east-1.amazonaws.com/personal_tmp/image2.png"
    url_imagem2 = "https://tainanfideliscom.s3.sa-east-1.amazonaws.com/personal_tmp/image1.png"
    texto = "ENSINE MELHOR COM IA"
    
    try:
        # Carregar as imagens
        response1 = requests.get(url_imagem1)
        response2 = requests.get(url_imagem2)

        # Verifique se as respostas foram bem-sucedidas
        response1.raise_for_status()
        response2.raise_for_status()

        img1 = Image.open(BytesIO(response1.content)).convert("RGBA")
        img2 = Image.open(BytesIO(response2.content)).convert("RGBA")

        # Calcular a proporção comum
        proporcao_img1 = img1.width / img1.height
        proporcao_img2 = img2.width / img2.height

        # Definir a largura máxima e calcular a nova altura mantendo a proporção
        largura_maxima = min(img1.width, img2.width)  # Definindo largura máxima para caber em ambas
        if proporcao_img1 > proporcao_img2:
            altura_img1 = int(largura_maxima / proporcao_img1)
            altura_img2 = int(largura_maxima / proporcao_img2)
        else:
            altura_img1 = int(largura_maxima * proporcao_img1)
            altura_img2 = int(largura_maxima * proporcao_img2)

        img1 = img1.resize((largura_maxima, altura_img1), Image.ANTIALIAS)
        img2 = img2.resize((largura_maxima, altura_img2), Image.ANTIALIAS)

        # Criar uma nova imagem com a imagem 2 como fundo
        imagem_fundo = img2.convert("RGBA")

        # Colocar a imagem 1 no centro
        pos_x = (imagem_fundo.width - largura_maxima) // 2
        pos_y = (imagem_fundo.height - altura_img1) // 2
        imagem_fundo.paste(img1, (pos_x, pos_y), img1)

        # Criar um desenho para adicionar bordas e texto
        draw = ImageDraw.Draw(imagem_fundo)
        
        # Adicionar borda vermelha em volta da imagem
        draw.rectangle([0, 0, imagem_fundo.width - 1, imagem_fundo.height - 1], outline="red", width=10)

        # Usar uma fonte TrueType para aumentar o tamanho do texto
        try:
            font = ImageFont.truetype("arial.ttf", 500)  # Usando Arial como exemplo
        except IOError:
            # Caso a fonte não esteja disponível, usar a fonte padrão
            font = ImageFont.load_default()
            print("Fonte TrueType não encontrada. Usando fonte padrão.")

        text_width, text_height = draw.textsize(texto, font=font)

        # Posição do texto no topo da imagem
        text_x = (imagem_fundo.width - text_width) // 2
        text_y = 20  # Distância do topo

        # Adicionar borda vermelha em volta do texto
        border_padding = 10
        draw.rectangle([text_x - border_padding, text_y - border_padding,
                        text_x + text_width + border_padding, text_y + text_height + border_padding],
                       outline="red", width=3)

        # Adicionar texto
        draw.text((text_x, text_y), texto, fill="white", font=font)

        # Salvar imagem em um buffer
        buffer = BytesIO()
        imagem_fundo.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Erro ao acessar as imagens: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar a imagem: {str(e)}")
