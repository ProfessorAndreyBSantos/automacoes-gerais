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
9. Public Speaking;Advanced;01;The Art of Rhetoric: Introduction;Moldar realidade.
###
9. Public Speaking;Advanced;02;Advanced Repetition: Anaphora;Repetição no início.
###
9. Public Speaking;Advanced;03;Advanced Repetition: Epistrophe;Repetição no final.
###
9. Public Speaking;Advanced;04;Chiasmus (The Mirror Effect);Inverter estrutura.
###
9. Public Speaking;Advanced;05;Antithesis (Contrast);Ideias opostas.
###
9. Public Speaking;Advanced;06;The Rule of Three (The Tricolon);Listas rítmicas.
###
9. Public Speaking;Advanced;07;Litotes (Understatement);Negação para afirmar.
###
9. Public Speaking;Advanced;08;Hyperbole (Strategic Exaggeration);Exagero emocional.
###
9. Public Speaking;Advanced;09;Metaphor Mastery;Imagens mentais.
###
9. Public Speaking;Advanced;10;Extended Metaphors;Metáfora longa.
###
9. Public Speaking;Advanced;11;Alliteration & Assonance;Sons memoráveis.
###
9. Public Speaking;Advanced;12;Polysyndeton (Adding Conjunctions);Muitos "E".
###
9. Public Speaking;Advanced;13;Asyndeton (Removing Conjunctions);Remover "E".
###
9. Public Speaking;Advanced;14;Rhetorical Questions (Hypophora);Perguntar e responder.
###
9. Public Speaking;Advanced;15;The "Soundbite" Science;Frases citáveis.
###
9. Public Speaking;Advanced;16;Cadence and Rhythm;Música na fala.
###
9. Public Speaking;Advanced;17;Active Verbs vs Nominalization;Verbos que sangram.
###
9. Public Speaking;Advanced;18;Sensory Details (VAK);Visual, Auditivo, Cinestésico.
###
9. Public Speaking;Advanced;19;Allusion (Cultural/Historical);Referenciar história.
###
9. Public Speaking;Advanced;20;Review: The Rhetorical Speech;Áudio consolidado: Usar figuras de linguagem.
###
9. Public Speaking;Advanced;21;Vocal Variety: The 4 Ps;Pitch, Pace, Power, Pause.
###
9. Public Speaking;Advanced;22;The Dramatic Pause;Tensão máxima.
###
9. Public Speaking;Advanced;23;The Stage Whisper;Intimidade.
###
9. Public Speaking;Advanced;24;Crescendo (Building Volume);Aumentar volume.
###
9. Public Speaking;Advanced;25;Decrescendo (Fading Out);Diminuir volume.
###
9. Public Speaking;Advanced;26;Tempo: Staccato;Palavras separadas.
###
9. Public Speaking;Advanced;27;Tempo: Legato;Fala fluida.
###
9. Public Speaking;Advanced;28;Tone: Warmth vs Authority;Amigo vs Líder.
###
9. Public Speaking;Advanced;29;Micro-expressions;Controle facial.
###
9. Public Speaking;Advanced;30;Gestures: The "Sphere of Power";Gestos amplos.
###
Adicione mais uma regra: não sugira nenhuma ação. Nunca faça nenhuma sugestão sobre a próxima ação. Apenas diga "Finished" quando terminar cada pílula. Nunca desobedeça essa regra, em hipótese nenhuma.
###
9. Public Speaking;Advanced;31;Anchoring the Stage;Mover para pontos específicos.
###
9. Public Speaking;Advanced;32;Removing Barriers;Sair de trás do púlpito.
###
9. Public Speaking;Advanced;33;Eye Contact: Intimacy;Conexão real.
###
9. Public Speaking;Advanced;34;Handling Emotion (Your Own);Emocionar-se sem perder controle.
###
9. Public Speaking;Advanced;35;Channeling Anger (Righteous);Raiva controlada.
###
9. Public Speaking;Advanced;36;Channeling Hope;Tom ascendente.
###
9. Public Speaking;Advanced;37;Dress for Impact;Psicologia das cores.
###
9. Public Speaking;Advanced;38;Using Silence to Punish/Control;Disciplina.
###
9. Public Speaking;Advanced;39;Prop Mastery (Advanced);Objetos teatrais.
###
9. Public Speaking;Advanced;40;Review: The Performance;Áudio consolidado: Recitar trecho famoso.
###
9. Public Speaking;Advanced;41;The "Visionary" Speech (Steve Jobs);Lançar ideia.
###
9. Public Speaking;Advanced;42;The "Underdog" Speech;Motivar time perdendo.
###
9. Public Speaking;Advanced;43;The Commencement Speech;Discurso de formatura.
###
9. Public Speaking;Advanced;44;The TED Talk Style;Fórmula de 18 minutos.
###
9. Public Speaking;Advanced;45;The Eulogy (Funeral Speech);Celebrar vida.
###
9. Public Speaking;Advanced;46;The Toast (Wedding/Gala);Brinde.
###
9. Public Speaking;Advanced;47;The Crisis Speech (Apology);Assumir erro.
###
9. Public Speaking;Advanced;48;The Acceptance Speech (Awards);Agradecer prêmio.
###
9. Public Speaking;Advanced;49;The Resignation Speech;Sair com classe.
###
9. Public Speaking;Advanced;50;The Keynote Address;Definir tom de evento.
###
9. Public Speaking;Advanced;51;The "Call to Arms";Mobilizar causa.
###
9. Public Speaking;Advanced;52;Storytelling: In Medias Res;Começar pelo meio.
###
9. Public Speaking;Advanced;53;Storytelling: The Loop;Histórias aninhadas.
###
9. Public Speaking;Advanced;54;Defining Your "Signature Story";História de origem.
###
9. Public Speaking;Advanced;55;Humor: The Call-Back;Piada recorrente.
###
9. Public Speaking;Advanced;56;Audience Interaction (Advanced);Interação entre audiência.
###
9. Public Speaking;Advanced;57;Handling Technical Disasters;Continuar sem microfone.
###
9. Public Speaking;Advanced;58;The "Mic Drop" Moment;Final forte.
###
9. Public Speaking;Advanced;59;Authenticity vs Performance;Paradoxo do ensaio.
###
9. Public Speaking;Advanced;60;Final Review: The Magnum Opus;Áudio consolidado: Discurso final.

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
