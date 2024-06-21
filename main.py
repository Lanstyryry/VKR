import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
import re

class GraphBuilderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Приложение для построения графов")

        # Создаем вкладки
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Ввод текста')
        self.tabControl.add(self.tab2, text='Шаблоны')
        self.tabControl.add(self.tab3, text='Настройка генерации')
        self.tabControl.add(self.tab4, text='Генерация')
        self.tabControl.pack(expand=1, fill='both')

        # Вкладка 1: ввод текста
        self.create_text_input_tab()

        # Вкладка 2: шаблоны
        self.create_templates_tab()

        # Вкладка 3: настройка генерации
        self.create_generation_settings_tab()

        # Вкладка 4: генерация (пока заглушка)
        self.create_generation_result_tab()

    def create_text_input_tab(self):
        label_text = ttk.Label(self.tab1, text="Введите текст:")
        label_text.grid(row=0, column=0, padx=10, pady=10)

        self.text_entry = tk.Text(self.tab1, width=50, height=10)
        self.text_entry.grid(row=1, column=0, padx=10, pady=10)

        def view_templates():
            self.tabControl.select(self.tab2)

        def next_tab():
            self.tabControl.select(self.tab3)

        view_templates_btn = ttk.Button(self.tab1, text="Просмотр шаблонов", command=view_templates)
        view_templates_btn.grid(row=2, column=0, padx=10, pady=10)

        next_tab_btn = ttk.Button(self.tab1, text="Далее", command=next_tab)
        next_tab_btn.grid(row=2, column=1, padx=10, pady=10)

    def create_templates_tab(self):
        label_template1 = ttk.Label(self.tab2, text="Текст шаблона 1:")
        label_template1.grid(row=0, column=0, padx=10, pady=10)

        self.template1_entry = ttk.Entry(self.tab2, width=50)
        self.template1_entry.insert(0, "Система управления поставками: система получает спецификации товаров от поставщика, передаёт заказы закупки поставщику, создаёт отчёты о получении для бухгалтерии.")
        self.template1_entry.grid(row=0, column=1, padx=10, pady=10)

        label_template2 = ttk.Label(self.tab2, text="Текст шаблона 2:")
        label_template2.grid(row=1, column=0, padx=10, pady=10)

        self.template2_entry = ttk.Entry(self.tab2, width=50)
        self.template2_entry.insert(0, "Система управления заказами: система получает заказы от клиентов, передаёт запросы на выполнение заказов в производство, создаёт отчёты о выполнении для отдела логистики.")
        self.template2_entry.grid(row=1, column=1, padx=10, pady=10)

        def back_to_input():
            self.tabControl.select(self.tab1)

        def insert_template1():
            self.text_entry.insert(tk.END, self.template1_entry.get())

        def insert_template2():
            self.text_entry.insert(tk.END, self.template2_entry.get())

        back_btn = ttk.Button(self.tab2, text="Назад", command=back_to_input)
        back_btn.grid(row=2, column=0, padx=10, pady=10)

        insert_template1_btn = ttk.Button(self.tab2, text="Вставить шаблон 1", command=insert_template1)
        insert_template1_btn.grid(row=2, column=1, padx=10, pady=10)

        insert_template2_btn = ttk.Button(self.tab2, text="Вставить шаблон 2", command=insert_template2)
        insert_template2_btn.grid(row=2, column=2, padx=10, pady=10)

    def create_generation_settings_tab(self):
        label_num_entities = ttk.Label(self.tab3, text="Количество сущностей:")
        label_num_entities.grid(row=0, column=0, padx=10, pady=10)

        self.num_entities_entry = ttk.Entry(self.tab3)
        self.num_entities_entry.grid(row=0, column=1, padx=10, pady=10)

        label_width = ttk.Label(self.tab3, text="Ширина холста:")
        label_width.grid(row=1, column=0, padx=10, pady=10)

        self.width_entry = ttk.Entry(self.tab3)
        self.width_entry.grid(row=1, column=1, padx=10, pady=10)

        label_height = ttk.Label(self.tab3, text="Высота холста:")
        label_height.grid(row=2, column=0, padx=10, pady=10)

        self.height_entry = ttk.Entry(self.tab3)
        self.height_entry.grid(row=2, column=1, padx=10, pady=10)

        def next_tab():
            self.tabControl.select(self.tab4)

        next_tab_btn = ttk.Button(self.tab3, text="Сгенерировать", command=next_tab)
        next_tab_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_generation_result_tab(self):
        def show_diagram():
            text_description = self.text_entry.get("1.0", tk.END)
            self.generate_dfd(text_description)

        def repeat_generation():
            self.tabControl.select(self.tab3)

        show_diagram_btn = ttk.Button(self.tab4, text="Отобразить диаграмму", command=show_diagram)
        show_diagram_btn.pack(padx=20, pady=20)

        repeat_generation_btn = ttk.Button(self.tab4, text="Повторная генерация", command=repeat_generation)
        repeat_generation_btn.pack(padx=20, pady=20)

    def generate_graph_result(self, num_entities, width, height, text_description):
        # Пример генерации графа
        G = nx.DiGraph()
        nodes = ['Entity ' + str(i) for i in range(1, num_entities + 1)]
        edges = [(nodes[i], nodes[i+1]) for i in range(num_entities - 1)]
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        plt.figure(figsize=(width / 10, height / 10))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
        plt.title('Граф сгенерированного потока данных')
        plt.show()

    def generate_dfd(self, text_description):
        # Очищаем старый граф, если он был нарисован
        plt.clf()

        # Словарь для хранения сущностей и их связей
        entities = {}
        links = []

        # Разделяем текст на предложения
        sentences = re.split(r'[,.]', text_description)
        prev_entity = None

        for sentence in sentences:
            words = sentence.split()
            if not words:
                continue

            # Ищем глагол
            verb_index = -1
            for i, word in enumerate(words):
                if word.endswith(('ет', 'ит', 'ет', 'ит', 'ат', 'ут', 'ют', 'ешь', 'ит', 'ите', 'им', 'ите')):
                    verb_index = i
                    break

            if verb_index == -1:
                continue

            entity1 = ' '.join(words[:verb_index])
            if prev_entity:
                entity1 = prev_entity
            else:
                prev_entity = entity1

            # Ищем предлог
            preposition_index = -1
            for i, word in enumerate(words[verb_index:], start=verb_index):
                if word in ['от', 'для', 'по', 'с', 'к', 'на']:
                    preposition_index = i
                    break

            if preposition_index == -1:
                continue

            # Связь
            link = ' '.join(words[verb_index:preposition_index])

            # Ищем следующую сущность
            entity2 = ' '.join(words[preposition_index+1:])

            if entity2:
                entities[entity1] = entity1
                entities[entity2] = entity2
                links.append((entity1, entity2, link))
                prev_entity = entity2

        # Создаем граф
        G = nx.DiGraph()

        # Добавляем сущности и связи
        for entity in entities.values():
            G.add_node(entity)

        for link in links:
            G.add_edge(link[0], link[1], label=link[2])

        # Размеры и позиция для отображения графа
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_shape='s', node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)

        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title('DFD Диаграмма')
        plt.show()

if __name__ == "__main__":
    app = GraphBuilderApp()
    app.mainloop()
