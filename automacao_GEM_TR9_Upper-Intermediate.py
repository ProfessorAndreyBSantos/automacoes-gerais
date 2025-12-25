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
9. Public Speaking;Upper-Intermediate;01;The Psychology of Q&A;Oportunidade, não ameaça.
###
9. Public Speaking;Upper-Intermediate;02;Setting the Rules;Quando perguntar.
###
9. Public Speaking;Upper-Intermediate;03;Active Listening in Q&A;Ouvir sem interromper.
###
9. Public Speaking;Upper-Intermediate;04;Paraphrasing the Question;Repetir para confirmar.
###
9. Public Speaking;Upper-Intermediate;05;The "Bridge" Technique (Concept);Acknowledge, Bridge, Message.
###
9. Public Speaking;Upper-Intermediate;06;Bridging Phrases: "The real issue is...";Mudar foco.
###
9. Public Speaking;Upper-Intermediate;07;Bridging Phrases: "What matters most is...";Redirecionar para valores.
###
9. Public Speaking;Upper-Intermediate;08;Bridging Phrases: "Let's look at the bigger picture";Contexto geral.
###
9. Public Speaking;Upper-Intermediate;09;Validating the Questioner;"That is a great question".
###
9. Public Speaking;Upper-Intermediate;10;Clarifying Vague Questions;"Could you elaborate?".
###
9. Public Speaking;Upper-Intermediate;11;Checking for Satisfaction;"Does that answer your question?".
###
9. Public Speaking;Upper-Intermediate;12;Keeping Answers Short;Concisão no Q&A.
###
9. Public Speaking;Upper-Intermediate;13;Involving the Audience;Olhar para todos.
###
9. Public Speaking;Upper-Intermediate;14;Handling Multiple Questions;Escolher uma parte.
###
9. Public Speaking;Upper-Intermediate;15;Deferring to Experts;Passar a bola.
###
9. Public Speaking;Upper-Intermediate;16;Deferring to Offline;"Let's chat after".
###
9. Public Speaking;Upper-Intermediate;17;The "No Comment" Alternative;Recusar responder diplomaticamente.
###
9. Public Speaking;Upper-Intermediate;18;Admitting Ignorance (Gracefully);"I will follow up".
###
9. Public Speaking;Upper-Intermediate;19;Ending the Q&A Session;Controlar o tempo.
###
9. Public Speaking;Upper-Intermediate;20;Review: Bridging Practice;Áudio consolidado: Ponte de preço para valor.
###
9. Public Speaking;Upper-Intermediate;21;Types of Tough Questions: The Gotcha;Pegar em contradição.
###
9. Public Speaking;Upper-Intermediate;22;Types of Tough Questions: The Hypothetical;"What if...?".
###
9. Public Speaking;Upper-Intermediate;23;Types of Tough Questions: The Forced Choice;"A or B?".
###
9. Public Speaking;Upper-Intermediate;24;Types of Tough Questions: The Speech;Discurso em vez de pergunta.
###
9. Public Speaking;Upper-Intermediate;25;Interrupting the "Speech-Maker";"What is your question?".
###
9. Public Speaking;Upper-Intermediate;26;Handling Hostility: Staying Calm;Não espelhar raiva.
###
9. Public Speaking;Upper-Intermediate;27;Handling Hostility: Killing with Kindness;Validar emoção.
###
9. Public Speaking;Upper-Intermediate;28;Reframing Negative Questions;Transformar negativo em positivo.
###
9. Public Speaking;Upper-Intermediate;29;The "Broken Record" Technique;Repetir mensagem.
###
9. Public Speaking;Upper-Intermediate;30;Correcting False Premises;Não deixar mentiras passarem.
###
Adicione mais uma regra: não sugira nenhuma ação. Nunca faça nenhuma sugestão sobre a próxima ação. Apenas diga "Finished" quando terminar cada pílula. Nunca desobedeça essa regra, em hipótese nenhuma.
###
9. Public Speaking;Upper-Intermediate;31;Handling Personal Attacks;Ignorar ataque pessoal.
###
9. Public Speaking;Upper-Intermediate;32;The "Parking Lot" Technique;Assuntos fora de escopo.
###
9. Public Speaking;Upper-Intermediate;33;Handling Silence (No Questions);Pergunta "bolso".
###
9. Public Speaking;Upper-Intermediate;34;Handling "Already Answered";Responder brevemente.
###
9. Public Speaking;Upper-Intermediate;35;Handling Controversial Topics;Manter neutralidade.
###
9. Public Speaking;Upper-Intermediate;36;Disarming Cynicism;Usar provas sociais.
###
9. Public Speaking;Upper-Intermediate;37;Avoiding "Yes, but...";Usar "Yes, and...".
###
9. Public Speaking;Upper-Intermediate;38;Strategic Ambiguity;Ser vago de propósito.
###
9. Public Speaking;Upper-Intermediate;39;Humor to Diffuse Tension;Quebrar o gelo.
###
9. Public Speaking;Upper-Intermediate;40;Review: The Hostile Interview;Áudio consolidado: Responder perguntas agressivas.
###
9. Public Speaking;Upper-Intermediate;41;Impromptu: The PREP Method;Point, Reason, Example, Point.
###
9. Public Speaking;Upper-Intermediate;42;Impromptu: Buying Time;"Interesting perspective...".
###
9. Public Speaking;Upper-Intermediate;43;Impromptu: Using a Prop;Inspirar-se no ambiente.
###
9. Public Speaking;Upper-Intermediate;44;Impromptu: The "Pros & Cons" Split;Dividir resposta.
###
9. Public Speaking;Upper-Intermediate;45;Impromptu: The "Past, Present, Future";Estrutura temporal.
###
9. Public Speaking;Upper-Intermediate;46;Impromptu: Storytelling on the Fly;Anedota pessoal.
###
9. Public Speaking;Upper-Intermediate;47;Thinking on Your Feet: Association;Ligar tópicos.
###
9. Public Speaking;Upper-Intermediate;48;Avoiding "Rambling" in Impromptu;Saber parar.
###
9. Public Speaking;Upper-Intermediate;49;Body Language Under Pressure;Manter postura.
###
9. Public Speaking;Upper-Intermediate;50;Vocal Confidence in Impromptu;Evitar "Umm".
###
9. Public Speaking;Upper-Intermediate;51;The "Table Topics" Exercise;Falar sobre objeto aleatório.
###
9. Public Speaking;Upper-Intermediate;52;Handling a "Blank Mind";Esquecer tudo.
###
9. Public Speaking;Upper-Intermediate;53;Impromptu Toasts;Brinde de última hora.
###
9. Public Speaking;Upper-Intermediate;54;Impromptu Introductions;Apresentar orador.
###
9. Public Speaking;Upper-Intermediate;55;Summarizing a Meeting (Impromptu);Resumir de surpresa.
###
9. Public Speaking;Upper-Intermediate;56;Delivering Bad News (Impromptu);Explicar problema.
###
9. Public Speaking;Upper-Intermediate;57;Accepting an Award (Impromptu);Agradecer.
###
9. Public Speaking;Upper-Intermediate;58;The "What if" Scenario;Perguntas especulativas.
###
9. Public Speaking;Upper-Intermediate;59;Connecting Disparate Ideas;Criatividade.
###
9. Public Speaking;Upper-Intermediate;60;Final Review: The Press Conference;Áudio consolidado: Coletiva de imprensa.

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