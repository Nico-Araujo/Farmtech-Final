import os
import sys

# Tenta importar o YOLO.
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ AVISO: Biblioteca 'ultralytics' não encontrada. Instalando modo de simulação.")

# --- CONFIGURAÇÕES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'assets', 'best.pt')

def carregar_modelo():
    """Tenta carregar o modelo YOLO."""
    if not YOLO_AVAILABLE:
        return None
    
    if os.path.exists(MODEL_PATH):
        try:
            # Carrega o modelo
            model = YOLO(MODEL_PATH)
            
            # --- ADAPTAÇÃO PARA AGRICULTURA (TRADUÇÃO DE CLASSES) ---
            # O modelo COCO detecta 'person', 'truck', 'car'.
            # Vamos traduzir isso para o contexto da fazenda.
            
            novos_nomes = {
                0: 'Agricultor / Pessoa',      # ID 0 = person
                2: 'Veículo / Trator',         # ID 2 = car
                7: 'Maquinário Pesado',        # ID 7 = truck
                5: 'Maquinário / Ônibus',      # ID 5 = bus
                1: 'Bicicleta / Moto',         # ID 1 = bicycle
                
                # Mantemos os animais caso apareçam (segurança contra invasão)
                16: 'Animal (Cachorro)',
                17: 'Animal (Gato)',
                21: 'Animal Silvestre (Urso)', 
                22: 'Animal Silvestre'
            }
            
            # Atualiza os nomes no modelo
            for id_classe, novo_nome in novos_nomes.items():
                if id_classe in model.names:
                    model.names[id_classe] = novo_nome
                    
            return model
        except Exception as e:
            print(f"Erro ao carregar modelo .pt: {e}")
            return None
    return None

def processar_imagem(caminho_imagem_ou_pil):
    """
    Processa a imagem focando em SEGURANÇA e ATIVOS.
    """
    model = carregar_modelo()
    
    # --- CENÁRIO 1: YOLO Funcionando ---
    if model:
        try:
            # Confiança de 0.25 (padrão) para evitar falsos positivos malucos
            results = model(caminho_imagem_ou_pil, conf=0.25)
            
            # Desenha as caixas com os nomes traduzidos
            img_resultado_array = results[0].plot() 
            
            # Gera o relatório de texto
            contagem = {}
            detectou_algo = False
            
            for box in results[0].boxes:
                detectou_algo = True
                cls_id = int(box.cls[0])
                nome_classe = model.names[cls_id]
                
                contagem[nome_classe] = contagem.get(nome_classe, 0) + 1
            
            if detectou_algo:
                resumo = ", ".join([f"{qtd}x {nome}" for nome, qtd in contagem.items()])
                # Mensagem focada em monitoramento
                msg = f"📍 Monitoramento: {resumo} identificado(s) na área."
            else:
                msg = "✅ Área limpa. Nenhum agricultor ou maquinário detectado."
                
            return img_resultado_array, msg
            
        except Exception as e:
            print(f"Erro na inferência YOLO: {e}")
            
    # --- CENÁRIO 2: Simulação / Falha ---
    import numpy as np
    from PIL import Image
    
    if hasattr(caminho_imagem_ou_pil, 'convert'):
         img_resultado_array = np.array(caminho_imagem_ou_pil)
    else:
         try:
             img = Image.open(caminho_imagem_ou_pil)
             img_resultado_array = np.array(img)
         except:
             return None, "Erro ao abrir imagem."

    aviso = "⚠️ Modo Simulação (Modelo não carregado)"
    return img_resultado_array, aviso