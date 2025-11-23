import pandas as pd
import random
import os

# --- CONFIGURAÇÃO DOS CAMINHOS ---
# O sistema tenta achar o CSV na pasta raiz. Se não achar, usa o modo SIMULAÇÃO.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '..', 'dados_sensores_simulados.csv')

def get_dados_sensores():
    """
    Função principal chamada pelo Dashboard.
    Retorna um dicionário com dados da MÁQUINA e do SOLO.
    """
    dados = {}
    
    # --- 1. DADOS DA MÁQUINA (Bomba de Irrigação) ---
    # Tenta ler do CSV. Se o arquivo não existir, gera aleatório (Modo Sem Arquivo).
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            if not df.empty:
                # Pega uma linha aleatória do CSV
                amostra = df.sample(1).iloc[0]
                dados['maquina_temp'] = float(amostra.get('temperatura', 0.0))
                dados['maquina_vibracao'] = float(amostra.get('vibracao', 0.0))
                dados['maquina_distancia'] = float(amostra.get('distancia', 0.0))
                dados['status_temp'] = amostra.get('alarme_temperatura', 'Desconhecido')
                dados['status_vibra'] = amostra.get('alarme_vibracao', 'Desconhecido')
                dados['fonte_maquina'] = "Arquivo CSV (Dados Históricos)"
            else:
                dados = _gerar_simulacao_maquina()
        except Exception:
            dados = _gerar_simulacao_maquina()
    else:
        # Se você não anexou o CSV, ele entra aqui automaticamente
        dados = _gerar_simulacao_maquina()

    # --- 2. DADOS DO SOLO (Simulação Agrícola) ---
    # Esses dados sempre são simulados pois não existiam no seu CSV original
    dados['solo_umidade'] = round(random.uniform(20.0, 90.0), 1)
    dados['solo_ph'] = round(random.uniform(5.0, 8.0), 1)
    
    # Lógica simples de nutrientes baseada no pH
    if 6.0 <= dados['solo_ph'] <= 7.0:
        dados['solo_nutrientes'] = 'Ideal'
    else:
        dados['solo_nutrientes'] = 'Baixo (Requer Correção)'
    
    return dados

def _gerar_simulacao_maquina():
    """
    Gera dados falsos da máquina se o CSV não estiver presente.
    Isso garante que seu código funcione "sem precisar anexar o .csv".
    """
    return {
        'maquina_temp': round(random.uniform(30.0, 80.0), 1),
        'maquina_vibracao': round(random.uniform(0.1, 1.5), 2),
        'maquina_distancia': round(random.uniform(80.0, 150.0), 1),
        'status_temp': 'Simulado',
        'status_vibra': 'Simulado',
        'fonte_maquina': 'Simulação Aleatória (Sem CSV)'
    }

def avaliar_irrigacao(dados_sensores):
    """
    Cérebro da Automação: Decide se liga a bomba.
    """
    umidade = dados_sensores.get('solo_umidade', 50.0)
    vibracao = dados_sensores.get('maquina_vibracao', 0.0)
    temp_maquina = dados_sensores.get('maquina_temp', 0.0)
    
    status = {
        "acao": "AGUARDANDO...", 
        "mensagem": "Sistema operando normalmente.",
        "cor_mensagem": "green", 
        "alerta_critico": False 
    }

    # PRIORIDADE 1: Segurança da Máquina
    # Se a máquina estiver vibrando muito ou quente, NÃO liga a irrigação.
    if vibracao > 1.0 or temp_maquina > 55.0:
        status["acao"] = "PARADA DE EMERGÊNCIA 🛑"
        status["mensagem"] = f"ERRO CRÍTICO: Bomba com anomalia (Vibração: {vibracao:.2f} / Temp: {temp_maquina:.1f}°C)."
        status["cor_mensagem"] = "red"
        status["alerta_critico"] = True
        return status

    # PRIORIDADE 2: Necessidade da Planta
    if umidade < 40.0:
        status["acao"] = "LIGAR BOMBA 💧"
        status["mensagem"] = f"Solo seco ({umidade}%). Iniciando irrigação."
        status["cor_mensagem"] = "blue"
    elif umidade > 80.0:
        status["acao"] = "DESLIGAR BOMBA ⛔"
        status["mensagem"] = f"Solo encharcado ({umidade}%). Parando irrigação."
        status["cor_mensagem"] = "orange"
    else:
        status["acao"] = "MONITORANDO 👁️"
        status["mensagem"] = f"Umidade ideal ({umidade}%). Solo estável."
        status["cor_mensagem"] = "green"
        
    return status

# --- BLOCO DE TESTE (Isto permite rodar o arquivo direto no terminal) ---
if __name__ == "__main__":
    import time
    print("\n🌱 --- SIMULAÇÃO DE IOT FARMTECH --- 🌱")
    print("Lendo sensores virtuais e verificando arquivo CSV...")
    time.sleep(1) # Só para dar um charme de 'processando'
    
    # 1. Obter dados
    dados = get_dados_sensores()
    print(f"\n📡 DADOS COLETADOS:")
    for k, v in dados.items():
        print(f"   - {k}: {v}")
    
    # 2. Avaliar decisão
    analise = avaliar_irrigacao(dados)
    print(f"\n🧠 INTELIGÊNCIA ARTIFICIAL (EDGE):")
    print(f"   Ação: {analise['acao']}")
    print(f"   Motivo: {analise['mensagem']}")
    print("----------------------------------------------\n")