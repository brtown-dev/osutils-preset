import streamlit as st
import base_module

# Delete Preset
# /wms/common/relationship-preset/delete
# SAMPLE
# {
#     "uuid": "sort001", 
# }

c = base_module.read_config("config.json")

def main():
    # if 'key' not in st.session_state: st.session_state.key = base.issue_session_key()

    st.header('preset mode - delete', divider='grey')
    st.write(f'Preset URL: {c["uri"]}/#/ruleTable')

    with st.form("form", clear_on_submit=True ):
        # u = st.text_input("Input uuid of the preset you want to remove, then submit", key=st.session_state.key)
        u = st.text_input("Input uuid of the preset you want to remove, then submit")
        u = u.strip()

        submitted = st.form_submit_button("Submit")
   
        if submitted and not len(u) == 0 :
            data = {
                "uuid": u
            }
            response = base_module.post_data(data, "/wms/common/relationship-preset/delete")
            st.write(u)
            st.success(response.status_code)
            st.success(response.text)
            
if __name__ == "__main__":
    main()