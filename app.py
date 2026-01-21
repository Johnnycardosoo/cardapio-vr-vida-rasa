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
    # Adicionada a coluna 'disponivel' (1 = Visível, 0 = Oculto)
    conn.execute('''CREATE TABLE IF NOT EXISTS produtos 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     categoria TEXT, nome TEXT, preco REAL, ml TEXT, img_path TEXT,
                     disponivel INTEGER DEFAULT 1)''')
    
    # Tenta adicionar a coluna caso o banco já exista sem ela
    try:
        conn.execute("ALTER TABLE produtos ADD COLUMN disponivel INTEGER DEFAULT 1")
    except:
        pass
        
    conn.commit()
    conn.close()

inicializar_sistema()

# --- 3. FUNÇÕES DE SUPORTE (VERSÃO CORRIGIDA) ---
@st.cache_data
def carregar_imagem_base64(caminho):
    if caminho and os.path.exists(caminho):
        # Descobre a extensão real do arquivo (ex: jpg, png, jpeg)
        ext = caminho.split('.')[-1].lower()
        if ext == 'jpg': ext = 'jpeg'
        
        with open(caminho, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            # Já retorna a string montada com o tipo de imagem correto
            return f"data:image/{ext};base64,{encoded}"
    return None

# --- 4. BARRA LATERAL (GESTÃO VR) ---
with st.sidebar:
    st.title("⚙️ Gestão VR")
    senha = st.text_input("Senha Admin", type="password")
    
    if senha == "@Hagatavr25#":
        st.success("Acesso Liberado")
        
        if os.path.exists("cardapio_vr.db"):
            with open("cardapio_vr.db", "rb") as f:
                st.download_button(
                    label="📥 Baixar Banco de Dados (Backup)",
                    data=f,
                    file_name="cardapio_vr.db",
                    mime="application/octet-stream"
                )
        
        st.divider()
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
                desc = st.text_input("ML / Descrição")
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
            todos = cursor.fetchall()
            if todos:
                it_sel = st.selectbox("Selecione o produto", todos, format_func=lambda x: f"{'🟢' if x[6]==1 else '🔴'} [{x[5]}] {x[1]}")
                with st.form("form_editar"):
                    n_nome = st.text_input("Nome", value=it_sel[1])
                    n_prec = st.number_input("Preço", value=float(it_sel[2]))
                    n_desc = st.text_input("ML", value=it_sel[3])
                    # Opção de Ocultar/Mostrar
                    n_disp = st.checkbox("Produto Disponível (Mostrar no Cardápio)", value=True if it_sel[6] == 1 else False)
                    n_foto = st.file_uploader("Trocar Foto", type=['png', 'jpg', 'jpeg'])
                    
                    if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                        cam_f = os.path.join("img", n_foto.name) if n_foto else it_sel[4]
                        val_disp = 1 if n_disp else 0
                        if n_foto:
                            with open(cam_f, "wb") as f: f.write(n_foto.getbuffer())
                        cursor.execute("UPDATE produtos SET nome=?, preco=?, ml=?, img_path=?, disponivel=? WHERE id=?", (n_nome, n_prec, n_desc, cam_f, val_disp, it_sel[0]))
                        db.commit()
                        st.cache_data.clear()
                        st.rerun()

        elif aba == "Excluir":
            t_ex = st.selectbox("O que deseja excluir?", ["Um Produto", "Uma Categoria Inteira"])
            if t_ex == "Um Produto":
                cursor.execute("SELECT id, nome, categoria FROM produtos ORDER BY categoria")
                lista_p = cursor.fetchall()
                if lista_p:
                    it = st.selectbox("Escolha o item", lista_p, format_func=lambda x: f"[{x[2]}] {x[1]}")
                    if st.button("❌ EXCLUIR ITEM PERMANENTEMENTE"):
                        cursor.execute("DELETE FROM produtos WHERE id = ?", (it[0],))
                        db.commit(); st.cache_data.clear(); st.rerun()
            else:
                if categorias_existentes:
                    cat_ex = st.selectbox("Escolha a categoria", categorias_existentes)
                    if st.button("🔥 EXCLUIR CATEGORIA INTEIRA"):
                        cursor.execute("DELETE FROM produtos WHERE categoria = ?", (cat_ex,))
                        db.commit(); st.cache_data.clear(); st.rerun()
        db.close()

# --- 5. CORPO DO CARDÁPIO ---

# Fundo do bar
fundo_b64 = carregar_imagem_base64('fundo_bar.png') or carregar_imagem_base64('img/fundo_bar.png')
if fundo_b64:
    st.markdown(f'''<style>.stApp {{ background-image: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("data:image/png;base64,{fundo_b64}"); background-size: cover; background-position: center; background-attachment: fixed; }} </style>''', unsafe_allow_html=True)

# 5.1 Cabeçalho
logo_b64 = carregar_imagem_base64("vr_logo.png") or carregar_imagem_base64("img/vr_logo.png")
if logo_b64:
    st.markdown(f'''
        <div style="text-align:center;">
            <img src="data:image/png;base64,{logo_b64}" width="180">
            <p style="color:white; letter-spacing:5px; font-weight:200; margin-top:10px; margin-bottom:5px;">CARDÁPIO DIGITAL</p>
            <p style="color:#888; font-size:0.85rem; margin-bottom:5px; line-height:1.4;">
                📍 Av. Vaticano, N° 4 - Anjo da Guarda<br>São Luís - MA, 65071-383
            </p>
            <div style="display:inline-block; border:1px solid #FF4B4B; color:#FF4B4B; padding:2px 12px; border-radius:5px; font-size:0.7rem; font-weight:bold; margin-top:5px;">
                🔞 PROIBIDO PARA MENORES DE 18 ANOS
            </div>
        </div>
    ''', unsafe_allow_html=True)

# 5.2 Listagem de Produtos (FILTRADA: apenas disponivel = 1)
for p in itens:
        # Busca os dados da imagem já formatados pela função nova
        full_img_data = carregar_imagem_base64(p[4])
        
        # Se a imagem existir, usa o HTML; se não, usa o emoji de copo
        if full_img_data:
            img_html = f'<img src="{full_img_data}" style="max-width:100%; max-height:100%; object-fit: contain;">'
        else:
            img_html = '🥃'
        
        preco_formatado = f"{p[2]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # Mantenha o restante do st.markdown igual ao que você já tem...

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; gap: 15px;">
            <div style="width: 60px; height: 60px; flex-shrink: 0; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.03); border-radius:8px; overflow:hidden;">{img_html}</div>
            <div style="flex-grow: 1;"><span style="color:white; font-weight:bold; font-size:1.1rem;">{p[1]}</span><br><span style="color:#888; font-size:0.8rem;">{p[3]}</span></div>
            <div style="color:#FF4B4B; font-weight:900; font-size:1.1rem; background:rgba(255,75,75,0.1); padding:8px; border-radius:8px; white-space: nowrap;">R$ {preco_formatado}</div>
        </div>
        """, unsafe_allow_html=True)
db.close()

# 5.3 Rodapé
st.markdown(f'''
    <div style="text-align:center; margin-top:50px; padding-bottom:30px; border-top: 1px solid #222; padding-top:20px;">
        <p style="color:#FF4B4B; font-weight:bold; margin-bottom:5px;">www.cardapiovr.com.br</p>
        <p style="color:#555; font-size:0.75rem;">Copyright © 2026 <b>VR - VIDA RASA</b><br>Desenvolvido por Johnny Cardoso</p>
    </div>
''', unsafe_allow_html=True)



