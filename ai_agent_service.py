#!/usr/bin/env python3
"""
🤖 AI AGENT SERVICE - Serviço de Automação com IA
V1.0 - Pronto para vender
"""

import json
import time
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================
SERVICE_NAME = "AI Agent Service"
PRICING = {
    "basico": {"price": 97, "name": "Agente Basic", "features": ["1 agente", "100 msgs/dia", "Suporte email"]},
    "pro": {"price": 297, "name": "Agente Pro", "features": ["3 agentes", "1000 msgs/dia", "Suporte priority", "API access"]},
    "enterprise": {"price": 997, "name": "Agente Enterprise", "features": ["10 agentes", "Ilimitado", "Suporte 24/7", "API", "Integrações"]}
}

# ==================== AGENTES PRONTOS ====================
AGENTS = {
    "atendente": {
        "name": "Atendente Virtual",
        "description": "Atende clientes 24/7",
        "system_prompt": "Você é um atendente virtual educado e eficiente. Responda sempre de forma útil e amable.",
        "price": 97
    },
    "vendas": {
        "name": "Assistente de Vendas",
        "description": "Auxilia no processo de vendas",
        "system_prompt": "Você é um vendedor expert. Ajude o cliente a encontrar o melhor produto e cierre a venda.",
        "price": 147
    },
    "suporte": {
        "name": "Suporte Técnico",
        "description": "Resolve problemas técnicos",
        "system_prompt": "Você é um suporte técnico especializado. Seja claro, objetivo e resolva o problema do cliente.",
        "price": 197
    },
    "analista": {
        "name": "Analista de Dados",
        "description": "Analisa dados e gera relatórios",
        "system_prompt": "Você é um analista de dados expert. Analise os dados e gere insights acionáveis.",
        "price": 297
    },
    "rh": {
        "name": "Assistente RH",
        "description": "Auxilia em tarefas de RH",
        "system_prompt": "Você é um especialista em RH. Ajude com recrutamento, benefícios e políticas internas.",
        "price": 197
    }
}

# ==================== CORE FUNCTIONS ====================
class AIService:
    def __init__(self):
        self.users = {}
        self.conversations = {}
        self.agents = AGENTS
        
    def create_user(self, name, email, plan="basico"):
        user_id = f"user_{len(self.users) + 1}"
        self.users[user_id] = {
            "name": name,
            "email": email,
            "plan": plan,
            "agents": [],
            "messages_today": 0,
            "created_at": datetime.now().isoformat()
        }
        return user_id
    
    def add_agent(self, user_id, agent_type):
        if agent_type not in self.agents:
            return False, "Agente não existe"
        
        if len(self.users[user_id]["agents"]) >= len(PRICING[self.users[user_id]["plan"]]["features"]) // 2:
            return False, "Limite do plano atingido"
        
        self.users[user_id]["agents"].append(agent_type)
        return True, f"Agente {self.agents[agent_type]['name']} adicionado"
    
    def chat(self, user_id, message):
        user = self.users.get(user_id)
        if not user:
            return "Usuário não encontrado"
        
        # Simula resposta do agente
        agents = user.get("agents", ["atendente"])
        agent_key = agents[0]
        agent = self.agents.get(agent_key, self.agents["atendente"])
        
        response = f"[{agent['name']}] Entendi sua mensagem: '{message}'. Como posso ajudar?"
        
        # Registra conversa
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        self.conversations[user_id].append({
            "user": message,
            "agent": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def get_analytics(self, user_id):
        convs = self.conversations.get(user_id, [])
        return {
            "total_conversas": len(convs),
            "agentes_usados": self.users.get(user_id, {}).get("agents", []),
            "plano": self.users.get(user_id, {}).get("plan", "N/A")
        }

# ==================== API SIMPLES ====================
def main():
    service = AIService()
    
    print("""
╔═══════════════════════════════════════════════════╗
║   🤖 AI AGENT SERVICE - Pronto para Vender        ║
╚═══════════════════════════════════════════════════╝
    """)
    
    # Demo
    user_id = service.create_user("Cliente Demo", "demo@email.com", "pro")
    print(f"✅ Usuário criado: {user_id}")
    
    # Adiciona agentes
    service.add_agent(user_id, "atendente")
    service.add_agent(user_id, "vendas")
    print("✅ Agentes adicionados")
    
    # Testa chat
    response = service.chat(user_id, "Olá, preciso de ajuda")
    print(f"💬 Resposta: {response}")
    
    # Analytics
    stats = service.get_analytics(user_id)
    print(f"📊 Stats: {stats}")
    
    print("\n🚀 Sistema pronto! Integre com WhatsApp/Telegram e comece a vender!")


if __name__ == "__main__":
    main()
