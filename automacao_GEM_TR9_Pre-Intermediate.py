import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# ==============================================================================
# 1. CONFIGURAÇÕES & DADOS
# ==============================================================================

# IMPORTANTE: No Chromebook (Linux), não usamos "C:\". 
# Usamos o caminho relativo ou absoluto do Linux.
# O perfil será criado na pasta onde o script estiver rodando.
CAMINHO_PERFIL_ROBO = os.path.join(os.getcwd(), "chromebook_profile")

# URL do Gemini
URL_ALVO = "https://gemini.google.com/app"

# --- SEUS TEXTOS (INSIRA AQUI O CONTEÚDO SEPARADO POR ###) ---
lista_conteudos = """
9. Public Speaking;Pre-Intermediate;01;The Importance of "Flow";O discurso precisa deslizar.
###
9. Public Speaking;Pre-Intermediate;02;Sequencing: First, Second, Third;Enumeração básica.
###
9. Public Speaking;Pre-Intermediate;03;Sequencing: Next & Then;Mover a narrativa.
###
9. Public Speaking;Pre-Intermediate;04;Sequencing: Finally / Lastly;Sinalizar o último ponto.
###
9. Public Speaking;Pre-Intermediate;05;The "Chrono" Structure;Ordem de tempo.
###
9. Public Speaking;Pre-Intermediate;06;The "Process" Structure;Passo a passo.
###
9. Public Speaking;Pre-Intermediate;07;Adding Info: "In addition";Adicionar ponto extra.
###
9. Public Speaking;Pre-Intermediate;08;Adding Info: "Also" vs "Too";Posição na frase.
###
9. Public Speaking;Pre-Intermediate;09;Adding Info: "Plus...";Adição casual.
###
9. Public Speaking;Pre-Intermediate;10;Adding Info: "Furthermore";Adição sofisticada.
###
9. Public Speaking;Pre-Intermediate;11;Giving Examples: "For instance";Introduzir caso prático.
###
9. Public Speaking;Pre-Intermediate;12;Giving Examples: "Such as";Listar exemplos rápidos.
###
9. Public Speaking;Pre-Intermediate;13;Giving Examples: A Personal Story;"Let me give you a personal example".
###
9. Public Speaking;Pre-Intermediate;14;Clarifying: "In other words";Reformular ideia.
###
9. Public Speaking;Pre-Intermediate;15;Clarifying: "To put it simply";Simplificar conceito.
###
9. Public Speaking;Pre-Intermediate;16;Clarifying: "What I mean is...";Ajustar o que disse.
###
9. Public Speaking;Pre-Intermediate;17;Emphasizing: "Especially / Particularly";Destacar item.
###
9. Public Speaking;Pre-Intermediate;18;Emphasizing: "Above all";Destacar ponto crucial.
###
9. Public Speaking;Pre-Intermediate;19;Emphasizing: "Crucially";Chamar atenção.
###
9. Public Speaking;Pre-Intermediate;20;Review: The How-To Speech;Áudio consolidado: Ensinar processo.
###
9. Public Speaking;Pre-Intermediate;21;Contrast: "However";A virada de chave.
###
9. Public Speaking;Pre-Intermediate;22;Contrast: "On the other hand";O lado oposto.
###
9. Public Speaking;Pre-Intermediate;23;Contrast: "Although / Even though";Concessão.
###
9. Public Speaking;Pre-Intermediate;24;Contrast: "But" vs "Yet";Oposição simples vs surpresa.
###
9. Public Speaking;Pre-Intermediate;25;Contrast: "Despite";Superação de obstáculo.
###
9. Public Speaking;Pre-Intermediate;26;Cause: "Because of" / "Due to";Explicar origem.
###
9. Public Speaking;Pre-Intermediate;27;Effect: "Therefore";Conclusão lógica.
###
9. Public Speaking;Pre-Intermediate;28;Effect: "So" (The Power Connector);Concluir ou mudar tópico.
###
9. Public Speaking;Pre-Intermediate;29;Effect: "As a result";Ação e reação.
###
9. Public Speaking;Pre-Intermediate;30;Effect: "Consequently";Impacto direto.
###
9. Public Speaking;Pre-Intermediate;31;Comparison: "Similarly";Mostrar igualdade.
###
9. Public Speaking;Pre-Intermediate;32;Comparison: "Just like";Analogias simples.
###
9. Public Speaking;Pre-Intermediate;33;Purpose: "In order to";Objetivo da ação.
###
9. Public Speaking;Pre-Intermediate;34;Purpose: "So that";"We invested so that we could grow".
###
9. Public Speaking;Pre-Intermediate;35;Highlighting Truth: "Actually";Corrigir percepção.
###
9. Public Speaking;Pre-Intermediate;36;Highlighting Truth: "In fact";Reforçar com verdade.
###
9. Public Speaking;Pre-Intermediate;37;Generalizing: "In general";Falar do todo.
###
9. Public Speaking;Pre-Intermediate;38;Generalizing: "On the whole";Resumir experiência.
###
9. Public Speaking;Pre-Intermediate;39;Summarizing Points;"To recap...".
###
9. Public Speaking;Pre-Intermediate;40;Review: The Argument;Áudio consolidado: Defender ponto de vista.
###
9. Public Speaking;Pre-Intermediate;41;The "Rule of Recency";Lembrar do último ponto.
###
9. Public Speaking;Pre-Intermediate;42;Referring Back (Looping);"Remember when I said...".
###
9. Public Speaking;Pre-Intermediate;43;Referring Forward (Teasing);"I will get to that...".
###
9. Public Speaking;Pre-Intermediate;44;Signposting Questions;"Why is this important?".
###
9. Public Speaking;Pre-Intermediate;45;The Bridge Technique;Conectar assuntos distantes.
###
9. Public Speaking;Pre-Intermediate;46;Avoiding: "And... and... and...";Run-on sentences.
###
9. Public Speaking;Pre-Intermediate;47;Avoiding: Rambling;Voltar ao foco.
###
9. Public Speaking;Pre-Intermediate;48;Checking Audience Focus;"Are you still with me?".
###
9. Public Speaking;Pre-Intermediate;49;Transitioning to Visuals;"If you look at this slide...".
###
9. Public Speaking;Pre-Intermediate;50;Transitioning to Q&A;"That covers the main points".
###
9. Public Speaking;Pre-Intermediate;51;Repeating for Clarity;"Let me repeat that".
###
9. Public Speaking;Pre-Intermediate;52;Rephrasing for Impact;Dizer de duas formas.
###
9. Public Speaking;Pre-Intermediate;53;The "Problem-Solution" Bridge;Problema -> Solução.
###
9. Public Speaking;Pre-Intermediate;54;The "Past-Present" Bridge;Antes -> Agora.
###
9. Public Speaking;Pre-Intermediate;55;Defining Scope;"I won't talk about X".
###
9. Public Speaking;Pre-Intermediate;56;Acknowledging the Obvious;"Obviously...".
###
9. Public Speaking;Pre-Intermediate;57;Expressing Certainty;"Clearly...".
###
9. Public Speaking;Pre-Intermediate;58;Expressing Uncertainty;"It seems that...".
###
9. Public Speaking;Pre-Intermediate;59;Coherence in Storytelling;Começo, meio e fim.
###
9. Public Speaking;Pre-Intermediate;60;Final Review: The Coherent Pitch;Áudio consolidado: Pitch de 2 minutos.

"""

# Separa os blocos e remove vazios
projetos = [bloco.strip() for bloco in lista_conteudos.split('###') if bloco.strip() != '']

# ==============================================================================
# 2. INICIALIZAÇÃO DO CHROMIUM
# ==============================================================================
def get_driver():
    print("⚙️ Configurando Chromium no Chromebook...")
    
    options = Options()
    # Mantém o navegador aberto após o script (opcional, mas bom para debug)
    options.add_experimental_option("detach", True)
    
    # Configura o perfil de usuário para salvar login (se necessário futuramente)
    options.add_argument(f"user-data-dir={CAMINHO_PERFIL_ROBO}")
    
    # Ajustes para rodar liso no ambiente Linux/Container
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # --- PONTO CRÍTICO PARA CHROMEBOOK ---
    # O Selenium precisa saber onde está o executável do Chromium.
    # Geralmente em: /usr/bin/chromium ou /usr/bin/google-chrome
    # Se der erro, verifique rodando 'which chromium' no terminal.
    options.binary_location = "/usr/bin/chromium" 

    try:
        # Tenta usar o gerenciador automático
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"⚠️ Erro no Manager, tentando driver padrão do sistema Linux: {e}")
        # Fallback para o driver instalado via apt (sudo apt install chromium-driver)
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

    return driver

# ==============================================================================
# 3. AUTOMAÇÃO
# ==============================================================================
def run_automation():
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    # 1. Abrir o site (Chromium já abriu no get_driver)
    print(f"🌍 Navegando para {URL_ALVO}...")
    driver.get(URL_ALVO)

    # 2 e 3. Esperar interação do usuário
    print("\n" + "="*50)
    print("🛑 PAUSA DE 1 MINUTO")
    print("👉 Por favor, faça login (se necessário) e selecione a conversa alvo.")
    print("⏳ Aguardando 60 segundos...")
    print("="*50 + "\n")
    
    time.sleep(60) # Pausa solicitada de 1 minuto

    print("🚀 Iniciando envio dos prompts...")

    for i, texto in enumerate(projetos):
        print(f"\n🔹 Enviando Prompt {i+1} de {len(projetos)}...")
        
        try:
            # 4. Encontrar a caixa de texto
            # O seletor abaixo busca pela DIV editável (role="textbox") que é mais estável que classes dinâmicas
            caixa_texto = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='textbox']")))
            
            # Limpa (por segurança) e Cola o texto
            # Nota: send_keys direto costuma funcionar melhor que CTRL+V em containers Linux, 
            # mas se o texto for muito grande, o script colará caractere por caractere.
            caixa_texto.send_keys(texto)
            
            # 5. Esperar 2 segundos e Apertar Enter
            time.sleep(2)
            caixa_texto.send_keys(Keys.ENTER)
            print("   ✅ Texto enviado (Enter pressionado).")

            # Nota sobre o botão: Você forneceu o seletor do botão, mas pediu para apertar ENTER.
            # O Enter é mais seguro. Se preferir clicar, descomente as linhas abaixo:
            # botao_enviar = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Envi']")
            # botao_enviar.click()

            # 6. Esperar 65 segundos para a resposta
            if i < len(projetos) - 1: # Só espera se não for o último
                print("   ⏳ Aguardando 65 segundos para a resposta do Gemini...")
                time.sleep(65)
            else:
                print("   🏁 Último prompt enviado.")

        except Exception as e:
            print(f"❌ Erro ao processar o item {i+1}: {e}")
            continue

    print("\n✅ Automação Finalizada!")

if __name__ == "__main__":
    run_automation()