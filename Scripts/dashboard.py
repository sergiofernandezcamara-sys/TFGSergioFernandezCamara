from pathlib import Path
import shutil
import tkinter as tk
from tkinter import ttk
import pandas as pd

ADAPT_FILE = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv_adapt")
DASH_FILE = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv_dash")

ADAPT_FILE.mkdir(parents=True, exist_ok=True)
DASH_FILE.mkdir(parents=True, exist_ok=True)

MIN_ATTACK_FLOWS = 10
MIN_ATTACK_RATIO = 0.20

MAX_FLOWS = 10000

flows_memory = []
captures_memory = []

def process_new_csv_files():
    new_files = sorted(ADAPT_FILE.glob("*.csv"))

    if not new_files:
        return

    csv_file=new_files[0]

    df = pd.read_csv(csv_file)

    total_flows = len(df)
    attack_flows = int((df["Prediction"] == "ATTACK").sum())
    benign_flows = total_flows - attack_flows
    attack_ratio = attack_flows / total_flows if total_flows > 0 else 0

    is_attack = (
        attack_flows >= MIN_ATTACK_FLOWS
        and attack_ratio >= MIN_ATTACK_RATIO
    )

    capture_summary = {
        "capture_id": csv_file.name,
        "total_flows": total_flows,
        "attack_flows": attack_flows,
        "benign_flows": benign_flows,
        "attack_ratio": attack_ratio,
        "is_attack": is_attack
    }

    captures_memory.append(capture_summary)

    flows = df.to_dict(orient="records")

    for flow in flows:
        flow["capture_id"] = csv_file.name

    flows_memory.extend(flows)
    flows_memory[:] = flows_memory[-MAX_FLOWS:]

    processed_file = DASH_FILE / csv_file.name
    shutil.move(str(csv_file), str(processed_file))

def update_status():
    attack=0
    for capture in captures_memory:
        if capture["is_attack"]:
            attack=1

        if attack==1:
            status_label.config(
                text="Ataque detectado",
                bg="red",
                fg="white"
            )
        else:
            status_label.config(
                text="Sin ataque detectado",
                bg="green",
                fg="white"
            )

        total_captures = len(captures_memory)
        attack_captures = sum(1 for capture in captures_memory if capture["is_attack"])
    
        stats_label.config(
            text=(
                f"Captura: {capture['capture_id']} | "
                f"Flujos: {capture['total_flows']} | "
                f"Ataques: {capture['attack_flows']} | "
                f"Ratio: {capture['attack_ratio']:.2%} \n | "
                f"Capturas analizadas: {total_captures} | "
                f"Capturas con ataque: {attack_captures} |"
            )
        )

def update_table():
    for row in tree.get_children():
        tree.delete(row)

    for flow in flows_memory:
        probability = flow.get("Probability", "")

        if isinstance(probability, float):
            probability = f"{probability:.4f}"

        tree.insert(
            "",
            "end",
            values=(
                flow.get("Src IP", ""),
                flow.get("Src Port", ""),
                flow.get("Dst IP", ""),
                flow.get("Dst Port", ""),
                flow.get("Protocol", ""),
                probability,
                flow.get("Prediction", "")
            )
        )

def show_page(page):
    page.tkraise()

def refresh_dashboard():
    process_new_csv_files()
    update_status()
    update_table()

    root.after(2000, refresh_dashboard)

root = tk.Tk()
root.title("Dashboard IDS")
root.geometry("1200x700")
root.configure(bg="#f3f4f6")

###########################
#Barra superior
###########################

top_bar = tk.Frame(root, bg="#111827", height=90)
top_bar.pack(fill="x")
top_bar.pack_propagate(False)

buttons_frame = tk.Frame(top_bar, bg="#111827")
buttons_frame.pack(expand=True)

btn_flows = tk.Button(
    buttons_frame,
    text="Flujos",
    font=("Arial", 16, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    padx=45,
    pady=14,
    command=lambda: show_page(flows_page)
)
btn_flows.pack(side="left", padx=20)

btn_status = tk.Button(
    buttons_frame,
    text="Estado IDS",
    font=("Arial", 16, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    padx=45,
    pady=14,
    command=lambda: show_page(status_page)
)
btn_status.pack(side="left", padx=20)

###########################
#Contenedor de páginas
###########################

pages_container = tk.Frame(root, bg="#f3f4f6")
pages_container.pack(fill="both", expand=True)

flows_page = tk.Frame(pages_container, bg="#f3f4f6")
status_page = tk.Frame(pages_container, bg="#f3f4f6")

for page in (flows_page, status_page):
    page.place(relx=0, rely=0, relwidth=1, relheight=1)

###########################
#Página 1: tabla de flujos
###########################

flows_title = tk.Label(
    flows_page,
    text="Flujos detectados",
    font=("Arial", 20, "bold"),
    bg="#f3f4f6",
    fg="#111827"
)
flows_title.pack(anchor="w", padx=20, pady=(20, 10))

table_frame = tk.Frame(flows_page, bg="white")
table_frame.pack(fill="both", expand=True, padx=20, pady=20)

columns = (
    "src_ip",
    "src_port",
    "dst_ip",
    "dst_port",
    "protocol",
    "probability",
    "prediction"
)

tree = ttk.Treeview(table_frame, columns=columns, show="headings")

tree.heading("src_ip", text="IP origen")
tree.heading("src_port", text="Puerto origen")
tree.heading("dst_ip", text="IP destino")
tree.heading("dst_port", text="Puerto destino")
tree.heading("protocol", text="Protocolo")
tree.heading("probability", text="Probabilidad")
tree.heading("prediction", text="Predicción")

tree.column("src_ip", width=150)
tree.column("src_port", width=100)
tree.column("dst_ip", width=150)
tree.column("dst_port", width=100)
tree.column("protocol", width=100)
tree.column("probability", width=130)
tree.column("prediction", width=130)

scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_y.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar_y.pack(side="right", fill="y")

###########################
#Página 2: estado IDS
###########################

status_title = tk.Label(
    status_page,
    text="Estado del sistema IDS",
    font=("Arial", 24, "bold"),
    bg="#f3f4f6",
    fg="#111827"
)
status_title.pack(pady=(40, 20))

status_card = tk.Frame(
    status_page,
    bg="white",
    padx=30,
    pady=30
)
status_card.pack(padx=40, pady=20, fill="x")

status_label = tk.Label(
    status_card,
    text="Esperando capturas...",
    font=("Arial", 24, "bold"),
    bg="#6b7280",
    fg="white",
    padx=30,
    pady=30
)
status_label.pack(fill="x", pady=(0, 30))

stats_label = tk.Label(
    status_card,
    text="Capturas aún no analizadas",
    font=("Arial", 15),
    bg="white",
    fg="#111827",
    justify="left"
)
stats_label.pack(anchor="w")

show_page(flows_page)

refresh_dashboard()

root.mainloop()