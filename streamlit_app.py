import streamlit as st
import functions as ft
def giris():
    users={
        "merve":"19031903",
        "nazli":"Q7.ihaber",
    }
    st.title("Haber Asistan V 1.2")
    with st.form("giriş",clear_on_submit=True):
        username=st.text_input("Kullanıcı Adı")
        password=st.text_input("Şifre",type="password")
        buton=st.form_submit_button("Giriş Yap")
        if buton:
            if users.get(username)==password:
                st.session_state["key"]="1"
                st.experimental_rerun()
            else:
                st.error("Kullanıcı Adı veya Şifre Hatalı")


        else:
            st.stop()

if "key" not in st.session_state:
    giris()

else:

    st.button("Yenile")

    ft.topluHaberEkle()
    gunluk_trends=ft.trendsfull()
    df=ft.haberGetir()

    st.sidebar.title("Anlık Keyword")
    gunluk_trends.reverse()
    for a in gunluk_trends:
        st.sidebar.error(a[0])


    dakika=round(df['kalan'].dt.total_seconds()/60)
    sozluk = dict(zip(df['Başlık'],dakika))

    col1,col2=st.columns([3,1])
    with col1:
        st.subheader("Başlık")
    with col2:
        st.subheader("Kalan Süre")

    for haber in sozluk.keys():
        col1,col2=st.columns([3,1])
        with col1:

            st.write(haber)
        with col2:

            st.write(sozluk[haber],"dk")
        st.markdown("""---""")


    hide_streamlit_style = """
                <style>
                .viewerBadge_link__1S137 {display:none!important;}
                .viewerBadge_link__1S137 {visibility: hidden!important;}
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .viewerBadge_container__1QSob {visibility: hidden!important;}


                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
