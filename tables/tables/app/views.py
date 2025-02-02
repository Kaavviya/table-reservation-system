from app import app

from flask import request,session,render_template, make_response,redirect,url_for

from app.patterns import table,client_details,invoker,Reserved,Availale,RserervedCancelledNotification,CancelReservationCommand,ReserveSeatCommand,Payment,ManagerSingleton

import json


def deserialise(file_name):
    with open(file_name,'r') as f:
        return json.load(f)

@app.route('/')
def index():
    reserved_seat = deserialise('reservedSeat.json')
    return make_response(render_template('public/home.html',reserved_seats = reserved_seat))

@app.route('/process_form', methods=['POST'])
def process_form():
    table.current_state = Availale()
    input_seat = int(request.form['seat_number'])
    available_seats = deserialise('availableSeat.json')
    if(len(available_seats)<input_seat):
        return render_template('public/message.html',message='Sorry not enough seats left')
    elif(input_seat<0):
        return render_template('public/message.html',message='Enter a valid input')
    input_name = request.form['name']
    input_email = request.form['email']

    input_mobileno = request.form['mobile']
    details = (input_name, input_email, input_mobileno)

    reserve_command = ReserveSeatCommand(table, details, input_seat)
    invoker.execute_command(reserve_command)
    return redirect(url_for('check_reservation'))


@app.route('/check_reservation')
def check_reservation():
    if client_details:
        last_item = list(client_details.items())[-1]
        bill = len(last_item[1]) * 100
        return render_template('public/check_reservation.html',reservation = last_item,bill = bill)
    return render_template('public/check_reservation.html',reservation = None,bill = 0)



@app.route('/cancel_reservation',methods = ['POST'])
def cancel_reservation():
    table.current_state = Reserved()
    detail = tuple(request.form['reservation_id'].split(','))
    print('after cancel',detail)
    cancel_command = CancelReservationCommand(table, detail)
    invoker.execute_command(cancel_command)
    notification = RserervedCancelledNotification()
    table.observer.notify_observers(notification.style_notification(f"{detail[0].upper()} your resrvation has been cancelled"))
    reserved_seat = deserialise('reservedSeat.json')
    return redirect(url_for('index',reserved_seats = reserved_seat))

@app.route('/make_payment',methods=['POST'])
def make_payment():
    bill = request.form['total_bill']
    detail = request.form['detail']
    strategy = request.form['mode']
    payment = Payment(detail,bill,strategy)
    table.observer.notify_observers(payment.push_notification())
    return redirect(url_for('see_notification'))


@app.route('/see_notification')
def see_notification():
    img = None
    notification = table.observer.observers[-1].notification
    if notification and notification[-1][-5:-2] == 'upi':
        img = 'qr.jpeg'
    return render_template('public/check_notification.html', user_notifications=notification, img=img)

@app.route('/manager')
def manager():
    notification = table.observer.observers[0].notification
    return make_response(render_template('public/manager.html',client_details = client_details,manager_notifications=notification))

manager_instance = ManagerSingleton()

@app.route('/update_payment', methods=['POST'])
def update_payment():
    client_detail = tuple(request.form['client_detail'].split(','))
    payment_done = 'payment_done' in request.form
    manager_instance.update_payment(client_detail, payment_done, table)
    return redirect(url_for('manager'))


@app.route('/view_history')
def view_history():
    client_history_data = manager_instance.get_client_history()
    return render_template('public/history.html', client_history=client_history_data)


@app.route('/show_manager_notifications', methods=['POST'])
def show_manager_notifications():
    notification = manager_instance.get_manager_notifications(table)
    return render_template('public/manager.html', manager_notifications=notification, client_details=client_details)