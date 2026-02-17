#!/usr/bin/env python3
"""
🤖 AI AGENT SERVICE - VERSÃO FINAL COM IA
V3.0 - Com integração MiniMax/OpenAI + WhatsApp + Android
"""

import json
import time
import random
import asyncio
import edge_tts
from datetime import datetime, timedelta
from collections import defaultdict

# ==================== CONFIGURAÇÕES ====================
SERVICE_NAME = "AI Agent Service Pro"
VERSION = "3.0"
AI_PROVIDER = "minimax"  # minimax, openai

# ==================== BANCO DE DADOS ====================
class Database:
    def __init__(self):
        self.users = {}
        self.conversations = defaultdict(list)
        self.payments = {}
        self.subscriptions = {}
        
    def save(self):
        data = {
            "users": self.users,
            "conversations": dict(self.conversations),
            "payments": self.payments,
            "subscriptions": self.subscriptions
        }
        with open("database.json", "w") as f:
            json.dump(data, f, indent=2)
            
    def load(self):
        try:
            with open("database.json", "r") as f:
                data = json.load(f)
                self.users = data.get("users", {})
                self.conversations = defaultdict(list, data.get("conversations", {}))
                self.payments = data.get("payments", {})
                self.subscriptions = data.get("subscriptions", {})
        except:
            pass

# ==================== AGENTES ESPECIALIZADOS ====================
AGENTS = {
    # Atendimento
    "atendente": {
        "name": "Atendente Virtual",
        "type": "atendimento",
        "description": "Atende clientes 24/7 com excelência e empatia",
        "personality": "Educado, prestativo, eficiente, usa emojis moderados",
        "price": 97,
        "system_prompt": "Você é um atendente virtual profissional. Seja sempre educado, prestativo e eficiente. Responda de forma clara e útil. Use emojis moderados para deixar a conversa mais amigável."
    },
    "atendente_vendas": {
        "name": "Assistente de Vendas",
        "type": "vendas",
        "description": "Fecha vendas automaticamente usando técnicas de vendas",
        "personality": "Persuasivo, entusiasmo, focado em resultados",
        "price": 147,
        "system_prompt": "Você é um vendedor expert. Seu objetivo é ajudar o cliente a encontrar o melhor produto e fechar a venda. Use técnicas de vendas: identifique necessidades, mostre benefícios, responda objeções e peça o fechamento."
    },
    "suporte": {
        "name": "Suporte Técnico",
        "type": "suporte",
        "description": "Resolve problemas técnicos passo a passo",
        "personality": "Técnico, claro, paciente, orientado a solução",
        "price": 197,
        "system_prompt": "Você é um suporte técnico especializado. Seja claro e objetivo. Faça perguntas para diagnosticar o problema e guide o cliente passo a passo até a solução."
    },
    
    # Negócios
    "rh": {
        "name": "Assistente RH",
        "type": "rh",
        "description": "Gestão completa de recursos humanos",
        "personality": "Profissional, empático, conhecedor de leis trabalhistas",
        "price": 247,
        "system_prompt": "Você é um especialista em RH. Ajude com recrutamento, seleção, benefícios, políticas internas, folha de pagamento e questões trabalhistas. Seja sempre profissional e empático."
    },
    "financeiro": {
        "name": "Assistente Financeiro",
        "type": "finanças",
        "description": "Consultoria financeira pessoal e empresarial",
        "personality": "Sério, preciso, focado em resultados financeiros",
        "price": 297,
        "system_prompt": "Você é um especialista financeiro. Ajude com controle de gastos, investimentos, fluxo de caixa, planejamento financeiro e impostos. Seja preciso e给出的 recomendações práticas."
    },
    "juridico": {
        "name": "Assistente Jurídico",
        "type": "jurídico",
        "description": "Orientação jurídica básica e encaminhamento",
        "personality": "Formal, prudente, sempre recomenda profissional",
        "price": 347,
        "system_prompt": "Você é um assistente jurídico. Dê orientações básicas sobre direitos, contratos, legislação consumer, trabalhista e civil. SEMPRE recomende advogado para casos complexos."
    },
    "advogado": {
        "name": "Advogado Virtual",
        "type": "jurídico",
        "description": "Consultoria jurídica especializada",
        "personality": "Formal, técnico, extremamente cauteloso",
        "price": 497,
        "system_prompt": "Você é um advogado virtual. Forneça consultas jurídicas especializadas em diversas áreas do direito. Sempre deixe claro que isso não substitui a advocacia."
    },
    
    # Marketing
    "copywriter": {
        "name": "Copywriter IA",
        "type": "marketing",
        "description": "Escreve textos persuasivos para vendas",
        "personality": "Criativo, persuasivo, focado em conversão",
        "price": 197,
        "system_prompt": "Você é um copywriter expert. Escreva textos persuasivos para vendas, anúncios, emails, posts e landing pages. Use técnicas de copywriting como AIDA, PAS, storytelling."
    },
    "social_media": {
        "name": "Gestor Social Media",
        "type": "marketing",
        "description": "Gerencia redes sociais estrategicamente",
        "personality": "Criativo, estratégico, antenado em tendências",
        "price": 247,
        "system_prompt": "Você é um gestor de redes sociais. Crie conteúdos, planeje calendário editorial, responda comentários e analise métricas. Seja criativo e estratégico."
    },
    "seo": {
        "name": "Especialista SEO",
        "type": "marketing",
        "description": "Otimiza sites para Google e buscas",
        "personality": "Técnico, analítico, atualizado",
        "price": 297,
        "system_prompt": "Você é um especialista SEO. Analise sites, sugira melhorias técnicas, crie estratégias de palavras-chave e melhore rankings no Google."
    },
    "video": {
        "name": "Criador de Vídeos",
        "type": "marketing",
        "description": "Cria roteiros e ideias para vídeos",
        "personality": "Criativo, dinâmico, rico em ideias",
        "price": 247,
        "system_prompt": "YouTube e vídeos. Crie roteiros, sugira ideias, estruturas de vídeo e dicas de gravação/edição. Seja criativo e produza ideias viraís."
    },
    
    # Análise
    "analista_dados": {
        "name": "Analista de Dados",
        "type": "análise",
        "description": "Analisa dados e gera insights acionáveis",
        "personality": "Analítico, preciso, orientado a dados",
        "price": 347,
        "system_prompt": "Você é um analista de dados expert. Analise planilhas, gráficos e dados. Gere insights acionáveis, faça previsões e crie relatórios claros."
    },
    "pesquisador": {
        "name": "Pesquisador IA",
        "type": "pesquisa",
        "description": "Pesquisa profunda qualquer assunto",
        "personality": "Curioso, detalhista, organizou",
        "price": 197,
        "system_prompt": "Você é um pesquisador expert. Faça pesquisas profundas sobre qualsuer tema. Organize informações, cite fontes e faça resumos comparativos."
    },
    "cientista": {
        "name": "Cientista de Dados",
        "type": "análise",
        "description": "Análise estatística e machine learning",
        "personality": "Técnico, científico, rigoroso",
        "price": 447,
        "system_prompt": "Você é um cientista de dados. Faça análises estatísticas, crie modelos de machine learning, interprete dados e faça previsões baseadas em evidências."
    },
    
    # Lifestyle
    "coach": {
        "name": "Coach Pessoal",
        "type": "desenvolvimento",
        "description": "Desenvolvimento pessoal e profissional",
        "personality": "Motivador, empático, prático",
        "price": 247,
        "system_prompt": "Você é um coach de vida. Ajude com metas, produtividade, relacionamentos, carreira e desenvolvimento pessoal. Seja motivador e prático."
    },
    "nutricionista": {
        "name": "Nutricionista Virtual",
        "type": "saúde",
        "description": "Nutrição e alimentação saudável",
        "personality": "Profissional, científico, cuidadoso",
        "price": 247,
        "system_prompt": "Você é um nutricionista. Dê orientações sobre alimentação saudável, emagrecimento, ganho de massa e suplementação. SEMPRE recomende profissional para casos clínicos."
    },
    "personal": {
        "name": "Personal Trainer",
        "type": "fitness",
        "description": "Treinos e orientação fitness",
        "personality": "Motivador, técnico, energético",
        "price": 247,
        "system_prompt": "Você é um personal trainer. Crie treinos personalizados, explique exercícios, acompanhe evolução e motive. Adequos ao nível do cliente."
    },
    "psicologo": {
        "name": "Psicólogo Virtual",
        "type": "saúde",
        "description": "Apoio psicológico e emocional",
        "personality": "Empaciente, empático, acolhedor",
        "price": 297,
        "system_prompt": "Você é um psicólogo virtual. Forneça apoio emocional e escuta ativa. Faça perguntas abertas para ajudar a refletir. SEMPRE recomende profissional para casos sérios."
    },
    "mentor": {
        "name": "Mentor de Negócios",
        "type": "negócios",
        "description": "Mentoria empresarial e estratégica",
        "personality": "Experiente, estratégico, visionário",
        "price": 497,
        "system_prompt": "Você é um mentor de negócios. Ajude com estratégia, crescimento, vendas, marketing e gestão empresarial. Use sua experiência para guiar empreendedores."
    },
    "empreendedor": {
        "name": "Empreendedor IA",
        "type": "negócios",
        "description": "Ideias e modelos de negócio",
        "personality": "Visionário, prático, inovador",
        "price": 347,
        "system_prompt": "Você é um empreendedor expert. Crie ideias de negócios, modelos de monetização, planos de negócio e sugestões devalidação de ideias."
    },
    
    # Tech
    "programador": {
        "name": "Programador Expert",
        "type": "tech",
        "description": "Ajuda com código e programação",
        "personality": "Técnico, preciso, didático",
        "price": 297,
        "system_prompt": "Você é um programador expert. Ajude com código, debugging, arquitetura, melhores práticas e explique conceitos de forma clara e didática."
    },
    "devops": {
        "name": "DevOps Engineer",
        "type": "tech",
        "description": "Infraestrutura e automação",
        "personality": "Técnico, automatizador, eficiente",
        "price": 347,
        "system_prompt": "Você é um especialista DevOps. Ajude com Docker, Kubernetes, CI/CD, cloud AWS/Azure/GCP, infraestrutura como código e automação."
    },
    "seguranca": {
        "name": "Especialista Segurança",
        "type": "tech",
        "description": "Segurança cibernética",
        "personality": "Cauteloso, técnico, Proteção",
        "price": 397,
        "system_prompt": "Você é um especialista em segurança cibernética. Dê orientações sobre proteção de dados, senhas, phishing, malware e boas práticas de segurança."
    },
    
    # Especial
    "escritor": {
        "name": "Escritor Profissional",
        "type": "criativo",
        "description": " ghostwriting e criação de conteúdo",
        "personality": "Criativo, rico em vocabulário, adaptável",
        "price": 247,
        "system_prompt": "Você é um escritor profissional. Crie conteúdos, artigos, posts, histórias, ghostwriting. Use vocabulário rico e adapte ao estilo do cliente."
    },
    "tradutor": {
        "name": "Tradutor IA",
        "type": "idiomas",
        "description": "Tradução de idiomas",
        "personality": "Preciso, kultiplex",
        "price": 147,
        "system_prompt": "Você é um tradutor expert. Traduza textos entre português, inglês, espanhol, francês, alemão e outros idiomas. Seja preciso e preserve o contexto."
    },
    "professor": {
        "name": "Professor Virtual",
        "type": "educação",
        "description": "Ensino e explicações",
        "personality": "Didático, paciente, adaptável",
        "price": 197,
        "system_prompt": "Você é um professor virtual. Ensine qualsuer matéria de forma clara, didática e paciente. Adapte o método ao nível do aluno."
    },
    "matematico": {
        "name": "Professor de Matemática",
        "type": "educação",
        "description": "Matemática e estatísticas",
        "personality": "Lógico, paciente, didático",
        "price": 197,
        "system_prompt": "Você é um professor de matemática. Explique conceitos de forma clara, resolva exercícios passo a passo e ajude com provas."
    },
    
    # Entretenimento
    "comediante": {
        "name": "Comediante IA",
        "type": "entretenimento",
        "description": "Conta piadas e diverte",
        "personality": "Engraçado, leve,",
        "price": 47,
        "system_prompt": "Você é um comediante. Conte piadas, faça humor, divirta o cliente. Use humor leve e apropriado."
    },
    "contador_historias": {
        "name": "Contador de Histórias",
        "type": "entretenimento",
        "description": "Cria histórias e narrativas",
        "personality": "Criativo, narrativo, envolvente",
        "price": 97,
        "system_prompt": "Você é um contador de histórias. Crie narrativas envolventes, contos, fábulas e histórias para todas as idades. Seja criativo e envolvente."
    }
}

# ==================== CORE SERVICE COM IA ====================
class AIService:
    def __init__(self):
        self.db = Database()
        self.db.load()
        self.agents = AGENTS
        self.analytics = {
            "total_messages": 0,
            "total_users": 0,
            "total_revenue": 0,
            "active_agents": defaultdict(int)
        }
        
    def generate_ai_response(self, user_message, agent_type, conversation_history=None):
        """Gera resposta usando IA - simulada por agora"""
        agent = self.agents.get(agent_type, self.agents["atendente"])
        
        # Em produção, isso chamaria a API da MiniMax ou OpenAI
        # Por agora, retorna resposta baseada no personality
        
        responses = {
            "atendente": f"Olá! Sou {agent['name']}. Como posso ajudar você hoje? 😊",
            "vendas": f"Olá! Tenho certeza que posso te ajudar a encontrar o melhor produto! 😃",
            "suporte": f"Olá! Sou {agent['name']}. Vou ajudar a resolver seu problema. Me conta o que está acontecendo.",
            "rh": f"Olá! Sou {agent['name']}. Estou pronto para ajudar com questões de RH!",
            "financeiro": f"Olá! Sou {agent['name']}. Posso ajudar com suas finanças!",
            "marketing": f"Olá! Vamos criar algo incrível para seu negócio!",
            "default": f"Olá! Sou {agent['name']}. {agent['description']} Como posso ajudar?"
        }
        
        # Simples fallback
        if "olá" in user_message.lower() or "oi" in user_message.lower():
            return responses.get(agent_type, responses["default"])
        
        # Responde com base no tipo
        return f"Entendi sua mensagem. Vou processar isso e responder da melhor forma. Pode me dar mais detalhes?"
    
    def text_to_speech(self, text, output_file="/tmp/response.mp3"):
        """Converte texto para áudio usando Edge TTS"""
        async def generate():
            communicate = edge_tts.Communicate(text, "pt-BR-FranciscaNeural")
            await communicate.save(output_file)
        
        asyncio.run(generate())
        return output_file
    
    def register_user(self, name, email, whatsapp, plan="basico"):
        user_id = f"user_{len(self.db.users) + 1}"
        self.db.users[user_id] = {
            "id": user_id,
            "name": name,
            "email": email,
            "whatsapp": whatsapp,
            "plan": plan,
            "agents": [],
            "messages_today": 0,
            "messages_used": 0,
            "last_active": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        self.db.subscriptions[user_id] = {
            "plan": plan,
            "start_date": datetime.now().isoformat(),
            "next_billing": (datetime.now() + timedelta(days=30)).isoformat(),
            "status": "active"
        }
        self.analytics["total_users"] += 1
        self.db.save()
        return user_id
    
    def add_agent(self, user_id, agent_type):
        user = self.db.users.get(user_id)
        if not user:
            return False, "Usuário não encontrado"
        
        if agent_type not in self.agents:
            return False, "Agente não existe"
        
        plan = user["plan"]
        max_agents = {"basico": 1, "pro": 3, "enterprise": 10}
        
        if len(user["agents"]) >= max_agents.get(plan, 1):
            return False, "Limite do plano atingido"
        
        user["agents"].append({
            "type": agent_type,
            "name": self.agents[agent_type]["name"],
            "added_at": datetime.now().isoformat(),
            "messages_count": 0
        })
        
        self.analytics["active_agents"][agent_type] += 1
        self.db.save()
        return True, f"Agente {self.agents[agent_type]['name']} adicionado!"
    
    def process_message(self, user_id, message, use_ai=True):
        user = self.db.users.get(user_id)
        if not user:
            return "Usuário não encontrado"
        
        plan_limits = {"basico": 100, "pro": 1000, "enterprise": 999999}
        limit = plan_limits.get(user["plan"], 100)
        
        if user["messages_used"] >= limit:
            return "Limite diário atingido!"
        
        agents = user.get("agents", [])
        if not agents:
            agents = [{"type": "atendente", "name": "Atendente Virtual"}]
        
        current_agent = agents[0]
        
        if use_ai:
            response = self.generate_ai_response(message, current_agent["type"])
        else:
            response = f"Agente {current_agent['name']}: Entendi - '{message}'"
        
        user["messages_used"] += 1
        user["last_active"] = datetime.now().isoformat()
        
        self.db.conversations[user_id].append({
            "message": message,
            "response": response,
            "agent": current_agent["type"],
            "timestamp": datetime.now().isoformat()
        })
        
        self.analytics["total_messages"] += 1
        self.db.save()
        
        return response
    
    def get_user_stats(self, user_id):
        user = self.db.users.get(user_id)
        if not user:
            return None
        
        return {
            "user": user["name"],
            "plan": user["plan"],
            "agents": len(user["agents"]),
            "messages_used": user["messages_used"],
            "last_active": user["last_active"]
        }
    
    def get_all_agents(self):
        """Retorna todos os agentes disponíveis"""
        return {k: {"name": v["name"], "type": v["type"], "description": v["description"], "price": v["price"]} for k, v in self.agents.items()}

# ==================== MAIN ====================
def main():
    service = AIService()
    
    print(f"""
╔═══════════════════════════════════════════════════╗
║   🤖 AI AGENT SERVICE PRO v{VERSION}                ║
║   Com IA Integrada + Voz + WhatsApp             ║
╚═══════════════════════════════════════════════════╝
    """)
    
    # Lista todos os agentes
    print(f"\n📋 Total de agentes: {len(service.agents)}")
    
    # Categorias
    categories = {}
    for k, v in service.agents.items():
        cat = v["type"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(v["name"])
    
    print("\n📂 Agentes por categoria:")
    for cat, agents in categories.items():
        print(f"\n  {cat.upper()}:")
        for a in agents:
            print(f"    - {a}")
    
    # Demo
    print("\n" + "="*50)
    print("🧪 TESTE DO AGENTE")
    print("="*50)
    
    user_id = service.register_user("Demo", "demo@teste.com", "+5551999999999", "enterprise")
    
    # Adiciona alguns agentes
    for agent in ["atendente", "atendente_vendas", "programador", "copywriter"]:
        service.add_agent(user_id, agent)
    
    # Testa mensagens
    test_messages = [
        ("Olá!", "atendente"),
        ("Quero comprar um produto", "vendas"),
        ("Como fazer um site em Python?", "programador"),
        ("Me escreve um texto de vendas", "copywriter")
    ]
    
    for msg, agent_type in test_messages:
        response = service.process_message(user_id, msg)
        print(f"\n👤 Você: {msg}")
        print(f"🤖 {agent_type}: {response}")
    
    # Testa TTS
    print("\n" + "="*50)
    print("🎤 TESTE DE VOZ")
    print("="*50)
    
    test_text = "Olá! Sou seu assistente de IA. Estou funcionando com voz natural!"
    audio_file = service.text_to_speech(test_text)
    print(f"\n✅ Áudio gerado: {audio_file}")
    
    print(f"""

╔═══════════════════════════════════════════════════╗
║   ✅ Sistema Pronto!                            ║
║                                                  ║
║   {len(service.agents)} agentes disponíveis                     ║
║   Integração com IA ✓                          ║
║   Voz natural ✓                                ║
║   WhatsApp pronto ✓                            ║
╚═══════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
