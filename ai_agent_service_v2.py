#!/usr/bin/env python3
"""
🤖 AI AGENT SERVICE - VERSÃO COMPLETA
V2.0 - Com muito mais funcionalidades
"""

import json
import time
import random
from datetime import datetime, timedelta
from collections import defaultdict

# ==================== CONFIGURAÇÕES ====================
SERVICE_NAME = "AI Agent Service Pro"
VERSION = "2.0"

PRICING = {
    "basico": {"price": 97, "name": "Starter", "features": ["1 agente", "100 msgs/dia", "Email support"]},
    "pro": {"price": 297, "name": "Pro", "features": ["3 agentes", "1000 msgs/dia", "Priority support", "API"]},
    "enterprise": {"price": 997, "name": "Enterprise", "features": ["10 agentes", "Ilimitado", "24/7 support", "API", "Integrações"]}
}

# ==================== AGENTES ESPECIALIZADOS ====================
AGENTS = {
    # Agentes de Atendimento
    "atendente": {
        "name": "Atendente Virtual",
        "type": "atendimento",
        "description": "Atende clientes 24/7 com excelência",
        "system_prompt": "Você é um atendente virtual profissional, educado e eficiente. Responda sempre de forma útil, amable e Objective. Use emojis moderadamente.",
        "price": 97,
        "skills": ["perguntas_frequentes", "triagem", "encaminhamento"]
    },
    "atendente_vendas": {
        "name": "Atendente de Vendas",
        "type": "vendas",
        "description": "Fecha vendas automaticamente",
        "system_prompt": "Você é um vendedor expert. Conecte clientes aos produtos certos, responda objeções, mostre benefícios e busque siempre fechar a venda. Use técnicas de vendas.",
        "price": 147,
        "skills": ["produtos", "objeções", "fechamento", "upsell"]
    },
    "suporte": {
        "name": "Suporte Técnico",
        "type": "suporte",
        "description": "Resolve problemas técnicos",
        "system_prompt": "Você é um suporte técnico especializado. Seja claro, objetivo e resolva o problema. Peça informações necessárias e guia passo a passo.",
        "price": 197,
        "skills": ["diagnostico", "soluções", "tutoriais"]
    },
    
    # Agentes de Negócios
    "rh": {
        "name": "Assistente RH",
        "type": "rh",
        "description": "Auxilia em gestão de pessoas",
        "system_prompt": "Você é um especialista em RH. Ajude com recrutamento, benefícios, políticas,folha de pagamento e desenvolvimento profissional.",
        "price": 247,
        "skills": ["recrutamento", "benefícios", "políticas", "dúvidas_funcionais"]
    },
    "financeiro": {
        "name": "Assistente Financeiro",
        "type": "finanças",
        "description": "Gerencia finanças pessoais e empresariais",
        "system_prompt": "Você é um especialista financeiro. Ajude com controle de gastos, investimentos, fluxo de caixa,impostos e planejamento financeiro.",
        "price": 297,
        "skills": ["gastos", "investimentos", "impostos", "planejamento"]
    },
    "juridico": {
        "name": "Assistente Jurídico",
        "type": "jurídico",
        "description": "Auxilia em questões legais básicas",
        "system_prompt": "Você é um assistente jurídico. Dê orientações básicas sobre direitos, contratos, lei consumer,trabalhista e civil. Sempre recomende advogado para casos complexos.",
        "price": 347,
        "skills": ["direitos", "contratos", "orientação"]
    },
    
    # Agentes de Produção
    "copywriter": {
        "name": "Copywriter IA",
        "type": "marketing",
        "description": "Escreve textos para vendas",
        "system_prompt": "Você é um copywriter expert. Escreva textos persuasivos, convincing para vendas,anúncios, emails, posts e landing pages. Use técnicas de copywriting.",
        "price": 197,
        "skills": ["vendas", "anúncios", "email", "posts"]
    },
    "social_media": {
        "name": "Gestor Social Media",
        "type": "marketing",
        "description": "Gerencia redes sociais",
        "system_prompt": "Você é um gestor de redes sociais. Crie conteúdos, planeje calendario,responda comentários e analise métricas.",
        "price": 247,
        "skills": ["conteúdo", "calendário", "engajamento", "métricas"]
    },
    "seo": {
        "name": "Especialista SEO",
        "type": "marketing",
        "description": "Otimiza sites para Google",
        "system_prompt": "Você é um especialista SEO. Analise sites, sugira melhorias, crie estratégias depalavras-chave e melhore rankings.",
        "price": 297,
        "skills": ["análise", "palavras_chave", "otimização", " backlinks"]
    },
    
    # Agentes de Análise
    "analista_dados": {
        "name": "Analista de Dados",
        "type": "análise",
        "description": "Analisa dados e gera insights",
        "system_prompt": "Você é um analista de dados expert. Analise planilhas, gráficos e dados. Gereinsights, sugira ações e faça previsões.",
        "price": 347,
        "skills": ["análise", "insights", "previsões", "relatórios"]
    },
    "pesquisador": {
        "name": "Pesquisador IA",
        "type": "pesquisa",
        "description": "Pesquisa qualquer assunto",
        "system_prompt": "Você é um pesquisador expert. Faça pesquisas profundas sobre qualsuer tema. Organize informações e cite fontes.",
        "price": 197,
        "skills": ["pesquisa", "fontes", "resumo", "comparação"]
    },
    
    # Agentes Lifestyle
    "coach": {
        "name": "Coach Pessoal",
        "type": "desenvolvimento",
        "description": "Acompanha desenvolvimento pessoal",
        "system_prompt": "Você é um coach de vida. Ajude com metas, produtividade, relacionamentos,carreira e desenvolvimento pessoal. Seja motivador e prático.",
        "price": 247,
        "skills": ["metas", "produtividade", "carreira", "relacionamentos"]
    },
    "nutricionista": {
        "name": "Nutricionista Virtual",
        "type": "saúde",
        "description": "Orienta sobre alimentação",
        "system_prompt": "Você é um nutricionista. Dê orientações sobre alimentação saudável,emagrecimento, ganho de massa e suplementação. Sempre recomende profissional para casos clínicos.",
        "price": 247,
        "skills": ["dieta", "emagrecimento", "massa", "suplementos"]
    },
    "personal": {
        "name": "Personal Trainer",
        "type": "fitness",
        "description": "Cria treinos personalizados",
        "system_prompt": "Você é um personal trainer. Crie treinos personalizados, explique exercícios,adore evolução e motive.",
        "price": 247,
        "skills": ["treinos", "exercícios", "evolução", "motivação"]
    }
}

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

# ==================== CORE SERVICE ====================
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
        
        # Verifica limite do plano
        plan = user["plan"]
        max_agents = {"basico": 1, "pro": 3, "enterprise": 10}
        
        if len(user["agents"]) >= max_agents.get(plan, 1):
            return False, "Limite do plano atingido"
        
        # Adiciona agente
        user["agents"].append({
            "type": agent_type,
            "name": self.agents[agent_type]["name"],
            "added_at": datetime.now().isoformat(),
            "messages_count": 0
        })
        
        self.analytics["active_agents"][agent_type] += 1
        self.db.save()
        return True, f"Agente {self.agents[agent_type]['name']} adicionado!"
    
    def process_message(self, user_id, message):
        user = self.db.users.get(user_id)
        if not user:
            return "Usuário não encontrado"
        
        # Verifica limite diário
        plan_limits = {"basico": 100, "pro": 1000, "enterprise": 999999}
        limit = plan_limits.get(user["plan"], 100)
        
        if user["messages_used"] >= limit:
            return "Limite diário atingido. Faça upgrade do plano!"
        
        # Escolhe agente
        agents = user.get("agents", [])
        if not agents:
            agents = [{"type": "atendente", "name": "Atendente Virtual"}]
        
        current_agent = agents[0]
        agent_data = self.agents.get(current_agent["type"], self.agents["atendente"])
        
        # Gera resposta (simulada - em produção usaria IA real)
        response = self._generate_response(message, agent_data, user)
        
        # Registra
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
    
    def _generate_response(self, message, agent_data, user):
        """Gera resposta baseada no tipo de agente"""
        agent_type = agent_data["type"]
        message_lower = message.lower()
        
        # Respostas específicas por tipo
        responses = {
            "atendimento": [
                f"Ola! Sou {agent_data['name']}. Como posso ajudar hoje?",
                "Entendi! Vou verificar e te responder.",
                "Posso ajudar com isso! Me conta mais detalhes.",
            ],
            "vendas": [
                "Ótimo interesse! Qual produto te chamou mais atenção?",
                "Temos promoções exclusivas hoje! Quer aproveitar?",
                "Posso te dar um desconto especial. Quer fechar?",
            ],
            "suporte": [
                "Vou analisar seu problema. Pode me dar mais detalhes?",
                "Entendi. Vou verificar no sistema e te ajudar.",
                "Preciso de algumas informações para resolver isso.",
            ],
            "rh": [
                "Sobre RH, posso ajudar com: recrutamento, benefícios, políticas.",
                "Vou verificar suas dúvidas sobre recursos humanos.",
                "Posso orientar sobre seus direitos trabalhistas.",
            ],
            "marketing": [
                "Vou criar um conteúdo especial para você!",
                "Isso vai viralizar! Tenho certeza.",
                "Posso otimizar suas métricas de engajamento.",
            ]
        }
        
        # Respostas genéricas
        generic = [
            "Interessante! Me conta mais sobre isso.",
            "Entendi! Posso ajudar com isso.",
            "Claro! Vou processar sua solicitação.",
            "Perfeito! Mais alguma coisa?",
        ]
        
        # Escolhe resposta
        if agent_type in responses:
            return random.choice(responses[agent_type])
        return random.choice(generic)
    
    def get_user_stats(self, user_id):
        user = self.db.users.get(user_id)
        if not user:
            return None
        
        convs = self.db.conversations.get(user_id, [])
        
        return {
            "user": user["name"],
            "plan": user["plan"],
            "agents": len(user["agents"]),
            "messages_used": user["messages_used"],
            "total_conversations": len(convs),
            "last_active": user["last_active"]
        }
    
    def upgrade_plan(self, user_id, new_plan):
        if new_plan not in PRICING:
            return False, "Plano inválido"
        
        user = self.db.users.get(user_id)
        if not user:
            return False, "Usuário não encontrado"
        
        old_plan = user["plan"]
        user["plan"] = new_plan
        
        self.db.subscriptions[user_id]["plan"] = new_plan
        self.db.save()
        
        return True, f"Plano atualizado de {old_plan} para {new_plan}!"
    
    def get_dashboard_stats(self):
        return {
            "total_users": len(self.db.users),
            "total_messages": self.analytics["total_messages"],
            "total_revenue": self.analytics["total_revenue"],
            "active_agents": dict(self.analytics["active_agents"]),
            "plans_distribution": self._get_plan_distribution()
        }
    
    def _get_plan_distribution(self):
        plans = {"basico": 0, "pro": 0, "enterprise": 0}
        for user in self.db.users.values():
            plan = user.get("plan", "basico")
            if plan in plans:
                plans[plan] += 1
        return plans

# ==================== API REST SIMPLES ====================
def main():
    service = AIService()
    
    print(f"""
╔═══════════════════════════════════════════════════╗
║   🤖 AI AGENT SERVICE PRO v{VERSION}                  ║
║   Sistema Completo de Automação com IA            ║
╚═══════════════════════════════════════════════════╝
    """)
    
    # Demo completa
    print("📊 Criando usuário demo...")
    user_id = service.register_user(
        name="Cliente Demo",
        email="demo@exemplo.com",
        whatsapp="+5551999999999",
        plan="pro"
    )
    print(f"✅ Usuário criado: {user_id}")
    
    # Adiciona agentes
    print("\n🤖 Adicionando agentes...")
    for agent in ["atendente", "atendente_vendas", "suporte", "copywriter"]:
        success, msg = service.add_agent(user_id, agent)
        print(f"   {msg}")
    
    # Testa conversas
    print("\n💬 Testando conversas...")
    test_messages = [
        "Olá, preciso de ajuda",
        "Quanto custa o produto?",
        "Quero fazer uma reclamação"
    ]
    
    for msg in test_messages:
        response = service.process_message(user_id, msg)
        print(f"   Você: {msg}")
        print(f"   IA: {response}\n")
    
    # Stats
    print("\n📊 Estatísticas do usuário:")
    stats = service.get_user_stats(user_id)
    print(f"   Nome: {stats['user']}")
    print(f"   Plano: {stats['plan']}")
    print(f"   Agentes: {stats['agents']}")
    print(f"   Mensagens: {stats['messages_used']}")
    print(f"   Conversas: {stats['total_conversations']}")
    
    print("\n📈 Estatísticas globais:")
    dashboard = service.get_dashboard_stats()
    print(f"   Usuários: {dashboard['total_users']}")
    print(f"   Mensagens: {dashboard['total_messages']}")
    print(f"   Planos: {dashboard['plans_distribution']}")
    
    print("""

╔═══════════════════════════════════════════════════╗
║   🚀 Sistema Pronto para Usar!                  ║
║                                                  ║
║   Próximos passos:                               ║
║   1. Integrar com WhatsApp/Telegram              ║
║   2. Conectar com IA real (OpenAI/MiniMax)      ║
║   3. Colocar para rodar 24/7                    ║
║   4. Começar a vender!                           ║
╚═══════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
