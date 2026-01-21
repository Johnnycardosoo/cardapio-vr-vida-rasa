import streamlit as st
import sqlite3
import os
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="VR - Cardápio Digital", 
    page_icon="🥃", 
    layout="centered",
    initial_sidebar_state="collapsed" # Começa com o menu de gestão oculto
)

def conectar_db():
    return sqlite3.connect('cardapio_vr.db', check_same_thread=False)

# --- 2. INICIALIZAÇÃO DO SISTEMA ---
def inicializar_sistema():
    if not os.path.exists("img"):
        os.makedirs("img")
    conn = conectar_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS produtos 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     categoria TEXT, nome TEXT, preco REAL, ml TEXT, img_path TEXT)''')
    conn.commit()
    conn.close()

inicializar_sistema()

# --- 3. FUNÇÕES DE SUPORTE (IMAGENS) ---
def carregar_imagem_local(caminho):
    if caminho and os.path.exists(caminho):
        with open(caminho, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def get_base64_bin(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

# Aplicar fundo do bar se existir
fundo_b64 = get_base64_bin('fundo_bar.png')
if fundo_b64:
    st.markdown(f'''<style>.stApp {{ background-image: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("data:image/png;base64,{fundo_b64}"); background-size: cover; background-position: center; background-attachment: fixed; }} </style>''', unsafe_allow_html=True)

# --- 4. BARRA LATERAL (PAINEL DE GESTÃO VR) ---
with st.sidebar:
    st.title("⚙️ Gestão VR")
    senha = st.text_input("Senha Admin", type="password")
    if senha == "vr2026":
        st.success("Acesso Liberado")
        aba = st.radio("Ação:", ["Novo Produto", "Editar Produto", "Excluir"])
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
                desc = st.text_input("ML / Descrição")
                arquivo = st.file_uploader("Foto", type=['png', 'jpg', 'jpeg'])
                
                if st.form_submit_button("✅ SALVAR"):
                    if cat_final and nome and arquivo:
                        caminho_img = os.path.join("img", arquivo.name)
                        with open(caminho_img, "wb") as f:
                            f.write(arquivo.getbuffer())
                        cursor.execute("INSERT INTO produtos (categoria, nome, preco, ml, img_path) VALUES (?,?,?,?,?)", (cat_final, nome, prec, desc, caminho_img))
                        db.commit()
                        st.rerun()

        elif aba == "Editar Produto":
            st.subheader("📝 Editar Item")
            cursor.execute("SELECT id, nome, preco, ml, img_path, categoria FROM produtos")
            todos = cursor.fetchall()
            if todos:
                item_selecionado = st.selectbox("Selecione o produto", todos, format_func=lambda x: f"[{x[5]}] {x[1]}")
                with st.form("form_editar"):
                    novo_nome = st.text_input("Nome", value=item_selecionado[1])
                    novo_prec = st.number_input("Preço", value=float(item_selecionado[2]))
                    novo_desc = st.text_input("ML", value=item_selecionado[3])
                    nova_foto = st.file_uploader("Trocar Foto (opcional)", type=['png', 'jpg', 'jpeg'])
                    if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                        caminho_f = os.path.join("img", nova_foto.name) if nova_foto else item_selecionado[4]
                        if nova_foto:
                            with open(caminho_f, "wb") as f: f.write(nova_foto.getbuffer())
                        cursor.execute("UPDATE produtos SET nome=?, preco=?, ml=?, img_path=? WHERE id=?", (novo_nome, novo_prec, novo_desc, caminho_f, item_selecionado[0]))
                        db.commit()
                        st.rerun()

        elif aba == "Excluir":
            st.subheader("🗑️ Remover do Cardápio")
            tipo_ex = st.selectbox("O que deseja excluir?", ["Um Produto", "Uma Categoria Inteira"])
            if tipo_ex == "Um Produto":
                cursor.execute("SELECT id, nome, categoria FROM produtos ORDER BY categoria")
                lista_p = cursor.fetchall()
                if lista_p:
                    it = st.selectbox("Escolha o item", lista_p, format_func=lambda x: f"[{x[2]}] {x[1]}")
                    if st.button("❌ EXCLUIR ITEM"):
                        cursor.execute("DELETE FROM produtos WHERE id = ?", (it[0],))
                        db.commit()
                        st.rerun()
            else:
                if categorias_existentes:
                    cat_ex = st.selectbox("Escolha a categoria", categorias_existentes)
                    if st.button("🔥 EXCLUIR CATEGORIA"):
                        cursor.execute("DELETE FROM produtos WHERE categoria = ?", (cat_ex,))
                        db.commit()
                        st.rerun()
        db.close()

# --- 5. CABEÇALHO PÚBLICO (LOGO + INFOS) ---
if os.path.exists("vr_logo.png"):
    logo_b64 = get_base64_bin("vr_logo.png")
    st.markdown(f'''
        <div style="text-align:center;">
            <img src="data:image/png;base64,{logo_b64}" width="200">
            <p style="color:white; letter-spacing:5px; font-weight:200; margin-top:10px; margin-bottom:5px;">CARDÁPIO DIGITAL</p>
            <p style="color:#888; font-size:0.85rem; margin-bottom:5px; line-height:1.4;">
                📍 Av. Vaticano, N° 4 - Anjo da Guarda<br>São Luís - MA, 65071-383
            </p>
            <div style="display:inline-block; border:1px solid #FF4B4B; color:#FF4B4B; padding:2px 12px; border-radius:5px; font-size:0.7rem; font-weight:bold; margin-top:5px;">
                🔞 PROIBIDO PARA MENORES DE 18 ANOS
            </div>
        </div>
    ''', unsafe_allow_html=True)

# --- 6. EXIBIÇÃO DOS PRODUTOS ---
db = conectar_db()
cursor = db.cursor()
cursor.execute("SELECT DISTINCT categoria FROM produtos ORDER BY categoria")
categorias = [row[0] for row in cursor.fetchall()]

for cat in categorias:
    st.markdown(f"<div style='color:white; text-transform:uppercase; letter-spacing:4px; font-weight:900; margin-top:35px; border-bottom: 2px solid #FF4B4B; padding-bottom:5px; margin-bottom:15px;'>{cat}</div>", unsafe_allow_html=True)
    cursor.execute("SELECT nome, preco, ml, img_path FROM produtos WHERE categoria = ?", (cat,))
    for p in cursor.fetchall():
        img_b64 = carregar_imagem_local(p[3])
        # Container da imagem com 'object-fit: contain' para nunca cortar o produto
        if img_b64:
            img_html = f'''<div style="width:60px; height:60px; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.03); border-radius:8px; overflow:hidden;"><img src="data:image/png;base64,{img_b64}" style="max-width:100%; max-height:100%; object-fit: contain;"></div>'''
        else:
            img_html = '<div style="width:60px; height:60px; background:rgba(255,255,255,0.1); border-radius:8px; display:flex; align-items:center; justify-content:center;">🥃</div>'
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; gap: 15px;">
            <div style="min-width: 60px;">{img_html}</div>
            <div style="flex-grow: 1;"><span style="color:white; font-weight:bold; font-size:1.1rem;">{p[0]}</span><br><span style="color:#888; font-size:0.8rem;">{p[2]}</span></div>
            <div style="color:#FF4B4B; font-weight:900; font-size:1.1rem; background:rgba(255,75,75,0.1); padding:8px; border-radius:8px; white-space: nowrap;">R$ {p[1]:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
db.close()

# --- RODAPÉ ---
st.markdown("<br><br><div style='text-align:center; color:#555; font-size:0.8rem;'>VR - VIDA RASA © 2026<br>Desenvolvido por Johnny Cardoso</div>", unsafe_allow_html=True)
