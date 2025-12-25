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
9. Public Speaking;Intermediate;01;The Goal of Persuasion;Diferenciar informar de persuadir.
###
9. Public Speaking;Intermediate;02;The Three Pillars: Ethos (Credibility);Estabelecer autoridade.
###
9. Public Speaking;Intermediate;03;The Three Pillars: Logos (Logic);Usar lógica.
###
9. Public Speaking;Intermediate;04;The Three Pillars: Pathos (Emotion);Conectar emocionalmente.
###
9. Public Speaking;Intermediate;05;Structuring an Argument: Claims;Fazer uma afirmação.
###
9. Public Speaking;Intermediate;06;Structuring an Argument: Evidence;Apoiar com provas.
###
9. Public Speaking;Intermediate;07;Structuring an Argument: Warrant;Link lógico.
###
9. Public Speaking;Intermediate;08;The "Problem-Agitation-Solution";Estrutura de vendas.
###
9. Public Speaking;Intermediate;09;The "Before & After" Technique;Contrastar mundos.
###
9. Public Speaking;Intermediate;10;Using Analogies to Persuade;Simplificar o complexo.
###
9. Public Speaking;Intermediate;11;Anticipating Objections;Desarmar o crítico.
###
9. Public Speaking;Intermediate;12;Refuting Objections;"While that may be true...".
###
9. Public Speaking;Intermediate;13;Power Words (Verbs);Usar verbos fortes.
###
9. Public Speaking;Intermediate;14;Power Words (Adjectives);Usar adjetivos de impacto.
###
9. Public Speaking;Intermediate;15;Avoid: Weak Language;Cortar "I think", "Maybe".
###
9. Public Speaking;Intermediate;16;Call to Action (CTA): Direct;"Sign up today".
###
9. Public Speaking;Intermediate;17;Call to Action (CTA): Indirect;"Consider the possibilities".
###
9. Public Speaking;Intermediate;18;Creating Urgency;"The time is now".
###
9. Public Speaking;Intermediate;19;Scarcity Principle;"Only a few left".
###
9. Public Speaking;Intermediate;20;Review: The Persuasive Pitch;Áudio consolidado: Vender ideia usando pilares.
###
9. Public Speaking;Intermediate;21;Rhetorical Questions (Advanced);Perguntas para fazer pensar.
###
9. Public Speaking;Intermediate;22;Repetition: Anaphora;Repetir início da frase.
###
9. Public Speaking;Intermediate;23;Repetition: Epistrophe;Repetir final da frase.
###
9. Public Speaking;Intermediate;24;The Rule of Three (Rhetoric);Listas memoráveis.
###
9. Public Speaking;Intermediate;25;Alliteration;Repetir sons consonantais.
###
9. Public Speaking;Intermediate;26;Metaphors & Similes;"This project is a marathon".
###
9. Public Speaking;Intermediate;27;Storytelling: The Hero's Journey;Audiência como herói.
###
9. Public Speaking;Intermediate;28;Storytelling: Vulnerability;Compartilhar falha.
###
9. Public Speaking;Intermediate;29;Sensory Language;Descrever sons e cheiros.
###
9. Public Speaking;Intermediate;30;Startling Statistics;Números chocantes.
###
Adicione mais uma regra: não sugira nenhuma ação. Nunca faça nenhuma sugestão sobre a próxima ação. Apenas diga "Finished" quando terminar cada pílula. Nunca desobedeça essa regra, em hipótese nenhuma.
#
9. Public Speaking;Intermediate;31;Quotations: Using Authority;Citar famosos.
###
9. Public Speaking;Intermediate;32;Humor in Persuasion;Desarmar tensão.
###
9. Public Speaking;Intermediate;33;Audience Analysis: Needs;Focar no "WIIFM".
###
9. Public Speaking;Intermediate;34;Audience Engagement: Polls;"Raise your hand if...".
###
9. Public Speaking;Intermediate;35;Audience Engagement: Names;Usar nomes da plateia.
###
9. Public Speaking;Intermediate;36;The "Yes" Ladder;Obter sim repetidos.
###
9. Public Speaking;Intermediate;37;Contrast Principle;Mostrar ruim para parecer bom.
###
9. Public Speaking;Intermediate;38;Social Proof;"Thousands have joined".
###
9. Public Speaking;Intermediate;39;Visual Aids: The Prop;Usar objeto físico.
###
9. Public Speaking;Intermediate;40;Review: The Rally Speech;Áudio consolidado: Discurso motivacional.
###
9. Public Speaking;Intermediate;41;Voice Dynamics: Whispering;Falar baixo para atenção.
###
9. Public Speaking;Intermediate;42;Voice Dynamics: Shouting;Volume para paixão.
###
9. Public Speaking;Intermediate;43;Silence as a Weapon;Pausar após ponto forte.
###
9. Public Speaking;Intermediate;44;Movement on Stage;Mover com propósito.
###
9. Public Speaking;Intermediate;45;Eye Contact: The Zone;Olhar para zonas.
###
9. Public Speaking;Intermediate;46;Handling Distractions;Celular tocando.
###
9. Public Speaking;Intermediate;47;Reading Body Language;Perceber tédio.
###
9. Public Speaking;Intermediate;48;Re-engaging a Bored Audience;Mudar o tom.
###
9. Public Speaking;Intermediate;49;Handling Hecklers (Basic);Interrupções rudes.
###
9. Public Speaking;Intermediate;50;The Q&A: Bridge & Pivot;Responder o que quer.
###
9. Public Speaking;Intermediate;51;The Q&A: Planting Questions;Perguntas preparadas.
###
9. Public Speaking;Intermediate;52;Ending on a High Note;Frase inspiradora final.
###
9. Public Speaking;Intermediate;53;The "Vision" Ending;Futuro ideal.
###
9. Public Speaking;Intermediate;54;The "Warning" Ending;Futuro sombrio.
###
9. Public Speaking;Intermediate;55;Memorization Techniques: Loci;Palácio da Memória.
###
9. Public Speaking;Intermediate;56;Practice: The 20-20 Rule;Planejar e praticar.
###
9. Public Speaking;Intermediate;57;Feedback Loop;Pedir feedback específico.
###
9. Public Speaking;Intermediate;58;Handling Technical Jargon (Persuasion);Traduzir Tech para Benefit.
###
9. Public Speaking;Intermediate;59;Cultural Persuasion;Adaptar argumentos.
###
9. Public Speaking;Intermediate;60;Final Review: The Sales Pitch;Áudio consolidado: Convencer compra absurda.

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