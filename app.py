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
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    nome_arquivo = os.path.basename(caminho)
    caminho_real = os.path.join(diretorio_atual, "img", nome_arquivo)
    
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
        aba = st.radio("Ação:", ["Novo Produto", "Editar / Ocultar", "Excluir"])
        db = conectar_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT DISTINCT categoria FROM produtos ORDER BY categoria")
        categorias_existentes = [row[0] for row in cursor.fetchall()]

        if aba == "Novo Produto":
            st.subheader("📦 Novo Item")
            criar_nova = st.checkbox("➕ Cadastrar Nova Categoria?")
            cat_final = st.text_input("Nome da Categoria").upper() if criar_nova else st.selectbox("Categoria", categorias_existentes if categorias_existentes else ["CERVEJAS"])
            with st.form("form_novo", clear_on_submit=True):
                nome = st.text_input("Nome do Produto")
                prec = st.number_input("Preço", min_value=0.0)
                desc = st.text_input("Descrição / ML (Ex: sabor melancia)")
                arquivo = st.file_uploader("Foto", type=['png', 'jpg', 'jpeg'])
                if st.form_submit_button("✅ SALVAR"):
                    if cat_final and nome and arquivo:
                        caminho_img = os.path.join("img", arquivo.name)
                        with open(caminho_img, "wb") as f: f.write(arquivo.getbuffer())
                        cursor.execute("INSERT INTO produtos (categoria, nome, preco, ml, img_path, disponivel) VALUES (?,?,?,?,?,1)", (cat_final, nome, prec, desc, caminho_img))
                        db.commit()
                        st.cache_data.clear()
                        st.rerun()

        elif aba == "Editar / Ocultar":
            cursor.execute("SELECT id, nome, preco, ml, img_path, categoria, disponivel FROM produtos")
            todos_itens = cursor.fetchall()
            if todos_itens:
                it_sel = st.selectbox("Selecione o produto", todos_itens, format_func=lambda x: f"{'🟢' if x[6]==1 else '🔴'} [{x[5]}] {x[1]}")
                with st.form("form_editar"):
                    n_nome = st.text_input("Nome", value=it_sel[1])
                    n_prec = st.number_input("Preço", value=float(it_sel[2]))
                    n_desc = st.text_input("Descrição / ML", value=it_sel[3])
                    n_disp = st.checkbox("Disponível", value=True if it_sel[6] == 1 else False)
                    n_foto = st.file_uploader("Trocar Foto", type=['png', 'jpg', 'jpeg'])
                    if st.form_submit_button("💾 SALVAR"):
                        cam_f = os.path.join("img", n_foto.name) if n_foto else it_sel[4]
                        if n_foto:
                            with open(cam_f, "wb") as f: f.write(n_foto.getbuffer())
                        cursor.execute("UPDATE produtos SET nome=?, preco=?, ml=?, img_path=?, disponivel=? WHERE id=?", (n_nome, n_prec, n_desc, cam_f, 1 if n_disp else 0, it_sel[0]))
                        db.commit()
                        st.cache_data.clear()
                        st.rerun()
        db.close()

# --- 5. CORPO DO CARDÁPIO ---
fundo_data = carregar_imagem_base64('fundo_bar.png') or carregar_imagem_base64('img/fundo_bar.png')
if fundo_data:
    st.markdown(f'''<style>.stApp {{ background-image: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("{fundo_data}"); background-size: cover; background-position: center; background-attachment: fixed; }} </style>''', unsafe_allow_html=True)

logo_data = carregar_imagem_base64("vr_logo.png") or carregar_imagem_base64("img/vr_logo.png")
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
todos = cursor.fetchall()

menu = {}
for p in todos:
    menu.setdefault(p[0], []).append(p)

for cat, itens in menu.items():
    st.markdown(f"<div style='color:white; text-transform:uppercase; letter-spacing:4px; font-weight:900; margin-top:30px; border-bottom: 2px solid #FF4B4B; padding-bottom:5px; margin-bottom:15px;'>{cat}</div>", unsafe_allow_html=True)
    for p in itens:
        img_data = carregar_imagem_base64(p[4])
        img_html = f'<img src="{img_data}" style="width: 100%; height: 100%; object-fit: contain;">' if img_data else '🥃'
        preco_formatado = f"{p[2]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        nome_prod = p[1]
        desc_prod = p[3] if p[3] else ""

        # Lógica: Só exibe a linha de baixo se a descrição for algo diferente do que já está no nome
        html_desc = f'<div style="color:#888; font-size:0.8rem; margin-top:2px;">{desc_prod}</div>' if desc_prod and desc_prod.lower() not in nome_prod.lower() else ""

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; gap: 12px;">
            <div style="width: 52px; height: 52px; flex-shrink: 0; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.03); border-radius:8px; overflow:hidden;">
                {img_html}
            </div>
            <div style="flex-grow: 1; min-width: 0; overflow: hidden;">
                <div style="color:white; font-weight:bold; font-size:0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {nome_prod}
                </div>
                {html_desc}
            </div>
            <div style="color:#FF4B4B; font-weight:900; font-size:1rem; background:rgba(255,75,75,0.1); padding:8px 10px; border-radius:8px; white-space: nowrap; flex-shrink: 0; min-width: fit-content; text-align: center;">
                R$ {preco_formatado}
            </div>
        </div>
        """, unsafe_allow_html=True)
db.close()

# Rodapé
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
