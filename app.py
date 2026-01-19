import streamlit as st
import os

# 1. Configuração da página
st.set_page_config(page_title="VR - Vida Rasa", page_icon="🥃", layout="centered")

# 2. Estilização Visual Avançada (CSS) - VERSÃO PREMIUM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    .stApp { 
        background-color: #050505; 
        color: white; 
        font-family: 'Inter', sans-serif; 
    }

    /* TÍTULO EM CAIXA ALTA, FINO E ELEGANTE */
    .titulo-cardapio {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-size: 26px; 
        font-weight: 200; 
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 10px; 
        margin-top: 30px;
        margin-bottom: 5px;
        opacity: 0.8;
    }

    .subtitulo-bar {
        color: #FF4B4B;
        text-align: center;
        font-size: 14px; 
        font-weight: 600;
        letter-spacing: 10px; 
        text-transform: uppercase;
        margin-bottom: 10px;
        opacity: 0.9;
    }

    .endereco-bar {
        color: #888;
        text-align: center;
        font-size: 10px;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }

    /* CARTÃO DO PRODUTO (EFEITO GLASS) */
    .product-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.3s ease, background 0.3s ease;
    }
    
    .product-card:hover {
        background: rgba(255, 255, 255, 0.07);
        transform: translateY(-2px);
        border-color: rgba(255, 75, 75, 0.3);
    }

    .price-tag {
        color: #FF4B4B;
        font-weight: 800;
        font-size: 1.2rem;
        margin-top: 10px;
    }
    
    .product-name { 
        font-size: 1.1rem; 
        font-weight: 600; 
        color: #FFFFFF;
        letter-spacing: 0.5px;
    }
    
    .category-header {
        color: #FFFFFF;
        text-transform: uppercase;
        text-align: center;
        letter-spacing: 4px;
        font-size: 1.1rem;
        font-weight: 400;
        margin: 60px 0 30px 0;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }

    .stImage img {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho (Logo e Títulos)
if os.path.exists("vr_logo.png"):
    col_l, col_c, col_r = st.columns([1, 1.8, 1])
    with col_c:
        st.image("vr_logo.png", use_container_width=True)
else:
    st.markdown("<h1 style='text-align: center; color: #FF4B4B; margin-bottom: 0px;'>VR - VIDA RASA</h1>", unsafe_allow_html=True)

st.markdown('<p class="titulo-cardapio">CARDÁPIO DIGITAL</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-bar">PREMIUM BAR</p>', unsafe_allow_html=True)

# Endereço como texto simples
st.markdown('<p class="endereco-bar">📍 AV. VATICANO, N° 4 - ANJO DA GUARDA, SÃO LUÍS - MA</p>', unsafe_allow_html=True)

st.divider()

# 4. Dados do Cardápio
cardapio = {
    "CERVEJAS": [
        {"nome": "Stella 600ml", "preco": 15.00, "img": "stella_600ml.png", "desc": "Puro malte bem gelada"},
        {"nome": "Stella Long Neck", "preco": 12.00, "img": "stella_long.png", "desc": "Refrescante"},
        {"nome": "Corona Long Neck", "preco": 12.00, "img": "corona_long.png", "desc": "Com fatia de limão"},
        {"nome": "Skol Beats Lata", "preco": 10.00, "img": "skol_beats_lata.png", "desc": "Sabor vibrante"}
    ],
    "COPÃO": [
        {"nome": "Copão 500ml", "preco": 25.00, "img": "copao.png", "desc": "Whisky + Energético + Gelo Saborizado"},
        {"nome": "Copão 700ml", "preco": 30.00, "img": "copao.png", "desc": "Whisky + Energético + Gelo Saborizado"}
    ],
    "COMBOS": [
        {"nome": "Combo Buchanan's", "preco": 400.00, "img": "combo_buchanans.png", "desc": "1L + 4 Energéticos + Gelo"},
        {"nome": "Combo Old Parr", "preco": 350.00, "img": "combo_oldparr.png", "desc": "1L + Gelo Saborizado"},
        {"nome": "Combo Red Label", "preco": 250.00, "img": "combo_red.png", "desc": "O clássico das noites"}
    ],
    "DOSES": [
        {"nome": "Dose Buchanan's", "preco": 35.00, "img": "dose.png", "desc": "Dose 50ml"},
        {"nome": "Dose Old Parr", "preco": 30.00, "img": "dose.png", "desc": "Dose 50ml"},
        {"nome": "Dose Red Label", "preco": 20.00, "img": "dose.png", "desc": "Dose 50ml"}
    ],
    "EXTRAS": [
        {"nome": "Água 500ml", "preco": 5.00, "img": "agua.png", "desc": "Com ou sem gás"},
        {"nome": "Gelo Saborizado", "preco": 10.00, "img": "gelo.png", "desc": "Coco, Maracujá ou Melancia"},
        {"nome": "Gelo em Cubos", "preco": 20.00, "img": "gelo.png", "desc": "Pacote com 5kg"}
    ]
}

# 5. Renderização
for categoria, itens in cardapio.items():
    st.markdown(f"<h3 class='category-header'>{categoria}</h3>", unsafe_allow_html=True)
    
    for item in itens:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([0.4, 2]) 
        
        with c1:
            if os.path.exists(item["img"]):
                st.image(item["img"], width=70) 
            else:
                st.markdown("<div style='width:70px; height:70px; background:#1a1a1a; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:20px;'>📷</div>", unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"<div style='margin-top: -5px;'><span class='product-name'>{item['nome']}</span></div>", unsafe_allow_html=True)
            if item["desc"]:
                st.caption(item["desc"])
            st.markdown(f"<div class='price-tag'>R$ {item['preco']:.2f}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 6. Rodapé Finalizado
st.divider()
st.markdown(f"""
    <div style='text-align: center; padding-bottom: 40px; padding-top: 20px;'>
        <p style='color: #FF4B4B; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; letter-spacing: 1px;'>
            www.vrvidarasa.com.br
        </p>
        <p style='color: #888; font-size: 0.85rem; line-height: 1.6;'>
            <span style='letter-spacing: 1px;'>Copyright © 2026 <b>VR - VIDA RASA</b></span><br>
            <b>Todos os direitos reservados.</b><br>
            <span style='font-size: 0.75rem; color: #555;'>Proibido para menores de 18 anos.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)