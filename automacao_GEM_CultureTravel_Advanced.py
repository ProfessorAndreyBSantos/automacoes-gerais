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
1. Travel & Culture;Advanced;01;Living Abroad: The Expat Life;Diferenciar turista de morador.
###
1. Travel & Culture;Advanced;02;Culture Shock Stages;Honeymoon, Frustration, Adjustment.
###
1. Travel & Culture;Advanced;03;Reverse Culture Shock;Voltar para casa.
###
1. Travel & Culture;Advanced;04;Bureaucracy Abroad;Vistos, impostos, aluguel.
###
1. Travel & Culture;Advanced;05;Healthcare Systems;Comparar SUS com outros.
###
1. Travel & Culture;Advanced;06;Education Systems;Escolas internacionais.
###
1. Travel & Culture;Advanced;07;Work Culture Global;Diferenças de escritório.
###
1. Travel & Culture;Advanced;08;Making Local Friends (Deep);Sair da bolha de expats.
###
1. Travel & Culture;Advanced;09;Bilingualism;Desafios de criar filhos bilingues.
###
1. Travel & Culture;Advanced;10;Identity and Belonging;Onde é "casa"?
###
1. Travel & Culture;Advanced;11;Travel Idioms: "Hit the road";Pegar a estrada.
###
1. Travel & Culture;Advanced;12;Travel Idioms: "Off the beaten track";Lugar pouco visitado.
###
1. Travel & Culture;Advanced;13;Travel Idioms: "Travel light";Viajar com pouco peso.
###
1. Travel & Culture;Advanced;14;Travel Idioms: "Itchy feet";Vontade de viajar.
###
1. Travel & Culture;Advanced;15;Travel Idioms: "Culture vulture";Amante de cultura.
###
1. Travel & Culture;Advanced;16;Slang: "Tourist trap";Lugar pega-turista.
###
1. Travel & Culture;Advanced;17;Slang: "Red-eye flight";Voo noturno.
###
1. Travel & Culture;Advanced;18;Slang: "Jet lag";Cansaço de fuso.
###
1. Travel & Culture;Advanced;19;Slang: "Staycation";Férias em casa.
###
1. Travel & Culture;Advanced;20;Review: Expat Advice;Áudio consolidado: Dar conselhos para quem vai morar fora.
###
1. Travel & Culture;Advanced;21;Rhetoric: Describing a Place;Criar uma imagem mental vívida.
###
1. Travel & Culture;Advanced;22;Sensory Details;Cheiros, sons, texturas.
###
1. Travel & Culture;Advanced;23;The Art of Conversation;Manter papo com estranhos.
###
1. Travel & Culture;Advanced;24;Diplomacy in Travel;Evitar conflito internacional.
###
1. Travel & Culture;Advanced;25;Nuance: "Trip" vs "Journey";Diferenças sutis.
###
1. Travel & Culture;Advanced;26;Nuance: "Custom" vs "Tradition";Antiguidade e hábito.
###
1. Travel & Culture;Advanced;27;Humor: Self-Deprecation;Rir dos próprios erros culturais.
###
1. Travel & Culture;Advanced;28;Storytelling: Pacing;Controlar a velocidade da história.
###
1. Travel & Culture;Advanced;29;Storytelling: Dialogue;Imitar vozes na história.
###
1. Travel & Culture;Advanced;30;Public Speaking: Toast;Fazer um brinde em casamento gringo.
###
1. Travel & Culture;Advanced;31;Global Issues: Migration;Discutir crise de refugiados.
###
1. Travel & Culture;Advanced;32;Global Issues: Climate;Impacto em ilhas e neve.
###
1. Travel & Culture;Advanced;33;Global Issues: Economy;Turismo como fonte de renda.
###
1. Travel & Culture;Advanced;34;Heritage Sites Protection;UNESCO e preservação.
###
1. Travel & Culture;Advanced;35;Indigenous Tourism;Ética e respeito.
###
1. Travel & Culture;Advanced;36;Dark Tourism;Visitar locais de tragédia (Chernobyl).
###
1. Travel & Culture;Advanced;37;Space Tourism;Futuro das viagens.
###
1. Travel & Culture;Advanced;38;Virtual Reality Travel;Substituto ou complemento?
###
1. Travel & Culture;Advanced;39;The End of Travel?;Mundo pós-pandemia.
###
1. Travel & Culture;Advanced;40;Review: The Global Citizen;Áudio consolidado: Discurso sobre cidadania global.
###
1. Travel & Culture;Advanced;41;Proficiency Simulation: The Local;Falar como um nativo.
###
1. Travel & Culture;Advanced;42;Proficiency: Dialects;Reconhecer Cockney, Southern US.
###
1. Travel & Culture;Advanced;43;Proficiency: Speed;Entender fala rápida.
###
###
1. Travel & Culture;Advanced;44;Proficiency: Mumbling;Entender fala pouco clara.
###
1. Travel & Culture;Advanced;45;Proficiency: Slang Mastery;Usar gíria sem parecer forçado.
###
1. Travel & Culture;Advanced;46;Proficiency: Idiom Mastery;Usar expressões no momento certo.
###
1. Travel & Culture;Advanced;47;Proficiency: Tone;Ser sarcástico ou formal.
###
1. Travel & Culture;Advanced;48;Proficiency: Humor;Fazer piadas em inglês.
###
1. Travel & Culture;Advanced;49;Proficiency: Debate;Argumentar sem perder a calma.
###
1. Travel & Culture;Advanced;50;Proficiency: Poetry/Lyrics;Entender arte local.
###
1. Travel & Culture;Advanced;51;Literature: Travel Writing;Ler trechos de livros de viagem.
###
1. Travel & Culture;Advanced;52;Movies: Analysis;Discutir filmes de estrada.
###
1. Travel & Culture;Advanced;53;Philosophy of Travel;Por que viajamos?
###
1. Travel & Culture;Advanced;54;Self-Discovery;Viagem interior.
###
1. Travel & Culture;Advanced;55;Minimalism in Travel;Viajar só com o essencial.
###
1. Travel & Culture;Advanced;56;Slow Travel;A arte de não ter pressa.
###
1. Travel & Culture;Advanced;57;Connection;O valor das pessoas vs lugares.
###
1. Travel & Culture;Advanced;58;Memory;Como lembramos das viagens.
###
1. Travel & Culture;Advanced;59;Transformation;Como a viagem nos muda.
###
1. Travel & Culture;Advanced;60;Final Review: The Meaning of Travel;Áudio consolidado: Reflexão filosófica final. 
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
