import json
import os
import pandas as pd

# Tenta importar o Oracle, mas se falhar (porque não instalou), segue a vida.
try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    # print("⚠️ Aviso: cx_Oracle não instalado. Usando modo OFFLINE.")

# --- CONFIGURAÇÕES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'dados_insumos.json')

def conectar_oracle():
    """Tenta conectar ao Oracle. Retorna a conexão ou None se falhar."""
    if not ORACLE_AVAILABLE:
        return None
        
    try:
        dsn = cx_Oracle.makedsn("ORACLE.FIAP.COM.BR", 1521, service_name="ORCL")
        conn = cx_Oracle.connect(user="RM562962", password="170180", dsn=dsn)
        return conn
    except Exception as e:
        print(f"⚠️ Erro conexão Oracle: {e}")
        return None

def desconectar_oracle(conn):
    if conn:
        try:
            conn.close()
        except:
            pass

# --- FUNÇÕES DE LEITURA ---
def obter_dados_insumos():
    conn = conectar_oracle()
    
    # 1. TENTATIVA ORACLE
    if conn:
        try:
            query = "SELECT nome, tipo, quantidade, TO_CHAR(validade, 'YYYY-MM-DD') as validade FROM insumos"
            df = pd.read_sql(query, conn)
            desconectar_oracle(conn)
            return df, "Conectado ao Oracle Database (Nuvem)"
        except Exception as e:
            desconectar_oracle(conn)
    
    # 2. TENTATIVA JSON (FALLBACK)
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            df = pd.DataFrame(dados)
            return df, "Modo Offline (Lendo de JSON Local)"
        except Exception as e:
            return pd.DataFrame(), f"Erro ao ler JSON: {e}"
    
    return pd.DataFrame(), "Modo Simulado (JSON não encontrado)"

# --- FUNÇÕES DE ESCRITA (ATUALIZADA) ---
def inserir_insumo(nome, tipo, quantidade, validade):
    # Tenta conectar no Oracle primeiro
    conn = conectar_oracle()
    
    # --- CENÁRIO 1: SALVAR NO ORACLE (Se estiver online) ---
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO insumos (nome, tipo, quantidade, validade) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))"
            cursor.execute(sql, (nome, tipo, quantidade, validade))
            conn.commit()
            return "Sucesso: Insumo inserido no Oracle!"
        except Exception as e:
            return f"Erro ao inserir no Oracle: {str(e)}"
        finally:
            desconectar_oracle(conn)

    # --- CENÁRIO 2: SALVAR NO JSON (Modo Offline - O que você precisa pro vídeo) ---
    try:
        # 1. Carrega dados existentes
        lista_dados = []
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                lista_dados = json.load(f)
        
        # 2. Cria o novo item
        novo_item = {
            "nome": nome.upper(),
            "tipo": tipo,
            "quantidade": int(quantidade),
            "validade": str(validade)
        }
        
        # 3. Adiciona e Salva
        lista_dados.append(novo_item)
        
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista_dados, f, indent=4, ensure_ascii=False)
            
        return "Sucesso: Item salvo localmente (Modo Offline)!"
        
    except Exception as e:
        return f"Erro ao salvar no JSON: {str(e)}"