import math

# Função pura: Recebe dados, retorna resultado. Sem input() nem print()
def calcular_area_plantio(forma, dimensao1, dimensao2=0):
    """
    Calcula a área baseada na forma.
    forma: str ('retângulo', 'quadrado', 'círculo')
    dimensao1: largura ou lado ou raio
    dimensao2: comprimento (apenas para retângulo)
    """
    forma = forma.lower().strip()
    
    if forma in ["retângulo", "retangulo"]:
        # dimensao1 = largura, dimensao2 = comprimento
        return dimensao1 * dimensao2

    elif forma == "quadrado":
        # dimensao1 = lado
        return dimensao1 ** 2

    elif forma in ["círculo", "circulo"]:
        # dimensao1 = raio
        return math.pi * (dimensao1 ** 2)

    else:
        return 0.0

def calcular_qtd_insumos(area_cultivo, qtd_por_m2, num_linhas):
    """
    area_cultivo: float
    qtd_por_m2: float
    num_linhas: int
    """
    if area_cultivo <= 0 or qtd_por_m2 <= 0:
        return 0.0
        
    total_quantity = area_cultivo * qtd_por_m2 # Removi 'rows' da multiplicação pois geralmente é por m², mas mantive sua lógica original se quiser usar
    # Nota: No seu código original vc multiplicava por rows. 
    # Se a qtd é "por m²", multiplicar por linhas pode duplicar o valor dependendo da lógica agronômica.
    # Vou manter sua lógica original abaixo:
    total_quantity = area_cultivo * qtd_por_m2 * num_linhas
    
    return total_quantity