from flask import Flask, render_template, redirect, url_for, flash, request
from database import get_connection

app = Flask(__name__)
app.secret_key = "secret_key"

def fetch_all(query, args=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query) if not args else cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route("/")
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM relief_centers")
    centers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM victims")
    victims_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM supplies")
    supplies_count = cursor.fetchone()[0]

    cursor.execute("CALL get_center_utilization()")
    center_util = cursor.fetchall()

    cursor.close(); conn.close()


    low_logs = fetch_all("SELECT supply_id, item_name, center_id, quantity, log_time FROM low_inventory_log ORDER BY log_time DESC LIMIT 5")
    allocation_logs = fetch_all("SELECT region, item_name, quantity_allocated, allocation_time FROM allocation_log ORDER BY allocation_time DESC LIMIT 5")

    return render_template("index.html",
                           centers_count=centers_count,
                           victims_count=victims_count,
                           supplies_count=supplies_count,
                           center_util=center_util,
                           low_logs=low_logs,
                           allocation_logs=allocation_logs)

@app.route("/centers")
def centers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT center_id, center_name, location, capacity FROM relief_centers")
    centers = cursor.fetchall()

    cursor.execute("CALL get_center_utilization()")
    center_util = cursor.fetchall()
    cursor.close(); conn.close()

    return render_template("centers.html", centers=centers, center_util=center_util)

@app.route("/victims")
def victims():

    rows = fetch_all("SELECT region, victim_name, age, incident_type FROM victims ORDER BY region")
    victims_grouped = {}
    for r in rows:
        region, name, age, incident = r
        victims_grouped.setdefault(region, []).append((name, age, incident))
    return render_template("victims.html", victims_grouped=victims_grouped)

@app.route("/supplies")
def supplies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT supply_id, item_name, quantity, center_id FROM supplies ORDER BY center_id")
    supplies = cursor.fetchall()
    cursor.execute("CALL check_inventory_status()")
    inventory_status = cursor.fetchall()
    cursor.close(); conn.close()

    supplies_grouped = {}
    for s in supplies:
        sid, item, qty, cid = s
        supplies_grouped.setdefault(cid, []).append((sid, item, qty))
    return render_template("supplies.html", supplies_grouped=supplies_grouped, inventory_status=inventory_status)

@app.route("/low_inventory")
def low_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, center_id, quantity, status, checked_at FROM inventory_low")
    low_items = cursor.fetchall()
    conn.close()
    return render_template("low_inventory.html", low_items=low_items)

@app.route("/demands")
def demands():
    rows = fetch_all("SELECT region, food_required, water_required, medical_kits_required FROM demands")
    return render_template("demands.html", demands=rows)

@app.route("/donations")
def donations():
    rows = fetch_all("SELECT donor_name, item_donated, amount, donation_date FROM donations ORDER BY donation_date DESC")
    return render_template("donations.html", donations=rows)

@app.route("/feedback")
def feedback():
    rows = fetch_all("SELECT person_name, message, date_submitted FROM feedback ORDER BY date_submitted DESC")
    return render_template("feedback.html", feedback_list=rows)

@app.route("/allocation_logs")
def allocation_logs():
    rows = fetch_all("SELECT region, item_name, quantity_allocated, allocation_time FROM allocation_log ORDER BY allocation_time DESC")
    return render_template("allocation_logs.html", allocation_logs=rows)

@app.route("/disaster_reports")
def disaster_reports():
    rows = fetch_all("SELECT region, victims, total_demand, supplies_available, report_time FROM disaster_report_log ORDER BY report_time DESC")
    return render_template("disaster_reports.html", report_logs=rows)

@app.route("/run_allocate", methods=["POST"])
def run_allocate():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("CALL allocate_resources_weighted()")
    conn.commit(); cursor.close(); conn.close()
    flash("Weighted allocation calculated and logged.")
    return redirect(url_for("dashboard"))

@app.route("/run_distribute", methods=["POST"])
def run_distribute():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("CALL distribute_supplies()")
    conn.commit(); cursor.close(); conn.close()
    flash("Supplies distributed and logged.")
    return redirect(url_for("dashboard"))

@app.route("/run_report", methods=["POST"])
def run_report():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("CALL generate_disaster_report()")
    conn.commit(); cursor.close(); conn.close()
    flash("Disaster report generated.")
    return redirect(url_for("dashboard"))

@app.route("/run_check_inventory", methods=["POST"])
def run_check_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("check_low_inventory")
    conn.commit()
    conn.close()
    return redirect(url_for("low_inventory"))

if __name__ == "__main__":
    app.run(debug=True)
