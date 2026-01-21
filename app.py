import streamlit as st
import sqlite3
import os
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="VR - Cardápio Digital", 
    page_icon="🥃", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Conexão otimizada
def conectar_db():
    conn = sqlite3.connect('cardapio_vr.db', check_same_thread=False, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

# --- 2. INICIALIZAÇÃO ---
def inicializar_sistema():
    if not os.path.exists("img"):
        os.makedirs("img")
    conn = conectar_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS produtos 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     categoria TEXT, nome TEXT, preco REAL, ml TEXT, img_path TEXT,
                     disponivel INTEGER DEFAULT 1)''')
    conn.commit()
    conn.close()

inicializar_sistema()

# --- 3. FUNÇÕES DE SUPORTE ---
@st.cache_data
def carregar_imagem_base64(caminho):
    if not caminho:
        return None
    nome_arquivo = os.path.basename(caminho)
    caminho_real = os.path.join("img", nome_arquivo)
    
    if os.path.exists(caminho_real):
        with open(caminho_real, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            return f"data:image/png;base64,{encoded}"
    return None

# --- 4. BARRA LATERAL (GESTÃO VR) ---
with st.sidebar:
    st.title("⚙️ Gestão VR")
    senha = st.text_input("Senha Admin", type="password")
    
    if senha == "@Hagatavr25#":
        st.success("Acesso Liberado")
        
        if st.button("🔧 Corrigir Caminhos de Fotos"):
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("SELECT id, nome FROM produtos")
            itens = cursor.fetchall()
            for item_id, nome_prod in itens:
                if "red bull" in nome_prod.lower():
                    cursor.execute("UPDATE produtos SET img_path = 'img/redbull250ml.png' WHERE id = ?", (item_id,))
                elif "baly" in nome_prod.lower():
                    cursor.execute("UPDATE produtos SET img_path = 'img/baly1L.png' WHERE id = ?", (item_id,))
            db.commit()
            db.close()
            st.cache_data.clear()
            st.success("Caminhos corrigidos!")
            st.rerun()
        
        st.divider()
        aba = st.radio("Ação:", ["Novo Produto", "Editar / Ocultar", "Excluir"])
        db = conectar_db()
        cursor = db.cursor()
        
        if aba == "Novo Produto":
            st.subheader("📦 Novo Item")
            with st.form("form_novo", clear_on_submit=True):
                cat = st.text_input("Categoria").upper()
                nome = st.text_input("Nome do Produto")
                prec = st.number_input("Preço", min_value=0.0)
                desc = st.text_input("Descrição / Sabor (Ex: Morango)")
                arquivo = st.file_uploader("Foto", type=['png', 'jpg', 'jpeg'])
                if st.form_submit_button("✅ SALVAR"):
                    if cat and nome and arquivo:
                        caminho_img = os.path.join("img", arquivo.name)
                        with open(caminho_img, "wb") as f: f.write(arquivo.getbuffer())
                        cursor.execute("INSERT INTO produtos (categoria, nome, preco, ml, img_path, disponivel) VALUES (?,?,?,?,?,1)", 
                                     (cat, nome, prec, desc, caminho_img))
                        db.commit()
                        st.rerun()
        db.close()

# --- 5. CORPO DO CARDÁPIO (ELEMENTOS VISUAIS RESTAURADOS) ---

# 1. Fundo de Tela
fundo_data = carregar_imagem_base64('fundo_bar.png')
if fundo_data:
    st.markdown(f'''<style>.stApp {{ background-image: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("{fundo_data}"); background-size: cover; background-position: center; background-attachment: fixed; }} </style>''', unsafe_allow_html=True)

# 2. Logo, Endereço e Aviso
logo_data = carregar_imagem_base64("vr_logo.png")
if logo_data:
    st.markdown(f'''
        <div style="text-align:center;">
            <img src="{logo_data}" width="180">
            <p style="color:white; letter-spacing:5px; font-weight:200; margin-top:10px; margin-bottom:5px;">CARDÁPIO DIGITAL</p>
            <p style="color:#888; font-size:0.85rem; margin-bottom:5px; line-height:1.4;">
                📍 Av. Vaticano, N° 4 - Anjo da Guarda<br>São Luís - MA, 65071-383
            </p>
            <div style="display:inline-block; border:1px solid #FF4B4B; color:#FF4B4B; padding:2px 12px; border-radius:5px; font-size:0.7rem; font-weight:bold; margin-top:5px;">
                🔞 PROIBIDO PARA MENORES DE 18 ANOS
            </div>
        </div>
    ''', unsafe_allow_html=True)

# Listagem de Produtos
db = conectar_db()
cursor = db.cursor()
cursor.execute("SELECT categoria, nome, preco, ml, img_path FROM produtos WHERE disponivel = 1 ORDER BY categoria, nome")
produtos = cursor.fetchall()

menu = {}
for p in produtos:
    menu.setdefault(p[0], []).append(p)

for cat, itens in menu.items():
    st.markdown(f"<div style='color:white; text-transform:uppercase; letter-spacing:4px; font-weight:900; margin-top:30px; border-bottom: 2px solid #FF4B4B; padding-bottom:5px; margin-bottom:15px;'>{cat}</div>", unsafe_allow_html=True)
    
    for p in itens:
        img_b64 = carregar_imagem_base64(p[4])
        img_tag = f'<img src="{img_b64}" style="width:100%; height:100%; object-fit:contain;">' if img_b64 else '🥃'
        preco = f"R$ {p[2]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        linha_desc = f'<div style="color:#888; font-size:0.8rem; margin-top:2px;">{p[3]}</div>' if p[3] else ""

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:12px; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between; gap:12px; border: 1px solid rgba(255,255,255,0.03);">
            <div style="width:52px; height:52px; flex-shrink:0; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.03); border-radius:8px; overflow:hidden;">
                {img_tag}
            </div>
            <div style="flex-grow:1; min-width:0;">
                <div style="color:white; font-weight:bold; font-size:0.95rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{p[1]}</div>
                {linha_desc}
            </div>
            <div style="color:#FF4B4B; font-weight:900; font-size:1rem; background:rgba(255,75,75,0.1); padding:8px 10px; border-radius:8px; white-space:nowrap;">
                {preco}
            </div>
        </div>
        """, unsafe_allow_html=True)
db.close()

# 3. Rodapé Completo
st.divider()
st.markdown(f"""
    <div style='text-align: center; padding-bottom: 40px; padding-top: 10px;'>
        <p style='color: #FF4B4B; font-weight: bold; font-size: 1rem; margin-bottom: 10px;'>cardapiovr.com.br</p>
        <p style='color: #888; font-size: 0.85rem; line-height: 1.6;'>
            Copyright © 2026 <b>VR - VIDA RASA</b><br>
            Todos os direitos reservados.<br>
            <span style='font-size: 0.75rem; color: #555;'>Desenvolvido por <b>Johnny Cardoso</b></span>
        </p>
    </div>
    """, unsafe_allow_html=True)
