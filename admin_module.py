import streamlit as st
import qrcode
from io import BytesIO

def show_admin_page(supabase):
    st.sidebar.title("FoodLytics Admin")
    menu = st.sidebar.radio("Navigasi", ["Penjana QR", "Daftar Premis"])
    
    if menu == "Penjana QR":
        st.header("Pengurusan Kod QR")
        
        # Fetch list of cafes
        response = supabase.table("tbl_premis").select("id_premis, nama_premis").execute()
        cafes = response.data

        if not cafes:
            st.info("Sila daftar premis baru di tab 'Daftar Premis' terlebih dahulu.")
            return

        cafe_options = {c['nama_premis']: c['id_premis'] for c in cafes}
        selected_name = st.selectbox("Pilih Premis:", list(cafe_options.keys()))
        selected_id = cafe_options[selected_name]

        if st.button("Jana Kod QR"):
            # Create URL with parameter
            # Note: Change this to your deployed URL once you go live
            target_url = f"http://localhost:8501/?id_premis={selected_id}"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(target_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buf = BytesIO()
            img.save(buf, format="PNG")
            
            st.image(buf.getvalue(), caption=f"Kod QR untuk {selected_name}")
            st.download_button("Muat Turun PNG", buf.getvalue(), f"QR_{selected_name}.png", "image/png")
            
    else:
        st.header("Pendaftaran Premis Baru")
        with st.form("reg_premis"):
            nama = st.text_input("Nama Premis")
            alamat = st.text_area("Alamat Lengkap")
            submit = st.form_submit_button("Daftar")
            
            if submit and nama:
                supabase.table("tbl_premis").insert({"nama_premis": nama, "alamat_premis": alamat}).execute()
                st.success(f"{nama} telah didaftarkan!")
