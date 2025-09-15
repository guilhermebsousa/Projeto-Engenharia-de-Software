import os
import sys
import openai
from sqlalchemy.orm import Session
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.models.products import Product
from typing import List, Dict, Any
import json

class AIStockAgent:
    def __init__(self):
        # Configurar a API da OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY não está definida. Verifique o arquivo .env")
        
        self.client = openai.OpenAI(api_key=openai.api_key)
    
    def get_all_product_names(self) -> List[Dict[str, str]]:
        """Busca todos os nomes e marcas de produtos do banco para usar como contexto"""
        db = SessionLocal()
        try:
            products = db.query(Product.name, Product.brand).distinct().all()
            product_info = []
            for product in products:
                product_dict = {
                    "brand": product.brand if product.brand else "",
                    "product": product.name
                }
                product_info.append(product_dict)
            print(product_info)

            return product_info
        finally:
            db.close()
    
    def get_product_context(self) -> str:
        """Prepara o contexto com todos os produtos disponíveis"""
        product_names = self.get_all_product_names()
        if not product_names:
            return "Nenhum produto encontrado no estoque."
        
        context = "Produtos disponíveis no estoque:\n"
        for i, name in enumerate(product_names, 1):
            context += f"{i}. {name}\n"
        
        return context
    
    def generate_sql_query(self, user_question: str, product_context: str) -> str:
        """Usa a API da OpenAI para gerar uma query SQL baseada na pergunta do usuário"""
        
        system_prompt = f"""
Você é um assistente especializado em gerar queries SQL para consultas de estoque.

Estrutura da tabela 'products':
- id (varchar): identificador único
- user_idF (varchar): ID do usuário/mercado dono do produto
- barcode (varchar): código de barras
- name (varchar): nome do produto
- brand (varchar): marca
- unit (varchar): unidade de medida
- package_quantity (float8): quantidade por pacote
- minimum_stock (float8): estoque mínimo
- suggested_price (float8): preço sugerido
- current_quantity (float8): quantidade atual em estoque
- expiration_date (timestamp): data de validade
- created_at (timestamptz): data de criação
- updated_at (timestamptz): data de atualização

{product_context}

IMPORTANTE: Use APENAS sintaxe SQLite:
- Para busca case-insensitive use: UPPER(campo) LIKE UPPER('%valor%')
- NÃO use ILIKE (isso é PostgreSQL)
- Use LIKE com UPPER() para case-insensitive
- Para perguntas sobre quantidade, use o campo 'current_quantity'

Gere APENAS a query SQL, sem explicações adicionais.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=200,
                temperature=0.1
            )
            print(f"QUERY GERADA: {response.choices[0].message.content.strip()}")
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Erro ao gerar query SQL: {str(e)}")
    
    def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Executa a query SQL no banco de dados"""
        db = SessionLocal()
        try:
            result = db.execute(text(sql_query))
            columns = result.keys()
            rows = result.fetchall()
            
            # Converter resultado para lista de dicionários
            return [dict(zip(columns, row)) for row in rows]
        
        except Exception as e:
            raise Exception(f"Erro ao executar query: {str(e)}")
        finally:
            db.close()
    
    def format_response(self, user_question: str, query_results: List[Dict[str, Any]], product_context: str) -> str:
        """Usa a API da OpenAI para formatar a resposta em linguagem natural"""
        
        system_prompt = f"""
Você é um assistente de estoque que responde perguntas sobre produtos de forma clara e amigável.

{product_context}

Baseado nos resultados da consulta ao banco de dados, formate uma resposta em português brasileiro.
Seja específico com números e nomes de produtos.
Se não houver resultados, explique que o produto não foi encontrado ou não há estoque.
"""
        
        user_prompt = f"""
Pergunta do usuário: {user_question}

Resultados da consulta:
{json.dumps(query_results, indent=2, default=str)}

Formate uma resposta clara e útil para o usuário.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Erro ao formatar resposta: {str(e)}"
    
    def process_question(self, user_question: str) -> str:
        """Processa uma pergunta do usuário sobre estoque"""
        try:
            # 1. Buscar contexto dos produtos
            product_context = self.get_product_context()
            
            # 2. Gerar query SQL
            sql_query = self.generate_sql_query(user_question, product_context)
            print(f"Query gerada: {sql_query}")  # Para debug
            
            # 3. Executar query
            results = self.execute_query(sql_query)
            
            # 4. Formatar resposta
            response = self.format_response(user_question, results, product_context)
            
            return response
        
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"


def main():
    """Função principal para testar o agente"""
    agent = AIStockAgent()
    
    print("=== Agente de IA para Controle de Estoque ===")
    print("Digite suas perguntas sobre o estoque (ou 'sair' para encerrar):\n")
    
    while True:
        user_input = input("Você: ").strip()
        
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando o agente. Até logo!")
            break
        
        if not user_input:
            continue
        
        print("\nProcessando...")
        response = agent.process_question(user_input)
        print(f"\nAgente: {response}\n")
        print("-" * 50)


if __name__ == "__main__":
    main()