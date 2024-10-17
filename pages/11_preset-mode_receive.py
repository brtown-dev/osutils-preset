import streamlit as st
import base_module as b
import pandas as pd
import random
import re

# import openpyxl
# import collections
# import datetime
# import uuid
# import requests
# import json

# Receive Preset
# /wms/common/relationship-preset/receive
# SAMPLE
# {
#     "uuid": "sort001", 
#     "name": "sort001-SITE-1", 
#     "details": [
#         {
#             "destination": "A1-1",
#             "type": [ "normal" ],
#             "priority": 1,
#             "relationships": [
#                 {
#                     "key": "barcode",
#                     "value": "S0607",
#                     "condition": "equal"
#                 }
#             ],
#         }，
#         {
#             "destination": "A1-2",
#             "type": [ "noread" ],
#             "priority": 1,
#             "relationships": [],
#         }，
#         {
#             "destination": "A1-3",
#             "type": [ "nofind", "wmsReject" ],
#             "priority": 1,
#             "relationships": [],
#         }，
#     ]
# }

c = b.read_config("config.json")

def main():
    if 'key' not in st.session_state: 
        st.session_state.key = str(random.randint(1000, 100000000))

    st.header('preset mode - receive', divider='grey')
    infile = st.file_uploader("Choose a xlsx file", type="xlsx", key=st.session_state.key)

    with open("pages/sample_preset.xlsx", 'rb') as f:
        st.download_button('Download Sample', f, file_name='sample_preset.xlsx')


    if infile:
        df = pd.read_excel(infile)
        df = df.fillna("")  # "nan"を空文字に変換
        df = df.astype(str)  # 全データを文字列に変換

        # check barcode duplication
        state = 0
        dup = list(set(df[df.iloc[:, 0].duplicated()].iloc[:,0].tolist()))
        if len(dup) > 0:
            st.error(f'Duplicate Barcode: {", ".join(dup)}')
            state = 1
        
        rows = 2
        for x in df.values.tolist():
            # barcode列に空セルが無いかチェック
            if x[0] == "":
                st.error(f'no barcode: {str(rows)}: {", ".join(x)}')
                state = 1

            # gridId列に空セルがが無いかチェック
            if x[1] == "":
                st.error(f'no grid: {str(rows)}: {", ".join(x)}')           
                state = 1

            # gridIdの書式確認
            for y in x[1].split('/'):
                if not re.match(r'^[AB]\d+-\d+$', y):
                    st.error(f'invalid gridId: {str(rows)}: {x[1]}')
                    state = 1
            rows += 1

        # gridId不一致確認
        rules = [x[1] for x in df.values.tolist()]
        rules = list(set(rules))
        grids = list()
        for x in rules:
            grids.extend(x.split('/'))
        grids = sorted(list(set(grids)))

        for x in grids:
            match = list()
            for y in rules:
                if re.search(x, y):
                    match.append(y)
            
            if len(match) > 1:
                st.error(f'invalid rule: {match}')
                state = 1

        # もし読み込んだファイルにエラーがなければ実行
        if state == 0:
            if st.button("Post", type="primary"):
                payload = generate_payload(df.values.tolist())
                st.session_state.key = str(random.randint(1000, 100000000))
                # st.rerun()
                st.write(st.session_state)
            else:
                st.dataframe(df, hide_index=True)

def generate_payload(d):
    payload = dict(
        {
            "name": str(),
            "uuid": str(),
            "details": list()
        }
    )
    sorted = dict()
    for i in d:
        if i[1] in sorted.keys():
            sorted[i[1]].append(i[0])
        else:
            sorted[i[1]] = [i[0]]
    
    for x in sorted:
        grids = x.split("/")
        priority = len(grids)
        for grid in grids:
            if sorted[x][0] == "REJECT":
                pass
                # {
                #     "destination": "B2-1",
                #     "type": ["noread","wmsReject","noRelationship"],
                #     "priority": 1,
                #     "relationships": []
                # },

            else:
                y = {
                    "destination": grid,
                    "type": ["normal"],
                    "priority": priority,
                    "relationships": list()
                }

                for z in sorted[x]:
                    y["relationships"].append(
                        {
                            "key": "barcode",
                            "value": str(z),
                            "condition": "equal"
                        }
                    )

            priority -= 1
        
            payload["details"].append(y)
    
    return payload


def read_file(infile):
    df = pd.read_excel(infile)
    return list(set(df[df.iloc[:, 0].duplicated()].iloc[:,0].to_list()))

if __name__ == "__main__":
    main()