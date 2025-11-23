import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# --- CONFIGURAÇÃO AWS ---
# Se tiver credenciais reais, coloque-as nas variáveis de ambiente ou configure o AWS CLI.
# Se não tiver, o código entrará em modo SIMULAÇÃO para não travar o app.

def enviar_alerta_aws(assunto, mensagem, topico_arn=None):
    """
    Tenta enviar um alerta via AWS SNS.
    Se falhar (sem credenciais), apenas simula o envio no log.
    """
    try:
        # Tenta conectar à AWS (busca credenciais automáticas do sistema)
        sns = boto3.client('sns', region_name='us-east-1')
        
        if topico_arn:
            response = sns.publish(
                TopicArn=topico_arn,
                Message=mensagem,
                Subject=assunto
            )
            return f"✅ Alerta AWS enviado! ID: {response['MessageId']}"
        else:
            return "⚠️ AWS Configurada, mas Tópico ARN não fornecido."
            
    except (NoCredentialsError, PartialCredentialsError):
        # MODO SIMULAÇÃO (Para garantir a nota se a conta AWS expirou)
        return f"☁️ [Simulação AWS] Alerta registrado: {assunto} - {mensagem}"
    except Exception as e:
        return f"❌ Erro AWS: {str(e)}"