import streamlit as st
import os
import base64

# 1. Configuração da página
st.set_page_config(page_title="VR - Vida Rasa", page_icon="🥃", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM DE FUNDO ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    if os.path.exists(png_file):
        bin_str = get_base64(png_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('fundo_bar.png')

# 2. Estilização Visual Avançada (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600;800&display=swap');
    
    .stApp { color: white; font-family: 'Inter', sans-serif; }

    .titulo-cardapio {
        color: #FFFFFF; font-size: 24px; font-weight: 200; text-align: center;
        text-transform: uppercase; letter-spacing: 12px; margin-top: 20px; opacity: 0.9;
    }

    .subtitulo-bar {
        color: #FF4B4B; text-align: center; font-size: 12px; font-weight: 800;
        letter-spacing: 8px; text-transform: uppercase; margin-bottom: 5px;
    }

    .endereco-bar {
        color: #888; text-align: center; font-size: 10px; font-weight: 400;
        text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px;
    }

    .restricao-idade {
        color: #FF4B4B; text-align: center; font-size: 9px; font-weight: 800;
        text-transform: uppercase; letter-spacing: 3px; margin-bottom: 30px;
        opacity: 0.8;
    }

    .product-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border-left: 3px solid #FF4B4B;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .product-name { font-size: 1rem; font-weight: 600; color: #FFFFFF; display: block; }
    .product-ml { color: #888; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

    .price-badge {
        background: rgba(255, 75, 75, 0.1);
        color: #FF4B4B; padding: 6px 12px; border-radius: 8px;
        font-weight: 800; font-size: 0.95rem; border: 1px solid rgba(255, 75, 75, 0.2);
        text-align: center;
    }
    
    .category-header {
        color: #FFFFFF; text-transform: uppercase; letter-spacing: 5px;
        font-size: 0.9rem; font-weight: 800; margin: 45px 0 20px 0;
        display: flex; align-items: center;
    }

    .category-header::after {
        content: ""; flex: 1; height: 1px;
        background: linear-gradient(90deg, #FF4B4B, transparent);
        margin-left: 15px; opacity: 0.3;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho
if os.path.exists("vr_logo.png"):
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        st.image("vr_logo.png", use_container_width=True)
else:
    st.markdown("<h1 style='text-align: center; color: #FF4B4B; letter-spacing: 5px; margin-bottom:0;'>VR</h1>", unsafe_allow_html=True)

st.markdown('<p class="titulo-cardapio">Cardápio Digital</p>', unsafe_allow_html=True)
st.markdown('<p class="endereco-bar">📍 AV. VATICANO, N° 4 - ANJO DA GUARDA, SÃO LUÍS - MA</p>', unsafe_allow_html=True)
st.markdown('<p class="restricao-idade">🔞 PROIBIDO PARA MENORES DE 18 ANOS</p>', unsafe_allow_html=True)

# 4. Dados do Cardápio
cardapio = {
    "CERVEJAS": [
        {"nome": "Stella Artois", "preco": 15.00, "img": "stella_600ml.png", "ml": "600ml"},
        {"nome": "Stella Long Neck", "preco": 12.00, "img": "stella_long.png", "ml": "330ml"},
        {"nome": "Corona Extra", "preco": 12.00, "img": "corona_long.png", "ml": "330ml"},
        {"nome": "Skol Beats", "preco": 10.00, "img": "skol_beats_lata.png", "ml": "269ml"}
    ],
    "COPÃO": [
        {"nome": "Copão Whisky", "preco": 25.00, "img": "copao.png", "ml": "500ml"},
        {"nome": "Copão Whisky", "preco": 30.00, "img": "copao.png", "ml": "700ml"}
    ],
    "COMBOS": [
        {"nome": "Combo Buchanan's", "preco": 400.00, "img": "combo_buchanans.png", "ml": "1L + 4 Energéticos"},
        {"nome": "Combo Old Parr", "preco": 350.00, "img": "combo_oldparr.png", "ml": "1L + Gelo Sabor"},
        {"nome": "Combo Red Label", "preco": 250.00, "img": "combo_red.png", "ml": "1L + Gelo"}
    ],
    "DOSES": [
        {"nome": "Dose Buchanan's", "preco": 35.00, "img": "dose.png", "ml": "50ml"},
        {"nome": "Dose Old Parr", "preco": 30.00, "img": "dose.png", "ml": "50ml"},
        {"nome": "Dose Red Label", "preco": 20.00, "img": "dose.png", "ml": "50ml"}
    ],
    "EXTRAS": [
        {"nome": "Água Mineral", "preco": 5.00, "img": "agua.png", "ml": "500ml"},
        {"nome": "Gelo Saborizado", "preco": 10.00, "img": "gelo.png", "ml": "Unidade"},
        {"nome": "Gelo em Cubos", "preco": 20.00, "img": "gelo.png", "ml": "Pacote 5kg"}
    ]
}

# 5. Renderização
for categoria, itens in cardapio.items():
    st.markdown(f"<div class='category-header'>{categoria}</div>", unsafe_allow_html=True)
    for item in itens:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([0.5, 2, 0.9])
        with c1:
            if os.path.exists(item["img"]):
                st.image(item["img"], width=60)
            else:
                st.markdown("<div style='font-size:24px; padding-top:10px;'>🥃</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='margin-left: 10px;'><span class='product-name'>{item['nome']}</span><span class='product-ml'>{item['ml']}</span></div>", unsafe_allow_html=True)
        with c3:
            preco_visivel = f"{item['preco']:.2f}".replace('.', ',')
            st.markdown(f"<div class='price-badge'>R$ {preco_visivel}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 6. Rodapé Atualizado com Créditos
st.divider()
st.markdown(f"""
    <div style='text-align: center; padding-bottom: 40px;'>
        <p style='color: #FF4B4B; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px;'>www.vrvidarasa.com.br</p>
        <p style='color: #888; font-size: 0.85rem;'>
            Copyright © 2026 <b>VR - VIDA RASA</b><br>
            Todos os direitos reservados.<br>
            <span style='font-size: 0.75rem; opacity: 0.6;'>Desenvolvido por <b>Johnny Cardoso</b></span>
        </p>
    </div>
    """, unsafe_allow_html=True)
