import os,secrets,datetime as dt,time,requests as r,stripe
from flask import Flask,render_template_string as rt,request as req,redirect as red,url_for as url,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash as gh,check_password_hash as ch

app=Flask(__name__)
app.config.update(SECRET_KEY=os.environ.get('sk_test_51Tke3WRsVgVw9kTXB7nWOrvb1jGUnCuTAqwgcX5OA7r7hxVh534pcyg5Y0D989GwT4CQmwsfN9SezJyb8gEdjXDF00OEi2JoDS',secrets.token_hex(16)),SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',SQLALCHEMY_TRACK_MODIFICATIONS=False)
db=SQLAlchemy(app);lm=LoginManager(app);lm.login_view='login'

E_URL,S_SK,S_WH="https://onrender.com",os.environ.get("stripe.api_key="sk_test_51Tke3WRsVgVw9kTXB7nWOrvb1jGUnCuTAqwgcX5OA7r7hxVh534pcyg5Y0D989GwT4CQmwsfN9SezJyb8gEdjXDF00OEi2JoDS","sk_test_placeholder"),os.environ.get("STRIPE_WEBHOOK_SECRET","")
stripe.api_key=S_SK

H="""<!DOCTYPE html><html><head><meta charset='UTF-8'><title>CodeX AI Pro</title><style>:root{--bg:#06070a;--panel:#0d0f14;--border:rgba(255,255,255,0.05);--neon:#00f2fe;--p:#ff007a;--t:#e2e8f0;}body{font-family:monospace;background:var(--bg);color:var(--t);margin:0;height:100vh;display:flex;flex-direction:column;overflow:hidden;}header{background:var(--panel);border-bottom:1px solid var(--border);padding:10px 20px;display:flex;justify-content:space-between;align-items:center;}.b{font-weight:700;font-size:16px;background:linear-gradient(135deg,var(--neon),var(--p));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}.w{display:flex;flex:1;height:calc(100vh - 55px);}.l,.r{flex:1;display:flex;flex-direction:column;padding:15px;box-sizing:border-box;}.l{border-right:1px solid var(--border);}textarea{flex:1;padding:15px;background:#090a0f;color:#34d399;border:1px solid var(--border);border-radius:6px;font-family:inherit;font-size:14px;resize:none;outline:none;line-height:1.5;}textarea:focus{border-color:var(--neon);box-shadow:0 0 10px rgba(0,242,254,0.15);}.bar{margin-top:10px;display:flex;gap:10px;}button{flex:1;padding:12px;background:linear-gradient(135deg,var(--neon),#7928ca);border:none;font-weight:700;border-radius:6px;cursor:pointer;font-size:14px;}pre{flex:1;margin:0;background:#030406;padding:15px;color:#a7f3d0;overflow:auto;border-radius:6px;white-space:pre-wrap;border:1px solid var(--border);line-height:1.5;}.pay{padding:5px 10px;font-size:11px;border-radius:4px;cursor:pointer;background:transparent;border:1px solid var(--neon);color:var(--neon);font-weight:normal;}.lo{color:#ef4444;text-decoration:none;font-size:12px;padding:4px 8px;background:rgba(239,68,68,0.05);border-radius:4px;border:1px solid rgba(239,68,68,0.15);}</style></head><body><header><div class='b'>CodeX Quantum AI Terminal 🌌</div><div style='display:flex;align-items:center;gap:12px;'><div style='font-size:12px;'>User: <b>{{current_user.username}}</b> | Tier: <span style='color:var(--neon);font-weight:bold;'>{%if current_user.is_premium_plus%}👑 Plus{%elif current_user.is_premium%}💎 Prem{%else%}<span id='tc'>{{current_user.tokens}}</span>/15 Free Tokens{%endif%}</span></div><form action='/pay/premium' method='POST'><button type='submit' class='pay'>Upgrade Premium</button></form><form action='/pay/plus' method='POST'><button type='submit' class='pay' style='border-color:var(--p);color:var(--p);'>Upgrade Plus 👑</button></form><a href='/logout' class='lo'>Exit Portal</a></div></header><div class='w'><div class='l'><textarea id='p' placeholder='# Enter computational prompts...'></textarea><div class='bar'><button onclick='g()'>Execute Runtime Array ✨</button></div></div><div class='r'><pre id='o'># CodeX Engine Standby... Awaiting core instruction sequences.</pre></div></div><script>function g(){const p=document.getElementById('p').value;if(!p.trim())return;const o=document.getElementById('o');o.innerText="# Initiating neural data pipelines...\\n# Fetching cluster compilation paths... ";fetch('/gen',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({p:p})}).then(r=>r.json()).then(d=>{if(d.c){o.innerText=d.c;const s=document.getElementById('tc');if(s&&d.r!==undefined)s.innerText=d.r;}else{o.innerText=d.message;}}).catch(()=>{o.innerText='# Compilation Timeout. Server cluster refreshing. Please click execute button again.';});}</script></body></html>"""
P="""<!DOCTYPE html><html><head><title>CodeX Gateway</title><meta charset='UTF-8'><style>body{font-family:sans-serif;background:#050609;color:#fff;max-width:350px;margin:150px auto;padding:15px;}.c{background:#0d0e15;padding:30px;border-radius:10px;border:1px solid rgba(255,255,255,0.05);box-shadow:0 15px 30px rgba(0,0,0,0.5);}h2{text-align:center;background:linear-gradient(135deg,#00f2fe,#ff007a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-top:0;}input{width:100%;padding:12px;margin:8px 0;background:#07080d;color:#fff;border:1px solid rgba(255,255,255,0.08);border-radius:6px;box-sizing:border-box;outline:none;}input:focus{border-color:#00f2fe;}button{width:100%;padding:12px;background:linear-gradient(135deg,#00f2fe,#7928ca);border:none;font-weight:bold;border-radius:6px;cursor:pointer;margin-top:10px;}a{color:#00f2fe;text-decoration:none;display:block;text-align:center;margin-top:15px;font-size:13px;}</style></head><body><div class='c'><h2>CodeX Gate {{t}}</h2>{%with m=get_flashed_messages()%}{%if m%}{%for msg in m%}<p style='color:#ff007a;text-align:center;font-size:12px;margin:0 0 10px 0;'>{{msg}}</p>{%endfor%}{%endif%}{%endwith%}<form method='POST'><input type='text' name='u' placeholder='Account Identifier' required><input type='password' name='p' placeholder='Secret Access Key' required><button type='submit'>Authenticate Identity</button></form>{%if t=='Login'%}<a href='/register'>Register New Credentials</a>{%else%}<a href='/login'>Return to Gate Login</a>{%endif%}</div></body></html>"""

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True);username=db.Column(db.String(150),unique=True,nullable=False);password=db.Column(db.String(256),nullable=False)
    tokens=db.Column(db.Integer,default=15);is_premium=db.Column(db.Boolean,default=False);is_premium_plus=db.Column(db.Boolean,default=False);last_reset=db.Column(db.DateTime,default=dt.datetime.utcnow)

@lm.user_loader
def load_user(uid):return db.session.get(User,int(uid))

def v_tok(u):
    if u.is_premium or u.is_premium_plus:return
    now=dt.datetime.utcnow()
    if u.last_reset is None:u.last_reset=now;db.session.commit()
    if (now-u.last_reset).total_seconds()/3600.0>=24.0:u.tokens=15;u.last_reset=now;db.session.commit()

@app.route('/')
@login_required
def dash():v_tok(current_user);return rt(H)

@app.route('/register',methods=['GET','POST'])
def register():
    if req.method=='POST':
        u,p=req.form.get('u'),req.form.get('p')
        if User.query.filter_by(username=u).first():flash('Identity path occupied.');return red(url('register'))
        n=User(username=u,password=gh(p,method='scrypt'));db.session.add(n);db.session.commit();login_user(n);return red(url('dash'))
    return rt(P,t="Register")

@app.route('/login',methods=['GET','POST'])
def login():
    if req.method=='POST':
        u=User.query.filter_by(username=req.form.get('u')).first()
        if u and ch(u.password,req.form.get('p')):login_user(u);return red(url('dash'))
        flash('Invalid credentials.')
    return rt(P,t="Login")

@app.route('/logout')
@login_required
def logout():logout_user();return red(url('login'))

@app.route('/gen',methods=['POST'])
@login_required
def gen_code():
    v_tok(current_user)
    if current_user.tokens<=0 and not current_user.is_premium and not current_user.is_premium_plus:return jsonify({'message':'Compute tokens exhausted.'}),402
    p,cc=req.json.get('p','') if req.json else '',None
    for _ in range(2):
        try:
            res=r.post(E_URL+"/compute",json={'prompt':p},timeout=15)
            if res.status_code==200:
                cc=res.json().get('code')
                if cc:break
        except:time.sleep(2)
    if not cc:cc="# CodeX Core Engine waking up from deep server hibernation.\\n# Please re-trigger the verification run execution button in 10 seconds."
    if not current_user.is_premium and not current_user.is_premium_plus and "waking up" not in cc:
        current_user.tokens-=1;db.session.commit()
    return jsonify({'c':cc,'r':current_user.tokens})

def create_checkout(name,amt,tier):
    s=stripe.checkout.Session.create(line_items=[{ 'price_data':{ 'currency':'usd','product_data':{ 'name':name},'unit_amount':amt},'quantity':1}],mode='payment',success_url=req.host_url,cancel_url=req.host_url,customer_email=current_user.username,metadata={ 'tier':tier})
    return red(s.url,code=303)

@app.route('/pay/premium',methods=['POST'])
@login_required
def pay_premium():return create_checkout('Premium Access',2500,'premium')

@app.route('/pay/plus',methods=['POST'])
@login_required
def pay_plus():return create_checkout('Premium Plus Access',4900,'plus')

@app.route('/stripe-webhook',methods=['POST'])
def stripe_webhook():
    try:
        e=stripe.Webhook.construct_event(req.data,req.headers.get('STRIPE_SIGNATURE'),S_WH)
        if e['type']=='checkout.session.completed':
            s=e['data']['object'];u=User.query.filter_by(username=s.get('customer_email')).first()
            if u:
                if s.get('metadata',{}).get('tier')=='plus':u.is_premium_plus=True
                else:u.is_premium=True
                db.session.commit()
    except:return 'Error',400
    return '',200

@app.errorhandler(Exception)
def handle_exception(e):
    return (jsonify({'message':'Neural cluster runtime exception. Retry array block.'}),500) if req.path.startswith('/gen') else ("CodeX Gateway Structural Reset. Please return to /login",500)

if __name__=='__main__':
    with app.app_context():db.create_all()
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))

