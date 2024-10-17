import streamlit as st
import base_module

# Switch Preset
# /wms/common/relationship-preset/switch
# SAMPLE
# {
#     "uuid": "sort001", 
#     "systemId": "S181", 
# }

c = base_module.read_config("config.json")

def main():
    st.header('preset mode - switch', divider='grey')
    st.write(f'Preset URL: {c["uri"]}/#/ruleTable')

    with st.form("form", clear_on_submit=True ):
        # u = st.text_input("Input uuid of the preset you want to remove, then submit", key=st.session_state.key)
        u = st.text_input("Input uuid of the preset you want to remove, then submit")
        u = u.strip()

        submitted = st.form_submit_button("Submit")
   
        if submitted and not len(u) == 0 :
            data = {
                "uuid": u,
                "systemId": c["systemid"],
            }
            response = base_module.post_data(data, "/wms/common/relationship-preset/switch")
            st.write(u)
            st.success(response.status_code)
            st.success(response.text)
            
if __name__ == "__main__":
    main()