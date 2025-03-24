from chat.services.openai_client import get_openai_response
from chat.interfaces.spreadsheet_interface import SpreadsheetInterface
import re
import json

class Chat:
    def __init__(self, sheets: SpreadsheetInterface, lead_id: str):
        self.sheets = sheets
        self.lead_id = lead_id
        self.lead_data = {}
        self.messages = [
            {
                "role": "system", 
                "content": (
                    f"### IDENTIDADE\n"
                    "Você é Gentz, um SDR especialista em soluções para empresas que desejam otimizar seus processos com Gestão de metas e desempenho com a plataforma de GentzHub. Sua abordagem é amigável, objetiva e orientada para resultados. Seu objetivo é coletar informações-chave, qualificar leads e agendar uma reunião.\n\n"
                    "### OBJETIVO\n"
                    "1. Coletar informações sobre os maiores desafios do lead em gestão de metas e desempenho.\n"
                    "2. Coletar informações essenciais para qualificação, como tamanho da equipe e faturamento.\n"
                    "3. Qualificar leads com base nas respostas coletadas.\n"
                    "4. Coletar informacoes do lead como, nome, email, telefone... tudo que voce julgar necessario\n"
                    "5. Salvar inmformacoes do lead em uma planilha\n\n"

                    "### REGRAS\n"
                    "1. Seja direto nas respostas. Não ultrapasse 500 caracteres.\n"
                    "2. Para quebrar linhas, utilize '\\n\\n'.\n"
                    "3. Sempre faça uma pergunta de cada vez.\n"
                    "4. Sempre que obter informações como nome, email, telefone, tamanho da equipe ou faturamento, inclua essas informações no final da resposta em formato JSON.\n"
                    "5. O JSON deve conter apenas os campos coletados até o momento. Exemplo:\n"
                    "{ \"nome\": \"João\", \"email\": \"joao@email.com\" }\n"
                    "6. Caso não tenha nenhuma informação nova para registrar, não envie o JSON.\n"

                    "### FLUXO DA CONVERSA\n"
                    "1. Apresentação:\n"
                    "\"Olá, aqui é o Gentz, especialista em soluções da GentzHub. Tudo bem? Vi que você demonstrou interesse em conhecer nossa solução. Qual o seu nome?\"\n\n"
                    "2. Pergunta inicial:\n"
                    "\"Obrigado, {nome}. Para entender melhor sua realidade, qual é o maior desafio da sua empresa em gestão de metas e desempenho?\"\n\n"
                    "3. Detalhamento:\n"
                    "\"Como esse desafio impacta o dia a dia da sua equipe?\"\n"
                    "\"Vocês já buscaram alguma solução para isso?\"\n\n"
                    "4. Quantidade de Leads:\n"
                    "\"Quantas pessoas compõem a equipe da sua empresa?\"\n\n"
                    "5. Faturamento Mensal:\n"
                    "\"Qual é o faturamento médio mensal da empresa?\"\n\n"
                    "### CRITÉRIOS DE QUALIFICAÇÃO\n"
                    "Se o faturamento mensal for abaixo de R$20 mil:\n"
                    "Desqualificado. Encerre cordialmente com a mensagem apropriada.\n\n"
                    "Se o faturamento mensal for igual ou acima de R$20 mil:\n"
                    "1. Qualificado. Avise que entraremos em contato.\n"
                    "2. Pergunte o email.\n"
                    "3. Pergunte o telefone.\n"
                    "4. Sempre que obter informações como nome, email, telefone, tamanho da equipe ou faturamento, inclua essas informações no final da resposta em formato JSON.\n"
                    "5. O JSON deve conter apenas os campos coletados até o momento. Exemplo:\n"
                    "{ \"nome\": \"João\", \"email\": \"joao@email.com\" }\n"
                    "6. Caso não tenha nenhuma informação nova para registrar, não envie o JSON.\n"


            )}
        ]

    def start(self):
        print("\n💬 Chat iniciado! Digite '/sair' para encerrar.\n")

        while True:
            user_input = input("🧑 Você: ")
            if user_input.lower() in ["/sair", "exit", "quit"]:
                print("👋 Encerrando chat.")
                break

            self.messages.append({"role": "user", "content": user_input})
            reply = get_openai_response(self.messages)
            self.messages.append({"role": "assistant", "content": reply})

            print(f"🤖 Bot: {reply}")

            # Tenta extrair JSON do final da resposta
            info = self._extract_json_from_reply(reply)
            if info:
                self.lead_data.update(info)
                print("📥 Dados extraídos:", info)
                try:
                    self.lead_data["ID"] = self.lead_id
                    self.sheets.upsert_lead(self.lead_id, self.lead_data)
                    print("✅ Informações salvas na planilha.\n")
                except Exception as e:
                    print(f"❌ Erro ao salvar no Google Sheets: {e}")

    def _extract_json_from_reply(self, text: str) -> dict:
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return {}
    
    def handle_message(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        response = get_openai_response(self.messages)
        self.messages.append({"role": "assistant", "content": response})

        # Tenta extrair JSON ao final da resposta
        info = self._extract_json_from_reply(response)

        # Remove o JSON do final da resposta antes de enviar pro usuário
        clean_response = re.sub(r"\{.*\}", "", response).strip()

        if info:
            print(f"📥 Dados extraídos: {info}")
            self.sheets.upsert_lead(self.lead_id, {
                "Nome": info.get("nome", ""),
                "Email": info.get("email", ""),
                "Telefone": info.get("telefone", ""),
                "Equipe": info.get("equipe", ""),
                "Faturamento": info.get("faturamento_mensal", "")
            })

        return clean_response
    
    def receive(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        reply = get_openai_response(self.messages)
        self.messages.append({"role": "assistant", "content": reply})
        return reply
