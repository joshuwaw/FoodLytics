import streamlit as st
import datetime

def show_customer_portal(supabase, premis_id):
    # Fetch cafe name for better UX
    try:
        res = supabase.table("tbl_premis").select("nama_premis").eq("id_premis", premis_id).maybe_single().execute()
        cafe_name = res.data['nama_premis'] if res.data else "Premis Tidak Dikenali"
    except:
        cafe_name = "Premis Unknown"

    st.title(f"Maklum Balas: {cafe_name}")
    st.write("Sila berikan ulasan anda untuk membantu kami menambah baik kualiti perkhidmatan.")

    with st.form("feedback_form", clear_on_submit=True):
        rating = st.select_slider("Rating Bintang", options=[1, 2, 3, 4, 5], value=5)
        comment = st.text_area("Ulasan Anda", placeholder="Contoh: Makanan sedap tapi servis agak lambat...")
        
        submitted = st.form_submit_button("Hantar Maklum Balas")
        
        if submitted:
            if not comment.strip():
                st.error("Sila masukkan ulasan teks.")
            else:
                new_feedback = {
                    "id_premis": int(premis_id),
                    "bilangan_bintang": rating,
                    "ulasan_teks": comment,
                    "sumber_platform": "Portal QR",
                    "tarikh_terima": datetime.datetime.now().isoformat()
                }
                supabase.table("tbl_maklumbalas").insert(new_feedback).execute()
                st.balloons()
                st.success("Terima kasih! Maklum balas anda telah disimpan.")
