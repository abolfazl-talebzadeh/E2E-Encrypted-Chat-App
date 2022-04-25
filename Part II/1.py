from flask import Flask, render_template,request
from flask_socketio import SocketIO, send
import sys,requests, DH, SDES

# defining required vars
n=90
enc_session={"status":False,"p":0,'z':[],"g":0,"a":0,"y":0,"k":0,"key_dec":0,"key_bin":"","p_q":0}
home={"name":"","port":False}
target={"name":"","port":False}
sendingMessage=""
receivingMessage=""

# defining flask instance
app=Flask(__name__)
socketio = SocketIO(app,  cors_allowed_origins="*") #defining socketIO instance and wrapping it aroun flask app

#index view
@app.route('/')
def index():
    return render_template('index.html')

#register view: registering the user at the first stage
@app.route('/register', methods=['POST'])
def register():
    global home
    home['name']=request.form.get('name')
    home['port']=request.environ['SERVER_PORT']
    return render_template("apply.html", name=home['name'], port=home['port'])# loading search page


# searching view
@app.route('/search', methods=['POST'])
def search():
    global home
    global target
    global enc_session
    target['port']=request.form.get('port')
    if not enc_session['status']:
        key=DH.DH(n) #defining Hiffie Hellman class 
        key.g_calculator() #calling "g" calculation method
        key.secret_number_generattor() #calling private key calculation method
        #assigning the calculated parameters to a gloabal dectionary
        enc_session['p']=str(key.p)
        enc_session['g']=str(key.g)
        enc_session['a']=str(key.a)
        enc_session['y']=str(key.ya)
        enc_session['p_q']=str(key.q_times_p)
        # building the payload to be sent to the other party
        payload={'type':'auth','name':home['name'],'p':enc_session['p'],'g':enc_session['g'],
        'y':enc_session['y'],'p_q':enc_session['p_q']}
        r=requests.get(f'http://127.0.0.1:{target["port"]}/connection',params=payload) # sending the data to the other server
        res_json=r.json() #openeing server response in the form of json
        key.yb=res_json['yb'] #fetching the target server's public key from the response
        target['name']=res_json['name'] #fetching the target server's name from the response
        key.k_generator() #calling key calculation method
        key.bss() #calling B.B.S parameters calculation method
        #assigning the calculated parameters to a gloabal dectionary
        enc_session['k']=str(key.k)
        enc_session['key_dec']=str(key.f_k_dec)
        enc_session['key_bin']=key.f_k_bin
        enc_session['status']=True
    else:
        # building the payload to be sent to the other party in the case of receiving an agreement message  
        payload={'type':'cr','port':home["port"]}
        r=requests.get(f'http://127.0.0.1:{target["port"]}/connection',params=payload)
        stringifiesJson=r.text
        target['name']=stringifiesJson
    return render_template('chatbox.html', 
        name=home['name'],targetUser=target['name'],targetPort=target['port']) #loading chatbox.html page

#connection view
@app.route('/connection', methods=['GET'])
def connection():
    global home
    global enc_session
    global target
    mes_type=request.args.get('type') #receiveing the type of the received message
    if mes_type=='cr': #knowing if the type is "connection request"
        return home['name']
    elif mes_type=='auth':
        #the same happening on search view but for the receiver part
        key=DH.DH(n)
        enc_session['status']=True
        target['name']=request.args.get('name')
        key.p=int(request.args.get('p'))
        key.g=int(request.args.get('g'))
        key.secret_number_generattor()
        key.yb=int(request.args.get('y'))
        key.q_times_p=int(request.args.get('p_q'))
        key.k_generator()
        key.bss()
        enc_session['k']=str(key.k)
        enc_session['p']=str(key.p)
        enc_session['g']=str(key.g)
        enc_session['a']=str(key.a)
        enc_session['y']=str(key.ya)
        enc_session['key_dec']=str(key.f_k_dec)
        enc_session['key_bin']=key.f_k_bin
        enc_session['p_q']=str(key.q_times_p)
        return {'yb':key.ya,'name':home['name']}
    return home['name']


# message receiving view
@app.route('/receive', methods=['POST'])
def receive():
    sdes=SDES.SDES()
    dec_mess=""
    global home
    global target
    type=request.form.get("type") # getting the type of the message
    if type=='msg':
        #if the type is a message then do the decoding
        bin_split_msg=bin_spliter(request.form.get('message'),8)
        for i in bin_split_msg:
            dec_mess+=sdes.sdes_decoder(i,enc_session['key_bin'])
        str_msg=bin_str(dec_mess)
        socketio.send(target["name"]+": "+str_msg+"\n")
        print("received: ", request.form.get('message'))
    elif type=='connection':
        #if the type is connection then save the target port 
        target['port']=request.form.get('port')
    return "received"


# socketIO receiving message event
@socketio.on('message')
def handle_message(msg):
    enc_mess=""
    global home
    global target
    global sendingMessage
    sdes=SDES.SDES()
    #if the type of the received message is a connection then save the home port and send the success log
    if msg['type']=='connection':
        home["port"]=msg['port']
        send("you can now chat!"+'\n')
    elif msg['type']=='msg':
        #if the type of the received message is a message then open the body and do the encryption and send it to the other server
        bin_msg=str_bin(msg['body'])
        bin_split_msg=bin_spliter(bin_msg,8)
        for i in bin_split_msg:
            enc_mess+=sdes.sdes_encoder(i,enc_session['key_bin'])
        print("Encrypted Message: ", enc_mess)
        payload={'type':'msg','message':enc_mess,'port':home["port"]}
        r=requests.post(f'http://127.0.0.1:{target["port"]}/receive',data=payload)
        send(home["name"]+": " +msg['body']+"\n")


############## string to binary<takes a string, returns a string of zeros and ones>
def str_bin(t):
    res=[] #for keeping the result
    f_res=""
    t_list=list(t) #converting the text to a list
    for j in t_list:
        #doing all the steps for every character of the text which is now in the form of a list
        t_ord=ord(j) #calculating the order of each char
        bi=["0","0","0","0","0","0","0","0"] #intiating the bits list
        for i in range(7,-1,-1):
            #doing the math for getting the bits corresponding the ascii code of the char
            if t_ord>=(2**i):
                t_ord= t_ord % (2**i)
                bi[i]="1"
            else:
                bi[i]="0"
        result=""
        bi=reversed(bi)
        for k in bi:
            #building the result
            result+=k
        res.append(result)
    #converting the list to string
    for k in res:
        f_res+=k
    return f_res

############## string to binary<takes a string of zeros and ones, returns a string>
def bin_str(b):
    s_res=""
    # doing the loop for 8 times
    for i in range(0,len(b),8):
        # cutting an eught-bit chunk of the sentence
        t=b[i:i+8]
        res=0
        # converting the segment to char
        for i in range(7,-1,-1):
            res+=int(t[7-i])*(2**i)
        #adding the char to the final result
        s_res+=chr(res)
    return s_res

############### receives an string of zeros and devides it into "n" substrings

def bin_spliter(s,n):
    b_l=[]
    #doing the loop for all the characters in the binary string
    for i in range(0,len(s),n):
        #spliting a piece with length of eight
        t=s[i:i+n]
        #adding it to the list
        b_l.append(t)
    return b_l  


###############  main body ###############
if __name__=="__main__":
    global port
    # if the port is not entered as an argument in the cmd after the name of the server it trys to receive the port manually from the user
    if len(sys.argv)<2:
        home['port']=input("enter port:")
    else:
        ## if the port is entered as an argument in the cms after the name of the server it sets the port to the gloabl port variable 
        home['port']=sys.argv[1]
    # building the flask app and wrapping it around the socket IO using the received port number
    socketio.run(app,host='127.0.0.1', port=home['port'])  
