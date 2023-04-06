
import sqlite3, subprocess
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = '88_ormwjyxrilcmmvawjxfayrtiv'

### save the values for mac_address, hostname and location in a temporary file
tmp_file = './.tt'

def run_command(command):
    output = subprocess.check_output(command,shell=True).decode('utf-8')
    return output


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/summary', methods=('GET', 'POST'))
def show_summary():

  ### Werte werden via tmp_file uebergeben
  with open(tmp_file, 'r') as fh:
      string = fh.read()

  mac_address, hostname, location, original_line = string.split('|')

  #flash('Calling sub show_summary() ... ')
  
  if request.method == 'POST':
 
    if check_mac_address(mac_address):

        print(f'Ignoring the mac-address {mac_address} ... ')
        flash(f'A dhcp reservation for this mac-address has already been created, please check the mac-address {mac_address} !')
        return redirect(url_for('create'))

    elif check_hostname(hostname):

        print(f'Ignoring the hostname {hostname} ... ')
        flash(f'A dhcp reservation for this hostname has already been created, please check the hostname {hostname} !')
        return redirect(url_for('create'))

    else:

        ### Save this mac_address to local sql database
        conn = get_db_connection()
        conn.execute('INSERT INTO devices (mac_address, hostname, original_line) VALUES (?, ?, ?)',
                 (mac_address, hostname, original_line))

        conn.commit(); conn.close()

        return redirect(url_for('show_result'))

  else:

    return render_template('summary.html', mac_address=mac_address, hostname=hostname, location=location)



@app.route('/archiv')
def archiv():
    conn = get_db_connection()
    devices = conn.execute('SELECT * FROM devices').fetchall()
    conn.close()

    devices.reverse()
    print(type(devices))
    return render_template('archiv.html', devices=devices)


@app.route('/result', methods=('GET', 'POST'))
def show_result():


    result = ''

    with open(tmp_file, 'r') as fh:
        string = fh.read()
    mac_address, hostname, location, original_line = string.split('|')

    ### jetzt passiert endlich mal was
    try:

        ### python Script aufrufen
        python_script = "C:\\Users\scma_site\zero_touch\create_dhcp_reservation-new.py --debug" \
            + " --location " + location + " --host " + hostname + " --mac-address " + mac_address \
            + ">C:\\temp\out.txt 2>&1 && type C:\\temp\out.txt"

        command = "C:\\Tools\python\python.exe " + python_script; print(command)

        result = run_command(command)

    except:
        flash('big problem :-(')

    return render_template('result.html', command=command, result=result)



def get_db_connection():
    conn = sqlite3.connect('device.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_device(device_id):
    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE id = ?',
                        (device_id,)).fetchone()
    conn.close()
    if device is None: abort(404)

    return device


def check_mac_address(mac_address):

   ### mac_address should not exist in sql database
   conn = get_db_connection()
   result = conn.execute('SELECT * FROM devices WHERE mac_address = ?',
		(mac_address,)).fetchone()
   conn.close()

   return result

def check_hostname(hostname):

   ### hostname should not exist in sql database
   conn = get_db_connection()
   result = conn.execute('SELECT * FROM devices WHERE hostname = ?',
		(hostname,)).fetchone()
   conn.close()

   return result


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':

        mac_address = hostname = ''
        original_line = request.form['content']

        try: 
            mac_address, hostname = original_line.split(';')[0:2]

            mac_address = mac_address.replace(':', "")
            mac_address = mac_address.replace('-', "")
            mac_address = mac_address.lower()
            hostname = hostname.lower()

        except:
            pass

        if not ( mac_address and hostname ):
            flash('Please insert valid data !')
            return render_template('create.html')

        if not len(mac_address) == 12:
            flash(f'The mac_address {mac_address} is invalid !')
            return render_template('create.html')

        else:

            ### get the location from the hostname
            location = hostname[1:5] 

            ### save the values in a temporary file
            string = mac_address + '|' + hostname + '|' + location + '|' + original_line
            with open(tmp_file, 'w') as fh:
                fh.write(string)

            ### Diese Seite zeigt ein Zusammenfassung, was passieren wird
            return redirect(url_for('show_summary'))

    return render_template('create.html')

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=9044, debug=True)
