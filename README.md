# 🌱 FarmTech Solutions - Sistema Integrado de Gestão Agrícola

## 📋 Descrição do Projeto (Fase 7)

Este projeto representa a consolidação final (Fase 7) do ecossistema FarmTech. Trata-se de uma plataforma Full Stack em Python que integra Backend, Frontend (Streamlit), Ciência de Dados, IoT e Visão Computacional em um único Dashboard interativo.

O objetivo é fornecer ao gestor agrícola uma ferramenta centralizada para o planejamento de plantio, controle de estoque, monitoramento de sensores em tempo real e segurança patrimonial via inteligência artificial.

## 👨‍🌾 Integrantes do Grupo
- <a href="https://www.linkedin.com/in/nicolas--araujo/">Nicolas Antonio Silva Araujo</a> 
- <a href="https://www.linkedin.com/in/vitoria-bagatin-31ba88266/">Vitória Pereira Bagatin</a> 

## 🎬 Vídeo Demonstrativo

Confira a demonstração completa de todas as funcionalidades rodando em tempo real:

[CLIQUE AQUI PARA ASSISTIR AO VÍDEO NO YOUTUBE]
(Link vídeo não listado aqui)

## 🛠️ Arquitetura e Funcionalidades Integradas

O projeto foi estruturado de forma modular para garantir organização e escalabilidade. Abaixo, o detalhamento de cada fase integrada:

### 🌱 Fase 1: Planejamento Inteligente

- Calculadora agronômica que auxilia na definição de área de plantio e quantidade de insumos.

- Destaque: Implementação de presets inteligentes. Ao selecionar a cultura (Soja, Milho, etc.), o sistema ajusta automaticamente a recomendação de insumos (kg/m²) baseada em boas práticas agronômicas.

### 🗄️ Fase 2: Banco de Dados Híbrido (Persistência)

- Sistema CRUD (Create, Read, Update, Delete) para gestão de estoque de insumos.

- Destaque Técnico: Arquitetura Híbrida/Resiliente.

- Modo Online: Preparado para conexão com Oracle Database (Nuvem).

- Modo Offline (Fallback): Caso a conexão falhe, o sistema alterna automaticamente para um banco de dados local em JSON (dados_insumos.json), permitindo leitura e escrita mesmo sem internet.

### 📡 Fase 3: IoT e Monitoramento (Edge Computing)

- Dashboard de telemetria que simula a leitura de sensores de campo (Umidade do Solo, pH) e sensores de maquinário (Vibração, Temperatura).

- Lógica de Automação: O sistema decide sozinho se deve ligar a irrigação baseada na umidade do solo.

- Segurança Crítica: Implementamos uma regra de "Parada de Emergência". Se o motor da bomba superaquecer (>55°C) ou vibrar excessivamente, o sistema bloqueia a irrigação para proteger o equipamento.

### ☁️ Fase 5: Cloud Computing (AWS)

- Integração com serviços de nuvem para mensageria crítica.

- Funcionalidade: Quando a Fase 3 detecta um erro crítico (ex: falha na bomba), o sistema aciona o módulo AWS para disparar alertas via SNS (Simple Notification Service).

- Evidência: O log do disparo e o status da conexão AWS são exibidos no próprio Dashboard.

![AWS](https://github.com/Nico-Araujo/Farmtech-Final/blob/7fcc287ab8c035874f944d673257c5375348615d/assets/farmtech_dashboard_aws.jpeg)

## 👁️ Fase 6: Visão Computacional (Segurança)

- Sistema de monitoramento visual utilizando Inteligência Artificial (YOLOv8).

- Objetivo: Segurança do trabalho e patrimonial.

- Funcionalidade: O modelo analisa imagens da plantação e detecta automaticamente a presença de Agricultores (Pessoas) e Maquinário (Tratores), permitindo o controle de acesso e segurança da área.

📂 Estrutura de Arquivos

A organização do projeto segue as melhores práticas de desenvolvimento, separando a lógica (Backend) da interface (Frontend):



```text
Farmtech_Final/
│
├── app.py                       # Arquivo Principal (Frontend Streamlit)
├── requirements.txt             # Lista de dependências
├── dados_sensores_simulados.csv # Base de dados histórica dos sensores
│
├── fases/                       # Módulos de Lógica (Backend)
│   ├── __init__.py              # (Opcional, mas bom ter)
│   ├── fase1_calc.py            # Lógica matemática e presets
│   ├── fase2_db.py              # Conexão Oracle e JSON
│   ├── fase3_iot.py             # Simulação de Sensores e Edge Computing
│   ├── fase5_cloud.py           # Integração AWS
│   ├── fase6_vision.py          # Processamento de Imagem (YOLO)
│   └── dados_insumos.json       # Banco de dados local (JSON)
│
└── assets/                      # Arquivos estáticos
    ├── best.pt                  # Modelo de I.A. Treinado
    └── teste.jpeg               # Imagem de exemplo para testes
````

## 🚀 Como Rodar o Projeto Localmente

- Pré-requisitos: Python 3.8+ instalado.

- Clone o repositório:

git clone [repositório](https://github.com/Nico-Araujo/Farmtech-Final)
cd Farmtech_Final


- Instale as dependências:

pip install -r requirements.txt


- Execute a aplicação:

streamlit run app.py


- Caso o comando acima não funcione no Windows, tente: python -m streamlit run app.py

- Acesse: O navegador abrirá automaticamente no endereço local (geralmente http://localhost:8501).

## 📊 Prints da Aplicação

Dashboard Principal

![Dashboard Home](https://github.com/Nico-Araujo/Farmtech-Final/blob/ca2cd13eb085407ca5d3e528a4d70df1a5578934/assets/farmtech_dashboard.jpeg)

Monitoramento de Segurança (I.A.)

![Visão Computacional](https://github.com/Nico-Araujo/Farmtech-Final/blob/0c6e8e401c65b1f467d7f595ce75fcadf432a337/assets/farmtech_vs_pessoas.jpeg)
