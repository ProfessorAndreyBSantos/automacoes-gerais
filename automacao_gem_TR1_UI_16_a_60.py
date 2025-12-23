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
1. Travel & Culture;Upper-Intermediate;16;Personal Space;Proximidade física.
###
1. Travel & Culture;Upper-Intermediate;17;Eye Contact Rules;Respeito vs Desafio.
###
1. Travel & Culture;Upper-Intermediate;18;Gender Roles in Travel;Segurança e costumes.
###
1. Travel & Culture;Upper-Intermediate;19;LGBTQ+ Travel;Vocabulário específico e segurança.
###
1. Travel & Culture;Upper-Intermediate;20;Review: Cultural Guide;Áudio consolidado: Explicar etiqueta brasileira para um gringo.
###
1. Travel & Culture;Upper-Intermediate;21;Travel Media: Magazines;Linguagem de revista de viagem.
###
1. Travel & Culture;Upper-Intermediate;22;Travel Media: Documentaries;Narrativa de documentário.
###
1. Travel & Culture;Upper-Intermediate;23;Travel Influencers;Crítica e vocabulário.
###
1. Travel & Culture;Upper-Intermediate;24;Analyzing Reviews;Ler nas entrelinhas do TripAdvisor.
###
1. Travel & Culture;Upper-Intermediate;25;Overtourism Debate;Discutir impacto do turismo de massa.
###
1. Travel & Culture;Upper-Intermediate;26;Voluntourism;Ética do turismo voluntário.
###
1. Travel & Culture;Upper-Intermediate;27;Authenticity in Travel;O que é uma experiência "real"?
###
1. Travel & Culture;Upper-Intermediate;28;The "Tourist Trap";Identificar e discutir.
###
1. Travel & Culture;Upper-Intermediate;29;Ethical Wildlife Tourism;Zoológicos vs Santuários.
###
1. Travel & Culture;Upper-Intermediate;30;Environmental Impact;Voar vs Trem (Flight shame).
###
1. Travel & Culture;Upper-Intermediate;31;Inversion: "Never have I...";Ênfase dramática.
###
1. Travel & Culture;Upper-Intermediate;32;Inversion: "Little did I know...";Narrativa avançada.
###
1. Travel & Culture;Upper-Intermediate;33;Cleft Sentences: "What I loved...";Enfatizar o que gostou.
###
1. Travel & Culture;Upper-Intermediate;34;Participle Clauses;Encurtar frases descritivas.
###
1. Travel & Culture;Upper-Intermediate;35;Advanced Adjectives: Landscapes;Pristine, Rugged, Sprawling.
###
1. Travel & Culture;Upper-Intermediate;36;Advanced Adjectives: Cities;Bustling, Vibrant, Gritty.
###
1. Travel & Culture;Upper-Intermediate;37;Advanced Adjectives: Food;Exquisite, Delectable.
###
1. Travel & Culture;Upper-Intermediate;38;Metaphors in Travel;"The city never sleeps".
###
1. Travel & Culture;Upper-Intermediate;39;Similes in Travel;"Like a scene from a movie".
###
1. Travel & Culture;Upper-Intermediate;40;Review: The Documentary Voiceover;Áudio consolidado: Narrar a intro de um doc de viagem.
###
1. Travel & Culture;Upper-Intermediate;41;Retórica: Persuading a Friend;Convencer a ir a um lugar exótico.
###
1. Travel & Culture;Upper-Intermediate;42;Debating: Resort vs Adventure;Argumentação.
###
1. Travel & Culture;Upper-Intermediate;43;Complaining Effectively (Written);E-mail formal de reclamação.
###
1. Travel & Culture;Upper-Intermediate;44;Complaining Effectively (Oral);Falar com o gerente.
###
1. Travel & Culture;Upper-Intermediate;45;Demanding Compensation;Pedir milhas ou reembolso.
###
1. Travel & Culture;Upper-Intermediate;46;Handling a Medical Crisis;Vocabulário avançado de hospital.
###
1. Travel & Culture;Upper-Intermediate;47;Legal Issues abroad;Polícia e direitos.
###
1. Travel & Culture;Upper-Intermediate;48;Embassy Assistance;O que a embaixada pode fazer.
###
1. Travel & Culture;Upper-Intermediate;49;Lost & Found (Advanced);Descrever itens detalhadamente.
###
1. Travel & Culture;Upper-Intermediate;50;Natural Disasters;Vocabulário de terremoto/furacão.
###
1. Travel & Culture;Upper-Intermediate;51;Travel Tech: Apps;Discutir utilidade de apps.
###
1. Travel & Culture;Upper-Intermediate;52;Remote Work Laws;Vistos para nômades.
###
1. Travel & Culture;Upper-Intermediate;53;Globalization impact;Lojas iguais em todo lugar.
###
1. Travel & Culture;Upper-Intermediate;54;Language Barriers;Como superar sem falar a língua.
###
1. Travel & Culture;Upper-Intermediate;55;Humor in Travel;Entender piadas locais.
###
1. Travel & Culture;Upper-Intermediate;56;Irony and Sarcasm;Detectar em serviço ruim.
###
1. Travel & Culture;Upper-Intermediate;57;Slang: British vs American;Diferenças em viagem (Lorry/Truck).
###
1. Travel & Culture;Upper-Intermediate;58;Australian Travel Slang;Arvo, Brekkie.
###
1. Travel & Culture;Upper-Intermediate;59;Global English Accents;Entender não-nativos.
###
1. Travel & Culture;Upper-Intermediate;60;Final Review: The Debate;Áudio consolidado: Debater "Turismo Espacial" (Prós/Contras).
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