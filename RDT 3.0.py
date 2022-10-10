"""
Sender-side simulation of RDT 3.0;

Input packets are formatted
[type, seq_num, message]
0 message with seq_num to be sent;
1 ACK received, ACKing seq_num;
2 timeout event - resend last packet; 

Output packets are formatted
[status, seq_num]
-1 unexpected packet, -1 as seq_num;
0 message sent successfully - seq_num is the seq # of the message;
1 ACK processed - seq_num is the ACk seq_num;
2 re-sending finished - seq_num is the seq_num of the re-sent message;

Four states as described in the FSM
0 - wait for data 0;
1 - wait for ack 0;
2 - wait for data 1;
3 - wait for ack 1;

"""

def rdt_sender(event, state=0):
    
    #Defines variables to use.
    event_type = None
    seq_num = None
    data = None
    
    
    #Iterates through events and defines variables accordingly.
    for item in event:
        if event_type is None:
            event_type = event[0]
        elif seq_num is None:
            seq_num = event[1]
        elif data is None:
            data = event[2]
    
    #If we're at state 0
    if state == 0:
        if seq_num == 0:
            if event_type == 0:
                return (1, [0, seq_num])
            elif event_type == 1:
                return (0, [-1, -1])
            elif event_type == 2:
                return (0, [0, seq_num])
        if seq_num == 1:
            return (1, [1, 1])
        else:
            return (1, [2, seq_num])
    
    #If we're at state 1
    if state == 1:
        if seq_num == 0:
            if event_type == 0:
                return (1, [-1, -1])
            elif event_type == 1:
                return (2, [1, 0])
            elif event_type == 2:
                return (1, [2, seq_num])
        else:
            return (state, [-1, -1])
        
    #If we're at state 2:
    if state == 2:
        if seq_num == 1:
            if event_type == 0:
                return (3, [0, 1])
            if event_type == 1:
                return (2, [-1, -1])
            if event_type == 2:
                return (2, [2, seq_num])
        else:
            return (state, [-1, -1])
    
    #If we're at state 3
    if state == 3:
        if event_type == 2:
            return (0, [2, 1])
        elif seq_num == 1:
            if event_type == 0:
                return (3, [-1, -1])
            if event_type == 1:
                return (0, [1, 1])
            
        else:
            return (0, [-1, -1])
            
        
    
    
    





                

#Do not modify the following lines    
def sender_test(event_list):    
    state = 0
    action_list = []    
    
    for event in event_list:        
        state, action = rdt_sender(event,state)
        action_list.append(action)    
    print(f'{action_list}')


#sender_test([[0, 0, 1], [2, 0, 1]])
#sender_test([[0, 0, 1], [1, 0, 1], [0, 1, 3], [2],[1,1,3]])
#sender_test([[0, 0, 1], [2, 0, 1]])
#sender_test([[0, 0, 1], [0, 1, 2], [0, 0, 3], [0, 1, 4], [0, 0, 5]])
#sender_test([[0, 0, 1], [1, 0, 1], [0, 1, 3], [1, 1, 3]])
#sender_test([[0, 0, 1], [1, 0], [0, 1, 3], [1, 1]])
#sender_test([[0, 0, 1], [1, 1, 1], [0, 1, 3], [1, 1, 3]])
#sender_test([[0, 0, 1], [1, 0, 1], [0, 1, 3], [2], [1, 1, 3], [0, 1, 4]])


"""
Receiver-side simulation of RDT 3.0

"""


def rdt_receiver(packet):
    if packet[0] not in [0, 1]:
        return [-1, -1]
    else:
        return [0, packet[0]]
    
       




#Do NOT modify the following lines    
def receiver_test(event_list):    
    action_list = []    
    
    for event in event_list:        
        action = rdt_receiver(event)
        action_list.append(action)    
        
    print(f'{action_list}')  
    
#receiver_test([[0, 1]])

"""
Sender-side simulation of GBN;

An event is formatted as
[type, seq_num, data]
0 data to send; no check on seq_num and data;
1 ACK received; acking seq_num;
2 timeout event; resend all outgoing unAck'ed events; no check on seq_num and data;

Output of function gbn_sender() is formatted as
[status, base, next_seq]
-1 unexpected event/window full
0 data sent successfully
1 ACK processed; 
2 resending finished; 

N - the window size
base - seq# of lower winder boundary (base)

"""

N = 4 # window size

def gbn_sender(event, base=0, next_seq=0):  
    """Applies the Go Back N protocol to a list of variables"""
    
    #Initialising variables
    event_type = None
    seq_num = None
    data = None

    for item in event:
        if event_type is None:
            event_type = item
        elif seq_num is None:
            seq_num = item
        else:
            data = item
    #print(event)
    #print(f"event type is {event_type}")
    #print(f"next_seq is {next_seq}")
    #print(range(base, next_seq - 1))
    #print('')
    
    #If event type is a date sending event       
    if event_type == 0:
        #Data has been sent, ready for transmission
        if (next_seq - base) < 4:
            return [0, base, next_seq + 1]
        else:
            return [-1, base, next_seq]
        
    #If event type is an acknowledgement event
    if event_type == 1:
        if seq_num in range(base, next_seq):
            base = seq_num
            return [1, base + 1, next_seq]
        else:
            return [-1, base, next_seq]
        
    #If event type is a timeout
    if event_type == 2:
        return [2, base, next_seq]
        
        
 
                

#Do NOT modify the following code    
def sender_test(event_list):    
    base = 0
    next_seq = 0
    action_list = []    
    
    for event in event_list:        
        action = gbn_sender(event, base, next_seq)
        base = action[1]
        next_seq = action[2]
        action_list.append(action)    
        
    print(f'{action_list}')
    
#sender_test([[2, 0, 0]])
#sender_test([[0, 0, 1]])
#sender_test([[0, 0, 1], [0, 1, 2]])
#sender_test([[0, 0, 1], [0, 1, 2], [0, 2, 3]])
#sender_test([[0, 0, 1], [0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5]])
#sender_test([[0, 0, 1], [0, 1, 1], [1, 1, 3], [0, 1, 4]])
#sender_test([[0, 0, 1], [0, 1, 2], [0, 2, 3],[2]])
#sender_test([[1, 0, 0]])
#sender_test([[0, 0, 1], [0, 1, 1], [1, 1, 3],[1,1,3]])
#sender_test([[0, 0, 1], [0, 1, 1], [1, 2, 3]])
#sender_test([[0, 0, 1], [0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5], [1,2,3],[0,4,5],[0,5,6],[2,0,0],[1,4,5]])

"""
Receiver-side simulation of GBN

Input packets are formatted as
[seq_num, data]

Output packets are formatted as
[status, exp_num]
0 - an ACK is sent;
-1 - unexpected packet received; 

"""

def gbn_receiver(packet, exp_num=1):
    seq_num = packet[0]
    data = packet[1]
    if seq_num == exp_num:
        status = 0
        exp_num += 1
    else:
        status = -1
        
    return [status, exp_num]

    
       
#Do NOT modify the following code    
def receiver_test(packet_list):    
    action_list = []
    exp_num = 1
    
    for packet in packet_list:        
        action = gbn_receiver(packet, exp_num)
        exp_num = action[1]
        action_list.append(action)    
        
    print(f'{action_list}')  

receiver_test([[1,1]])
receiver_test([[1,1],[2,2]])
receiver_test([[1,1],[2,2],[3,3]])
receiver_test([[0,1]])
