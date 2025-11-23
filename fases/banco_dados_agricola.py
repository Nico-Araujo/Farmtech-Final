import sqlite3
import datetime
import random
import csv
import os
from typing import List, Dict, Any, Tuple, Optional

class BancoDadosAgricola:
    def __init__(self, nome_bd: str = "dados_agricolas.db"):
        """Inicializa a conexão com o banco de dados."""
        self.nome_bd = nome_bd
        self.conn = sqlite3.connect(nome_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self) -> None:
        """
        Cria a tabela de sensores se não existir.
        ATUALIZAÇÃO FASE 4:
        - fosforo e potassio agora representam presença (0/1).
        - Adicionadas colunas para previsões do modelo de Machine Learning.
        """
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras_sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            umidade REAL,
            ph REAL,
            fosforo INTEGER,
            potassio INTEGER,
            status_bomba INTEGER,
            previsao_irrigacao INTEGER,
            confianca_previsao REAL,
            observacoes TEXT
        )
        ''')
        self.conn.commit()
        print("Tabela 'leituras_sensores' verificada/criada com sucesso!")

    def inserir_leitura(self, umidade: float, ph: float, fosforo: int,
                      potassio: int, status_bomba: int,
                      previsao_irrigacao: Optional[int] = None,
                      confianca_previsao: Optional[float] = None,
                      observacoes: str = "") -> int:
        """
        Insere uma nova leitura no banco de dados, incluindo previsões.
        """
        data_hora = datetime.datetime.now().isoformat()

        self.cursor.execute('''
        INSERT INTO leituras_sensores
        (data_hora, umidade, ph, fosforo, potassio, status_bomba,
         previsao_irrigacao, confianca_previsao, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data_hora, umidade, ph, fosforo, potassio, status_bomba,
              previsao_irrigacao, confianca_previsao, observacoes))

        self.conn.commit()
        return self.cursor.lastrowid

    def importar_do_serial(self, dados_serial: List[str]) -> List[int]:
        """
        Importa dados do monitor serial.
        ATUALIZAÇÃO FASE 4: Processa 'SIM'/'NAO' para fósforo e potássio.
        """
        ids_inseridos = []

        for linha in dados_serial:
            # Novo formato esperado: "umidade,ph,fosforo,potassio,status_bomba"
            # Exemplo: "40.0,3.40,SIM,NAO,0"
            try:
                partes = linha.strip().split(',')
                if len(partes) >= 5:
                    umidade = float(partes[0])
                    ph = float(partes[1])
                    
                    # Converte "SIM"/"NAO" para 1/0
                    fosforo_str = partes[2].strip().upper()
                    potassio_str = partes[3].strip().upper()
                    fosforo = 1 if fosforo_str == 'SIM' else 0
                    potassio = 1 if potassio_str == 'SIM' else 0

                    status_bomba = int(partes[4])

                    observacoes = ""
                    if len(partes) > 5:
                        observacoes = partes[5]

                    # Por enquanto, não há previsão de ML ao importar do serial
                    id_leitura = self.inserir_leitura(
                        umidade, ph, fosforo, potassio, status_bomba,
                        observacoes=observacoes
                    )
                    ids_inseridos.append(id_leitura)
            except (ValueError, IndexError) as e:
                print(f"Erro ao processar linha do serial: '{linha}'. Erro: {e}")

        return ids_inseridos
    
    # --- Funções que não precisam de alteração significativa ---
    
    def obter_todas_leituras(self) -> List[Dict[str, Any]]:
        """Retorna todas as leituras do banco de dados."""
        self.cursor.execute('SELECT * FROM leituras_sensores ORDER BY data_hora DESC')
        linhas = self.cursor.fetchall()
        colunas = [description[0] for description in self.cursor.description]
        return [dict(zip(colunas, linha)) for linha in linhas]

    def obter_leitura_por_id(self, id_leitura: int) -> Optional[Dict[str, Any]]:
        """Retorna uma leitura específica pelo ID."""
        self.cursor.execute('SELECT * FROM leituras_sensores WHERE id = ?', (id_leitura,))
        linha = self.cursor.fetchone()
        if linha:
            colunas = [description[0] for description in self.cursor.description]
            return dict(zip(colunas, linha))
        return None

    def atualizar_leitura(self, id_leitura: int, **kwargs) -> bool:
        """Atualiza uma leitura existente. Já é compatível com as novas colunas."""
        if not kwargs:
            return False
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        valores = list(kwargs.values())
        valores.append(id_leitura)
        self.cursor.execute(
            f'UPDATE leituras_sensores SET {set_clause} WHERE id = ?',
            valores
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def deletar_leitura(self, id_leitura: int) -> bool:
        """Deleta uma leitura pelo ID."""
        self.cursor.execute('DELETE FROM leituras_sensores WHERE id = ?', (id_leitura,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def exportar_para_csv(self, nome_arquivo: str = "dados_sensores.csv") -> str:
        """Exporta todos os dados para um arquivo CSV."""
        dados = self.obter_todas_leituras()
        if not dados:
            return "Sem dados para exportar"
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            nomes_campos = dados[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=nomes_campos)
            writer.writeheader()
            writer.writerows(dados)
        return os.path.abspath(nome_arquivo)
    
    def fechar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()

# --- Demonstração de Uso Atualizada ---

def gerar_dados_exemplo_fase4(num_amostras: int = 10) -> List[str]:
    """
    Gera dados simulados no formato da FASE 4 (com 'SIM'/'NAO').
    """
    dados = []
    for _ in range(num_amostras):
        umidade = round(random.uniform(20.0, 90.0), 1)
        ph = round(random.uniform(4.0, 8.5), 1)
        fosforo = random.choice(['SIM', 'NAO'])
        potassio = random.choice(['SIM', 'NAO'])
        status_bomba = 1 if umidade < 40.0 else 0
        linha = f"{umidade},{ph},{fosforo},{potassio},{status_bomba}"
        dados.append(linha)
    return dados

if __name__ == "__main__":
    # Apagar o banco antigo para testar a criação da nova tabela do zero
    if os.path.exists("dados_agricolas.db"):
        os.remove("dados_agricolas.db")
        print("Banco de dados antigo removido para novo teste.")

    with BancoDadosAgricola() as bd:
        print("\n=== Demonstração do Banco de Dados Agrícola - FASE 4 ===\n")

        # 1. Gerar e importar dados no novo formato
        print("1. Gerando e importando dados do serial (formato FASE 4)...")
        dados_serial = gerar_dados_exemplo_fase4(15)
        print(f"   Dados gerados: {dados_serial[:3]}...")
        ids_inseridos = bd.importar_do_serial(dados_serial)
        print(f"   {len(ids_inseridos)} registros inseridos com sucesso.")

        # 2. Inserir uma leitura com previsão de ML (simulado)
        print("\n2. Inserindo uma leitura com previsão de ML...")
        id_ml = bd.inserir_leitura(
            umidade=38.5, ph=6.8, fosforo=1, potassio=0, status_bomba=1,
            previsao_irrigacao=1,
            confianca_previsao=0.88,
            observacoes="Previsão do modelo Scikit-learn"
        )
        print(f"   Registro com previsão de ML inserido (ID: {id_ml}).")

        # 3. Consultar todos os registros para ver as novas colunas
        print("\n3. Consultando todos os registros:")
        todas_leituras = bd.obter_todas_leituras()
        for leitura in todas_leituras[:4]: # Mostra os primeiros 4
             print(f"   {leitura}")

        # 4. Atualizar um registro com uma previsão
        print(f"\n4. Atualizando o primeiro registro (ID: {ids_inseridos[0]}) com uma previsão...")
        sucesso = bd.atualizar_leitura(
            ids_inseridos[0],
            previsao_irrigacao=0,
            confianca_previsao=0.95,
            observacoes="Modelo previu não irrigar."
        )
        print(f"   Atualização {'bem-sucedida' if sucesso else 'falhou'}.")
        leitura_atualizada = bd.obter_leitura_por_id(ids_inseridos[0])
        print(f"   Registro atualizado: {leitura_atualizada}")

        # 5. Exportar para CSV
        print("\n5. Exportando dados para CSV:")
        caminho_csv = bd.exportar_para_csv()
        print(f"   Arquivo CSV gerado em: {caminho_csv}")

        print("\n=== Demonstração concluída ===")