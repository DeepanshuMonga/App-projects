from flask import Flask, render_template, redirect, url_for, request, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-secret'

# Use the folder where this script resides as the base folder
DATA_FOLDER = os.path.abspath(os.path.dirname(__file__))

# Relative paths inside the project folder
CRED_FILE = os.path.join(DATA_FOLDER, "Login Credentials.csv")
MASTER_FILE = os.path.join(DATA_FOLDER, "MasterTicket.csv")

def load_credentials():
    return pd.read_csv(CRED_FILE)

def get_user_file(username):
    return os.path.join(DATA_FOLDER, f"{username}.csv")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        df = load_credentials()
        user = df[(df['Name'] == username) & (df['Password'] == password)]
        if not user.empty:
            session["username"] = username
            role = user.iloc[0]['Role']
            session["role"] = role
            if role == "User":
                return redirect(url_for('user_dashboard'))
            elif role == "Support Agent":
                return redirect(url_for('agent_dashboard'))
            elif role == "Admin":
                return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Credentials. Try again.")
    return render_template("login.html")

@app.route("/user", methods=["GET", "POST"])
def user_dashboard():
    if not session.get("role") == "User":
        return redirect(url_for('login'))

    username = session["username"]
    user_file = get_user_file(username)

    # Load user tickets or create empty DataFrame if file doesn't exist
    df = pd.read_csv(user_file) if os.path.exists(user_file) else pd.DataFrame(columns=['Ticket', 'Status'])

    # Convert 'Resolved' tickets to 'Closed' on user dashboard view
    if not df.empty:
        changed = False
        if (df['Status'] == 'Resolved').any():
            df.loc[df['Status'] == 'Resolved', 'Status'] = 'Closed'
            df.to_csv(user_file, index=False)
            changed = True
        if changed:
            df = pd.read_csv(user_file)

    tickets = df.to_dict('records')

    if request.method == "POST":
        ticket = request.form['ticket']
        status = "Open"
        # Append new ticket with headers if file doesn't exist or is empty
        write_header = not os.path.exists(user_file) or os.path.getsize(user_file) == 0
        new_entry = pd.DataFrame([[ticket, status]], columns=['Ticket', 'Status'])
        new_entry.to_csv(user_file, mode='a', header=write_header, index=False)

        # Append to master ticket file similarly
        master_entry = pd.DataFrame([[ticket, status, username]], columns=['Ticket', 'Status', 'Username'])
        master_entry.to_csv(MASTER_FILE, mode='a', header=not os.path.exists(MASTER_FILE), index=False)
        flash("Ticket Added!")
        return redirect(url_for('user_dashboard'))

    return render_template("dashboard_user.html", tickets=tickets, username=username)

@app.route("/agent", methods=["GET", "POST"])
def agent_dashboard():
    if not session.get("role") == "Support Agent":
        return redirect(url_for('login'))

    df = pd.read_csv(MASTER_FILE) if os.path.exists(MASTER_FILE) else pd.DataFrame(columns=['Ticket', 'Status', 'Username'])
    tickets = df.to_dict('records')

    if request.method == "POST":
        idx = int(request.form["ticket_index"])
        if idx < 0 or idx >= len(df):
            flash("Invalid Ticket Index.")
            return redirect(url_for('agent_dashboard'))
        df.at[idx, 'Status'] = 'Resolved'
        ticket_content = df.at[idx, 'Ticket']
        username = df.at[idx, 'Username']
        df.to_csv(MASTER_FILE, index=False)

        user_file = get_user_file(username)
        if os.path.exists(user_file):
            df_user = pd.read_csv(user_file)
            match = df_user["Ticket"] == ticket_content
            df_user.loc[match, "Status"] = "Resolved"
            df_user.to_csv(user_file, index=False)

        flash(f"Ticket {idx} resolved!")
        return redirect(url_for('agent_dashboard'))

    return render_template("dashboard_agent.html", tickets=tickets)

@app.route("/admin")
def admin_dashboard():
    if not session.get("role") == "Admin":
        return redirect(url_for('login'))
    df = load_credentials()
    users = df.to_dict('records')
    return render_template("dashboard_admin.html", users=users)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    # Ensure master file exists before start
    if not os.path.exists(MASTER_FILE):
        pd.DataFrame(columns=['Ticket', 'Status', 'Username']).to_csv(MASTER_FILE, index=False)
    app.run(debug=True)
