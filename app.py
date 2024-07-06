from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    quantity = None
    directions = None
    days_supply = None
    if request.method == 'POST':
        try:
            quantity = float(request.form['quantity'])
            days_supply = quantity
            original_sig = request.form['directions']
            sig_codes = capitalize(original_sig.split(","))
            print(sig_codes)
            script_info = get_directions(sig_codes, days_supply)
            directions = script_info[0]
            days_supply = int(script_info[1])
            quantity = int(quantity)
        except (ValueError, ZeroDivisionError):
            days_supply = "Invalid input. Please check the values entered."
    return render_template('index.html', quantity=quantity, directions=directions, days_supply=days_supply)


def get_directions(sig_list, days_supply):
  directions = ""
  for sig in sig_list:
    if sig_exists(remove_spaces(sig)):
      sig = remove_spaces(sig)
      key = sigs_db.get(sig)
      if key:
        directions += str(key[0])
        days_supply = days_supply / key[1]
    elif sig:
      if sig[0] == " ":
        sig = sig[1:]
      if sig[-1] != " ":
        sig = sig + " "
      directions += sig
  script_info = [directions, days_supply]
  return script_info


def sig_exists(sig):
  return any(sig == key for key in sigs_db)


def remove_spaces(sig):
  return sig.replace(" ", "")


def capitalize(lower_list):
  capitalized_list = [word.upper() for word in lower_list]
  return capitalized_list



sigs_db = {
  "1T": ["TAKE ONE TABLET ", 1],
  "1C": ["TAKE ONE CAPSULE ", 1],
  "2T": ["TAKE TWO TABLETS ", 2],
  "2C": ["TAKE TWO CAPSULES ", 2],
  "3T": ["TAKE THREE TABLETS ", 3],
  "3C": ["TAKE THREE CAPSULES ", 3],
  "PO": ["BY MOUTH ", 1],
  "1D": ["INSTILL 1 DROP ", 1/20],
  "2D": ["INSTILL 2 DROPS ", 2/20],
  "3D": ["INSTILL 3 DROPS ", 3/20],
  "4D": ["INSTILL 4 DROPS ", 4/20],
  "QD": ["ONCE DAILY ", 1],
  "BID": ["TWICE A DAY ", 2],
  "TID": ["THREE TIMES DAILY ", 3],
  "QID": ["FOUR TIMES DAILY ", 4],
  "QAM": ["EVERY MORNING ", 1],
  "QPM": ["EVERY EVENING ", 1],
  "QW": ["EVERY WEEK ", 1/7],
  "BIW": ["TWICE WEEKLY ", 2/7],
  "TIW": ["THREE TIMES WEKLY ", 3/7],
  "OD": ["INTO THE RIGHT EYE ", 1],
  "OS": ["INTO THE LEFT EYE ", 1],
  "OU": ["INTO BOTH EYES ", 2],
  "AD": ["INTO THE RIGHT EAR ", 1],
  "AS": ["INTO THE LEFT EAR ", 1],
  "AU": ["INTO BOTH EARS ", 2],
  "PRN": ["AS NEEDED ", 1],
  "QHS": ["AT BEDTIME ", 1],
  "WF": ["WITH FOOD ", 1]
}


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
