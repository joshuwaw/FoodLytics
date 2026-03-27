import streamlit as st
import qrcode
from io import BytesIO

# Change this to your actual Streamlit URL once you deploy
PRODUCTION_URL = "https://foodlytics-ff5zenhikjdcqmqspxy52u.streamlit.app/"

def get_base_url():
    """Detects if the app is running locally or in production."""
    # Check if we are running on local host ports
    if st.config.get_option("server.address") == "localhost" or st.config.get_option("server.port") == 8501:
        return "http://localhost:8501"
    return PRODUCTION_URL

def show_admin_page(supabase):
    st.sidebar.title("FoodLytics Admin")
    menu = st.sidebar.radio("Navigasi", ["Penjana QR", "Daftar Premis"])
    
    if menu == "Penjana QR":
        st.header("Pengurusan Kod QR")
        
        # Fetch list of cafes
        try:
            response = supabase.table("tbl_premis").select("id_premis, nama_premis").execute()
            cafes = response.data
        except Exception as e:
            st.error(f"Galat pangkalan data: {e}")
            return

        if not cafes:
            st.info("Sila daftar premis baru di tab 'Daftar Premis' terlebih dahulu.")
            return

        cafe_options = {c['nama_premis']: c['id_premis'] for c in cafes}
        selected_name = st.selectbox("Pilih Premis:", list(cafe_options.keys()))
        selected_id = cafe_options[selected_name]

        if st.button("Jana Kod QR"):
            # Dynamic URL Generation
            base = get_base_url()
            target_url = f"{base}/?id_premis={selected_id}"
            
            # QR Code Generation logic
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(target_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buf = BytesIO()
            img.save(buf, format="PNG")
            
            st.info(f"Pautan dalam QR: {target_url}") # Useful for debugging
            st.image(buf.getvalue(), caption=f"Kod QR untuk {selected_name}")
            st.download_button(
                label="Muat Turun PNG", 
                data=buf.getvalue(), 
                file_name=f"QR_{selected_name.replace(' ', '_')}.png", 
                mime="image/png"
            )
            
    else:
        st.header("Pendaftaran Premis Baru")
        with st.form("reg_premis", clear_on_submit=True):
            nama = st.text_input("Nama Premis")
            alamat = st.text_area("Alamat Lengkap")
            submit = st.form_submit_button("Daftar")
            
            if submit and nama:
                try:
                    supabase.table("tbl_premis").insert({
                        "nama_premis": nama, 
                        "alamat_premis": alamat
                    }).execute()
                    st.success(f"{nama} telah didaftarkan!")
                    st.rerun() # Refresh to show the new cafe in the QR generator dropdown
                except Exception as e:
                    st.error(f"Gagal mendaftar: {e}")