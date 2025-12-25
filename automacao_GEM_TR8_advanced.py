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
8. Social English;Advanced;21;Nature vs Nurture;Genética ou criação?
###
8. Social English;Advanced;22;Emotional Intelligence (EQ);Importância de gerir emoções.
###
8. Social English;Advanced;23;Cognitive Biases: Confirmation Bias;Por que só aceitamos o que concordamos.
###
8. Social English;Advanced;24;Cognitive Biases: Sunk Cost Fallacy;Insistir no erro.
###
8. Social English;Advanced;25;The Imposter Syndrome;Sensação de ser uma fraude.
###
8. Social English;Advanced;26;The Psychology of Power;O poder corrompe?
###
8. Social English;Advanced;27;Groupthink & Herd Mentality;Decisões irracionais em grupo.
###
8. Social English;Advanced;28;Introverts vs Extroverts (Nuances);Ambiverts e energia.
###
8. Social English;Advanced;29;Toxic Positivity;Crítica à obrigação de ser feliz.
###
8. Social English;Advanced;30;Resilience & Grit;Superação de traumas.
###
8. Social English;Advanced;31;Intuition vs Logic;Confiar no instinto?
###
8. Social English;Advanced;32;Love Languages;Expressão de afeto.
###
8. Social English;Advanced;33;Modern Relationships;Monogamia, poliamor.
###
8. Social English;Advanced;34;The Impact of Social Media on Psyche;Comparação e autoestima.
###
8. Social English;Advanced;35;Generational Trauma;Impacto dos pais nos filhos.
###
8. Social English;Advanced;36;Forgiveness;Perdoar é para quem?
###
8. Social English;Advanced;37;Vulnerability (Brené Brown style);Fraqueza como força.
###
8. Social English;Advanced;38;Analyzing Dreams;Significado dos sonhos.
###
8. Social English;Advanced;39;The Concept of "Flow";Estado de concentração total.
###
8. Social English;Advanced;40;Review: Amateur Psychologist;Áudio consolidado: Analisar comportamento.
###
8. Social English;Advanced;41;Utopia vs Dystopia;Sociedade perfeita.
###
8. Social English;Advanced;42;Universal Basic Income (UBI);Dinheiro grátis e trabalho.
###
8. Social English;Advanced;43;The Future of Education;A escola está obsoleta?
###
8. Social English;Advanced;44;Globalization vs Localization;Identidade cultural.
###
8. Social English;Advanced;45;Gentrification;Revitalização de bairros.
###
8. Social English;Advanced;46;Over-tourism;Dilema ético do turismo.
###
8. Social English;Advanced;47;Climate Anxiety;Impacto psicológico do clima.
###
8. Social English;Advanced;48;Veganism & Ethics;Consumo de animais.
###
8. Social English;Advanced;49;Artificial Intelligence: Sentience;Direitos dos robôs.
###
8. Social English;Advanced;50;Space Exploration: Worth it?;Marte ou Terra?
###
8. Social English;Advanced;51;Meritocracy: Myth or Reality?;Esforço garante sucesso?
###
8. Social English;Advanced;52;Cancel Culture (Deep Dive);Justiça ou linchamento?
###
8. Social English;Advanced;53;Political Polarization;Ouvir o outro lado.
###
8. Social English;Advanced;54;Gender Roles & Stereotypes;Expectativas de gênero.
###
8. Social English;Advanced;55;The Aging Population;Desafios de viver 100 anos.
###
8. Social English;Advanced;56;Conspiracy Theories;Por que acreditamos?
###
8. Social English;Advanced;57;Privilege;Vantagem invisível.
###
8. Social English;Advanced;58;Cultural Appropriation;Apreciação ou roubo?
###
8. Social English;Advanced;59;Legacy;Que mundo queremos deixar?
###
8. Social English;Advanced;60;Final Review: The Dinner Speech;Áudio consolidado: Brinde sobre esperança.

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

            # 6. Esperar 60 segundos para a resposta
            if i < len(projetos) - 1: # Só espera se não for o último
                print("   ⏳ Aguardando 60 segundos para a resposta do Gemini...")
                time.sleep(60)
            else:
                print("   🏁 Último prompt enviado.")

        except Exception as e:
            print(f"❌ Erro ao processar o item {i+1}: {e}")
            continue

    print("\n✅ Automação Finalizada!")

if __name__ == "__main__":

    run_automation()
