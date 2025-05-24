import json
import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread

class MedicalChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.bot = MedicalChatbot()
        self.setup_ui()
        self.start_conversation()

    def setup_ui(self):
        self.master.title("Assistente Médico Inteligente")
        self.master.geometry("800x600")
        
        # Área de conversa
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled')
        self.chat_area.configure(font=('Arial', 12), bg='#f0f0f0')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame de entrada
        input_frame = tk.Frame(self.master)
        input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.user_input = tk.Entry(input_frame, font=('Arial', 14))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", lambda event: self.process_input())
        
        send_btn = tk.Button(input_frame, text="Enviar", command=self.process_input, 
                           bg='#4CAF50', fg='white', font=('Arial', 12))
        send_btn.pack(side=tk.RIGHT, padx=5)

    def start_conversation(self):
        self.add_bot_message("Bem-vindo ao Assistente Médico Virtual. Por favor, descreva seus sintomas iniciais.")

    def add_bot_message(self, text):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"Assistente: {text}\n\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def add_user_message(self, text):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"Você: {text}\n\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def process_input(self):
        user_text = self.user_input.get()
        if not user_text:
            return
        
        self.add_user_message(user_text)
        self.user_input.delete(0, tk.END)
        
        Thread(target=self.analyze_input, args=(user_text,)).start()

    def analyze_input(self, text):
        if self.bot.waiting_for_decision:
            response = self.bot.handle_emergency_decision(text)
            self.add_bot_message(response)
            return

        symptoms = self.bot.process_input(text)
        
        if symptoms:
            self.add_bot_message("Entendi. Analisando seus sintomas...")
            self.bot.diagnose()
            
            if self.bot.current_diagnoses:
                self.show_diagnosis()
            else:
                self.ask_followup_questions()
        else:
            self.add_bot_message("Não entendi completamente. Poderia descrever melhor seus sintomas?")

    def ask_followup_questions(self):
        next_question = self.bot.get_next_question()
        if next_question:
            self.add_bot_message(next_question)
        else:
            self.show_final_diagnosis()

    def show_diagnosis(self):
        diagnosis = self.bot.current_diagnoses[0]
        explanation = diagnosis['explicacao']
        treatment = self.bot.get_treatment_recommendation()
        
        self.add_bot_message(f"** Diagnóstico Preliminar **\n"
                           f"Condição: {diagnosis['condition'].capitalize()}\n"
                           f"Explicação: {explanation}\n"
                           f"Recomendação: {treatment}")
        
        if diagnosis['emergency']:
            self.handle_emergency_alert(diagnosis['condition'])

    def handle_emergency_alert(self, condition):
        self.add_bot_message(f"⚠️ ATENÇÃO: {condition.upper()} POTENCIALMENTE GRAVE!")
        self.add_bot_message("Deseja que eu contate ajuda médica emergencial? (sim/não)")
        self.bot.waiting_for_decision = True

    def show_final_diagnosis(self):
        self.add_bot_message("Análise completa. Resultados:")
        for idx, diagnosis in enumerate(self.bot.current_diagnoses, 1):
            self.add_bot_message(f"{idx}. {diagnosis['condition'].capitalize()} "
                               f"(Confiança: {diagnosis['confidence']}%)\n"
                               f"   Explicação: {diagnosis['explicacao']}")
        
        self.add_bot_message("Recomendações finais:\n" + self.bot.get_treatment_recommendation())

class MedicalChatbot:
    def __init__(self):
        with open("knowledge_base.json") as f:
            self.knowledge = json.load(f)
        
        self.stop_words = set([
            'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 
            'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais',
            'as', 'dos', 'como', 'mas', 'ao', 'ele', 'das', 'à', 'seu', 'sua',
            'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo',
            'ser', 'até', 'mesmo', 'está', 'você', 'tem', 'ter', 'meu', 'esse'
        ])
        
        self.symptoms = []
        self.history = {}
        self.current_diagnoses = []
        self.waiting_for_decision = False
        self.emergency_contact = False

    def process_input(self, text):
        # Processamento simplificado de texto
        tokens = [
            word.lower().strip('.,!?;:') 
            for word in text.split() 
            if word.lower() not in self.stop_words
        ]
        self.symptoms.extend(tokens)
        return tokens

    def diagnose(self):
        self.current_diagnoses = []
        for condition, data in self.knowledge.items():
            matched = set(self.symptoms) & set(data['sintomas'])
            if len(matched) >= data['sintomas_necessarios']:
                confidence = min(100, int((len(matched) / data['sintomas_necessarios']) * 50))
                self.current_diagnoses.append({
                    'condition': condition,
                    'confidence': confidence,
                    'explicacao': f"Correspondência com {len(matched)} sintomas-chave: {', '.join(matched)}",
                    'emergency': data['emergencia']
                })
        
        self.current_diagnoses.sort(key=lambda x: x['confidence'], reverse=True)

    def get_next_question(self):
        followups = {
            'dor': ['náusea', 'tontura', 'fotofobia'],
            'febre': ['calafrios', 'suor', 'duração'],
            'tosse': ['catarro', 'sangue', 'duração']
        }
        
        for symptom in self.symptoms:
            if symptom in followups:
                return f"Você está sentindo {followups[symptom][0]}?"
        return None

    def get_treatment_recommendation(self):
        if not self.current_diagnoses:
            return "Repouso e observe a evolução. Procure um médico se os sintomas persistirem."
        
        treatments = {
            "enxaqueca": "Repouso em ambiente escuro, paracetamol (500mg)\nConsulte um neurologista",
            "angina": "Procure emergência cardiológica imediatamente",
            "gripe": "Hidratação, repouso e medicamentos sintomáticos",
            "apendicite": "Encaminhamento cirúrgico urgente - procure um hospital"
        }
        
        main_condition = self.current_diagnoses[0]['condition']
        return treatments.get(main_condition, "Consulta médica recomendada")

    def handle_emergency_decision(self, response):
        self.waiting_for_decision = False
        if 'sim' in response.lower():
            self.emergency_contact = True
            return "Ajuda emergencial será contatada. Mantenha-se calmo e em posição segura."
        return "Continue monitorando os sintomas. Procure ajuda imediatamente se piorar."


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalChatbotGUI(root)
    root.mainloop()