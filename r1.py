import streamlit as st
import json
import datetime
import glob
import os

def save_status():
     status = {
          "debt": st.session_state.debt,
          "prepaid_bottle": st.session_state.prepaid_bottle,
          "transactions": st.session_state.transactions
     }
     username = st.session_state.username
     filename = f"user_data/{username}_data.json"
     with open(filename, "w") as file:
          json.dump(status, file)

def load_status():
     try:
          username = st.session_state.username
          filename = f"user_data/{username}_data.json"
          with open(filename, "r") as file:
               status = json.load(file)
               st.session_state.debt = status["debt"]
               st.session_state.prepaid_bottle = status["prepaid_bottle"]
               st.session_state.transactions = status["transactions"]
     except:
          st.session_state.debt = 0
          st.session_state.prepaid_bottle = 0
          st.session_state.transactions = []

def transaction_log(action, old_value, new_value):
     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     st.session_state.transactions.append({"timestamp": timestamp, "action": action, "old_value": old_value, "new_value": new_value})

# Load user data, choose user
user_datas = glob.glob("user_data/*_data.json")
usernames = ["新規登録"]
for user_data in user_datas:
     filename = user_data.split("/")[1]
     username = filename.split("_")[0]
     usernames.append(username)
selected_user = st.selectbox("ユーザーを選んでください", usernames)
if selected_user == "新規登録":
     new_username = st.text_input("ユーザー名を入力してください")
     if new_username:
          st.session_state.username = new_username
     else:
          st.stop()
else:
     st.session_state.username = selected_user

if not os.path.exists("user_data"):
     os.makedirs("user_data")

if not os.path.exists(f"user_data/{st.session_state.username}_data.json"):
     with open(f"user_data/{st.session_state.username}_data.json", "w") as f:
          default_data = {
               "debt": 0,
               "prepaid_bottle": 0,
               "transactions": []
          }
          json.dump(default_data, f)

if 'transactions' not in st.session_state:
     st.session_state.transactions = []
     
load_status()

col1, col2 = st.columns(2)

with col1:
     if 'debt' not in st.session_state:
          st.session_state.debt = 0

     if st.button("一本前借りする"):
          old_value = st.session_state.debt
          st.session_state.debt += 1
          new_value = st.session_state.debt
          transaction_log("debt_increase", old_value, new_value)
          save_status()

     if st.button("前借本数ー1"):
          old_value = st.session_state.debt
          st.session_state.debt -= 1
          if st.session_state.debt < 0:
               st.session_state.debt = 0
          new_value = st.session_state.debt
          transaction_log("debt_decrease", old_value, new_value)
          save_status()

     if st.button("前借りをチャラにする"):
          old_value = st.session_state.debt
          st.session_state.debt = 0
          new_value = st.session_state.debt
          transaction_log("debt_zero", old_value, new_value)
          save_status()

     if 'prepaid_bottle' not in st.session_state:
          st.session_state.prepaid_bottle = 0

     if st.button("一本前払いする"):
          old_value = st.session_state.prepaid_bottle
          st.session_state.prepaid_bottle += 1
          new_value = st.session_state.prepaid_bottle
          transaction_log("prepaid_increase", old_value, new_value)
          save_status()

     if st.button("前払本数ー1"):
          old_value = st.session_state.prepaid_bottle
          st.session_state.prepaid_bottle -= 1
          if st.session_state.prepaid_bottle < 0:
               st.session_state.prepaid_bottle = 0
          new_value = st.session_state.prepaid_bottle
          transaction_log("prepaid_decrease", old_value, new_value)
          save_status()

#     if st.button("前払いした分から一本飲む"):
#          old_value = st.session_state.prepaid_bottle
#          st.session_state.prepaid_bottle -= 1
#          if st.session_state.prepaid_bottle < 0:
#               st.session_state.prepaid_bottle = 0
#          new_value = st.session_state.prepaid_bottle
#          transaction_log("prepaid_decrease", old_value, new_value)
#          save_status()

with col2:
     st.write(f"前借りした本数：{st.session_state.debt}")
     st.write(f"前払いした本数：{st.session_state.prepaid_bottle}")

st.subheader("履歴")
transactions_latest_ten = st.session_state.transactions[-10:]
for transaction in transactions_latest_ten:
     col3, col4, col5 = st.columns(3)
     with col3:                      # display timestamp
          st.write(transaction["timestamp"])
     with col4:                      # display action
          if transaction["action"] == "debt_increase":
               st.write("前借り、一本")
          if transaction["action"] == "debt_decrease":
               st.write("前借り、一本消去")
          if transaction["action"] == "debt_zero":
               st.write("前借り、クリア")
          if transaction["action"] == "prepaid_increase":
               st.write("先払い、一本")
          if transaction["action"] == "prepaid_decrease":
               st.write("先払い、一本消去")
     with col5:                      # reflect change
          st.write(f"変更前：{transaction['old_value']}。変更後：{transaction['new_value']}")