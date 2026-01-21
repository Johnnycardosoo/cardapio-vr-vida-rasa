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
    
    try:
        conn.execute("ALTER TABLE produtos ADD COLUMN disponivel INTEGER DEFAULT 1")
    except:
        pass
        
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
        
        if os.path.exists("cardapio_vr.db"):
            with open("cardapio_vr.db", "rb") as f:
                st.download_button(label="📥 Backup Banco", data=f, file_name="cardapio_vr.db")
        
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
                ml = st.text_input("ML/Tamanho")
                arquivo = st.file_uploader("Foto do Produto", type=['png', 'jpg', 'jpeg'])
                
                if st.form_submit_button("✅ SALVAR PRODUTO"):
                    if cat_final and nome and arquivo:
                        caminho_img = os.path.join("img", arquivo.name)
                        with open(caminho_img, "wb") as f:
                            f.write(arquivo.getbuffer())
                        
                        cursor.execute("INSERT INTO produtos (categoria, nome, preco, ml, img_path, disponivel) VALUES (?,?,?,?,?,1)",
                                     (cat_final, nome, prec, ml, caminho_img))
                        db.commit()
                        st.cache_data.clear()
                        st.success(f"{nome} adicionado!")
                        st.rerun()

        elif aba == "Editar / Ocultar":
            cursor.execute("SELECT id, nome, preco, ml, img_path, categoria, disponivel FROM produtos")
            todos_itens = cursor.fetchall()
            if todos_itens:
                item_selecionado = st.selectbox("Selecione o produto", todos_itens, 
                                              format_func=lambda x: f"{'🟢' if x[6]==1 else '🔴'} [{x[5]}] {x[1]}")
                
                with st.form("form_editar"):
                    n_nome = st.text_input("Nome", value=item_selecionado[1])
                    n_prec = st.number_input("Preço", value=float(item_selecionado[2]))
                    n_ml = st.text_input("ML", value=item_selecionado[3])
                    n_disp = st.checkbox("Disponível no Cardápio", value=True if item_selecionado[6] == 1 else False)
                    n_foto = st.file_uploader("Trocar Foto (Opcional)", type=['png', 'jpg', 'jpeg'])
                    
                    if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                        caminho_foto_final = item_selecionado[4]
                        if n_foto:
                            caminho_foto_final = os.path.join("img", n_foto.name)
                            with open(caminho_foto_final, "wb") as f:
                                f.write(n_foto.getbuffer())
                        
                        cursor.execute("UPDATE produtos SET nome=?, preco=?, ml=?, img_path=?, disponivel=? WHERE id=?",
                                     (n_nome, n_prec, n_ml, caminho_foto_final, 1 if n_disp else 0, item_selecionado[0]))
                        db.commit()
                        st.cache_data.clear()
                        st.success("Atualizado!")
                        st.rerun()

        elif aba == "Excluir":
            cursor.execute("SELECT id, nome, categoria FROM produtos ORDER BY categoria")
            lista_produtos = cursor.fetchall()
            if lista_produtos:
                item_excluir = st.selectbox("Item para DELETAR", lista_produtos, format_func=lambda x: f"[{x[2]}] {x[1]}")
                if st.button("❌ EXCLUIR DEFINITIVAMENTE"):
                    cursor.execute("DELETE FROM produtos WHERE id = ?", (item_excluir[0],))
                    db.commit()
                    st.cache_data.clear()
                    st.rerun()
        db.close()

# --- 5. CORPO DO CARDÁPIO (VISUAL CLIENTE) ---
fundo_data = carregar_imagem_base64('fundo_bar.png') or carregar_imagem_base64('img/fundo_bar.png')
if fundo_data:
    st.markdown(f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("{fundo_data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    ''', unsafe_allow_html=True)

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

db = conectar_db()
cursor = db.cursor()
cursor.execute("SELECT categoria, nome, preco, ml, img_path FROM produtos WHERE disponivel = 1 ORDER BY categoria, nome")
todos_produtos = cursor.fetchall()

menu_por_categoria = {}
for p in todos_produtos:
    cat = p[0]
    if cat not in menu_por_categoria:
        menu_por_categoria[cat] = []
    menu_por_categoria[cat].append(p)

for categoria, itens in menu_por_categoria.items():
    st.markdown(f"<div style='color:white; text-transform:uppercase; letter-spacing:4px; font-weight:900; margin-top:30px; border-bottom: 2px solid #FF4B4B; padding-bottom:5px; margin-bottom:15px;'>{categoria}</div>", unsafe_allow_html=True)
    
    for p in itens:
        img_data = carregar_imagem_base64(p[4])
        img_html = f'<img src="{img_data}" style="width: 100%; height: 100%; object-fit: contain;">' if img_data else '<span style="font-size:20px;">🥃</span>'
        preco_formatado = f"{p[2]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Estrutura HTML do card
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; gap: 12px; border: 1px solid rgba(255,255,255,0.03);">
            <div style="width: 52px; height: 52px; flex-shrink: 0; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.03); border-radius:8px; overflow:hidden;">
                {img_html}
            </div>
            <div style="flex-grow: 1; min-width: 0; overflow: hidden;">
                <div style="color:white; font-weight:bold; font-size:0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {p[1]} {p[3]}
                </div>
            </div>
            <div style="color:#FF4B4B; font-weight:900; font-size:1rem; background:rgba(255,75,75,0.1); padding:8px 10px; border-radius:8px; white-space: nowrap; flex-shrink: 0; min-width: fit-content; text-align: center;">
                R$ {preco_formatado}
            </div>
        </div>
        """, unsafe_allow_html=True)

db.close()

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
