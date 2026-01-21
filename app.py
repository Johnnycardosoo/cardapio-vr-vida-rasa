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

# Conexão
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
    if not caminho: return None
    nome_arquivo = os.path.basename(caminho)
    caminho_real = os.path.join("img", nome_arquivo)
    if os.path.exists(caminho_real):
        with open(caminho_real, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

# --- 4. BARRA LATERAL (GESTÃO VR) ---
with st.sidebar:
    st.title("⚙️ Gestão VR")
    senha = st.text_input("Senha Admin", type="password")
    
    if senha == "@Hagatavr25#":
        st.success("Acesso Liberado")
        
        # Funções de sistema
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔧 Corrigir Fotos"):
                db = conectar_db(); cursor = db.cursor()
                cursor.execute("SELECT id, nome FROM produtos")
                for i, n in cursor.fetchall():
                    if "red bull" in n.lower(): cursor.execute("UPDATE produtos SET img_path='img/redbull250ml.png' WHERE id=?", (i,))
                    elif "baly" in n.lower(): cursor.execute("UPDATE produtos SET img_path='img/baly1L.png' WHERE id=?", (i,))
                db.commit(); db.close(); st.cache_data.clear(); st.rerun()
        with col2:
            if os.path.exists("cardapio_vr.db"):
                with open("cardapio_vr.db", "rb") as f:
                    st.download_button("📥 Backup", f, "cardapio_vr.db")

        st.divider()
        aba = st.radio("Ação:", ["Novo Produto", "Editar Individual", "Excluir"])
        db = conectar_db(); cursor = db.cursor()
        
        cursor.execute("SELECT DISTINCT categoria FROM produtos ORDER BY categoria")
        categorias = [r[0] for r in cursor.fetchall()]

        if aba == "Novo Produto":
            with st.form("novo_prod", clear_on_submit=True):
                c_nova = st.checkbox("Nova Categoria?")
                cat = st.text_input("Categoria").upper() if c_nova else st.selectbox("Categoria", categorias if categorias else ["GERAL"])
                nome = st.text_input("Nome do Produto")
                prec = st.number_input("Preço", min_value=0.0)
                # CAMPO INDIVIDUAL ABAIXO
                desc_individual = st.text_input("Descrição ÚNICA deste produto (Ex: Sabor Morango)")
                arquivo = st.file_uploader("Foto", type=['png', 'jpg', 'jpeg'])
                if st.form_submit_button("✅ SALVAR"):
                    if cat and nome and arquivo:
                        path = os.path.join("img", arquivo.name)
                        with open(path, "wb") as f: f.write(arquivo.getbuffer())
                        cursor.execute("INSERT INTO produtos (categoria, nome, preco, ml, img_path) VALUES (?,?,?,?,?)", (cat, nome, prec, desc_individual, path))
                        db.commit(); st.cache_data.clear(); st.rerun()

        elif aba == "Editar Individual":
            cursor.execute("SELECT id, nome, preco, ml, img_path, categoria, disponivel FROM produtos")
            itens = cursor.fetchall()
            if itens:
                sel = st.selectbox("Selecione o Item", itens, format_func=lambda x: f"[{x[5]}] {x[1]} - {x[3]}")
                with st.form("edit_form"):
                    ed_nome = st.text_input("Nome", value=sel[1])
                    ed_prec = st.number_input("Preço", value=float(sel[2]))
                    ed_desc = st.text_input("Descrição Individual (Sabor/ML)", value=sel[3])
                    ed_disp = st.checkbox("Disponível", value=True if sel[6]==1 else False)
                    if st.form_submit_button("💾 ATUALIZAR ITEM"):
                        cursor.execute("UPDATE produtos SET nome=?, preco=?, ml=?, disponivel=? WHERE id=?", (ed_nome, ed_prec, ed_desc, 1 if ed_disp else 0, sel[0]))
                        db.commit(); st.cache_data.clear(); st.rerun()

        elif aba == "Excluir":
            cursor.execute("SELECT id, nome, ml FROM produtos")
            p_del = cursor.fetchall()
            if p_del:
                sel_del = st.selectbox("Apagar:", p_del, format_func=lambda x: f"{x[1]} ({x[2]})")
                if st.button("🚨 EXCLUIR"):
                    cursor.execute("DELETE FROM produtos WHERE id=?", (sel_del[0],))
                    db.commit(); st.cache_data.clear(); st.rerun()
        db.close()

# --- 5. CORPO DO CARDÁPIO (DESIGN VR) ---
fundo = carregar_imagem_base64('fundo_bar.png')
if fundo:
    st.markdown(f'<style>.stApp {{ background-image: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("{fundo}"); background-size: cover; background-position: center; background-attachment: fixed; }} </style>', unsafe_allow_html=True)

logo = carregar_imagem_base64("vr_logo.png")
if logo:
    st.markdown(f'<div style="text-align:center;"><img src="{logo}" width="160"><p style="color:white; letter-spacing:4px; font-weight:200; margin:10px 0 0 0;">CARDÁPIO DIGITAL</p><p style="color:#888; font-size:0.8rem;">📍 Av. Vaticano, N° 4 - Anjo da Guarda</p></div>', unsafe_allow_html=True)

db = conectar_db(); cursor = db.cursor()
cursor.execute("SELECT categoria, nome, preco, ml, img_path FROM produtos WHERE disponivel=1 ORDER BY categoria, nome")
prods = cursor.fetchall()

menu = {}
for p in prods: menu.setdefault(p[0], []).append(p)

for cat, itens in menu.items():
    st.markdown(f"<div style='color:white; font-weight:900; border-bottom:2px solid #FF4B4B; margin:25px 0 15px 0; padding-bottom:5px; text-transform:uppercase; letter-spacing:2px;'>{cat}</div>", unsafe_allow_html=True)
    for p in itens:
        img_b64 = carregar_imagem_base64(p[4])
        img_tag = f'<img src="{img_b64}" style="width:100%; height:100%; object-fit:contain;">' if img_b64 else '🥃'
        # EXIBIÇÃO DA DESCRIÇÃO INDIVIDUAL
        linha_desc = f'<div style="color:#888; font-size:0.85rem; font-weight:normal;">{p[3]}</div>' if p[3] else ""
        
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:12px; margin-bottom:8px; display:flex; align-items:center; gap:12px; border:1px solid rgba(255,255,255,0.03);">
            <div style="width:50px; height:50px; flex-shrink:0; background:rgba(255,255,255,0.02); border-radius:8px; display:flex; align-items:center; justify-content:center; overflow:hidden;">{img_tag}</div>
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:0.95rem;">{p[1]}</div>
                {linha_desc}
            </div>
            <div style="color:#FF4B4B; font-weight:900; font-size:1rem; background:rgba(255,75,75,0.1); padding:8px 10px; border-radius:8px;">R$ {p[2]:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
db.close()

st.divider()
st.markdown("<div style='text-align:center; color:#555; font-size:0.8rem; padding-bottom:30px;'>Desenvolvido por Johnny Cardoso © 2026</div>", unsafe_allow_html=True)
