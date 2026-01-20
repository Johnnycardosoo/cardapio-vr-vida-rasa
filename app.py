import streamlit as st
import os
import base64

# 1. Configuração da página - Otimizada para Mobile
st.set_page_config(page_title="VR - Cardápio", page_icon="🥃", layout="centered")

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def set_background(png_file):
    bin_str = get_base64(png_file)
    if bin_str:
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.88), rgba(0, 0, 0, 0.88)), url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('fundo_bar.png')

# 2. CSS MOBILE-FIRST
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
    .stApp { color: white; font-family: 'Inter', sans-serif; }

    .titulo-cardapio {
        color: #FFFFFF; font-size: 20px; font-weight: 200; text-align: center;
        text-transform: uppercase; letter-spacing: 10px; margin-top: 10px;
    }

    .subtitulo-bar {
        color: #FF4B4B; text-align: center; font-size: 11px; font-weight: 800;
        letter-spacing: 6px; text-transform: uppercase; margin-bottom: 5px;
    }

    .endereco-bar {
        color: #999; text-align: center; font-size: 9px; 
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;
    }

    .restricao-idade {
        color: #FF4B4B; text-align: center; font-size: 9px; font-weight: 800;
        letter-spacing: 2px; margin-bottom: 25px;
    }

    .product-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-left: 4px solid #FF4B4B;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    
    .product-name { font-size: 0.95rem; font-weight: 600; color: #FFFFFF; line-height: 1.2; }
    .product-ml { color: #888; font-size: 0.7rem; text-transform: uppercase; margin-top: 3px; }

    .price-badge {
        background: rgba(255, 75, 75, 0.15);
        color: #FF4B4B; padding: 8px 10px; border-radius: 10px;
        font-weight: 800; font-size: 0.9rem; border: 1px solid rgba(255, 75, 75, 0.3);
        min-width: 85px; text-align: center;
    }
    
    .category-header {
        color: #FFFFFF; text-transform: uppercase; letter-spacing: 4px;
        font-size: 0.85rem; font-weight: 800; margin: 35px 0 15px 0;
        display: flex; align-items: center;
    }

    .category-header::after {
        content: ""; flex: 1; height: 1px;
        background: linear-gradient(90deg, #FF4B4B, transparent);
        margin-left: 10px; opacity: 0.3;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho
if os.path.exists("vr_logo.png"):
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        st.image("vr_logo.png", use_container_width=True)
else:
    st.markdown("<h1 style='text-align: center; color: #FF4B4B; letter-spacing: 5px; margin-bottom:0; font-size: 40px;'>VR</h1>", unsafe_allow_html=True)

st.markdown('<p class="titulo-cardapio">Cardápio</p>', unsafe_allow_html=True)
st.markdown('<p class="endereco-bar">📍 AV. VATICANO, N° 4 - ANJO DA GUARDA, SÃO LUÍS - MA</p>', unsafe_allow_html=True)
st.markdown('<p class="restricao-idade">🔞 PROIBIDO PARA MENORES DE 18 ANOS</p>', unsafe_allow_html=True)

# 4. Dados
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
        c1, c2, c3 = st.columns([0.6, 2, 1.1])
        with c1:
            if os.path.exists(item["img"]):
                st.image(item["img"], width=50)
            else:
                st.markdown("<div style='font-size:20px;'>🥃</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div><span class='product-name'>{item['nome']}</span><br><span class='product-ml'>{item['ml']}</span></div>", unsafe_allow_html=True)
        with c3:
            preco_visivel = f"{item['preco']:.2f}".replace('.', ',')
            st.markdown(f"<div class='price-badge'>R$ {preco_visivel}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 6. Rodapé Restaurado (Johnny Cardoso Style)
st.divider()
st.markdown(f"""
    <div style='text-align: center; padding-bottom: 40px; padding-top: 20px;'>
        <p style='color: #FF4B4B; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; letter-spacing: 1px;'>
            www.vrvidarasa.com.br
        </p>
        <p style='color: #888; font-size: 0.85rem; line-height: 1.6;'>
            <span style='letter-spacing: 1px;'>Copyright © 2026 <b>VR - VIDA RASA</b></span><br>
            <b>Todos os direitos reservados.</b><br>
            <span style='font-size: 0.75rem; color: #555;'>Desenvolvido por <b>Johnny Cardoso</b></span>
        </p>
    </div>
    """, unsafe_allow_html=True)
