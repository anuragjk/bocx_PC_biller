#!/usr/bin/python

from Adafruit_Thermal import *

'''
d_billEntry = {
        'shopName':'Name of Shop',
        'items':[
                    {'itemName':'item 1',       'qty':5,    'rate':10},
        ],
        'msg':'Thank you for shopping with us',
}
'''

def main():
    tp = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
    d_billEntry = bbGetData()
    if(d_billEntry == False):
        return
    bbPrintBill(tp, d_billEntry)

def bbGetData():
    itemList = []

    shopName = input('Name of Shop: ')
    if(bbValidate(shopName)!=0):
        bbError()
        return False

    shopAdr = input('Address of Shop: ')
    if(bbValidate(shopAdr)!=0):
        bbError()
        return False

    opt = input('Do you want to continue billing (y/n):')
    if(opt.lower() == 'n'):
        return False
    num = 1
    while True:
        itemName = input('Item(%d): '%(num))
        qty = input('Quantity(%d): '%(num))
        qty = int(qty)
        rate = input('Rate(%d): '%(num))
        rate = float(rate)
        itemList.append({'itemName':itemName,       'qty':qty,    'rate':rate})

        opt = input('Do you want to enter another item (y/n):')
        if(opt.lower() == 'n'):
            break
        num+=1

    opt = input('Do you want to enter a message\n(y)es/(n)o/(d)fault\n ')
    if(opt.lower() == 'y'):
        shopMsg = input('Enter a message(32 char): ')
        if(bbValidate(shopName)!=0):
            bbError()
            return False
    elif(opt.lower() == 'd'):
        shopMsg = "Thank you for shopping with us"
    elif(opt.lower() == 'n'):
        shopMsg = ""

    return {
        'shopName':shopName,
        'shopAdr':shopAdr,
        'items':itemList,
        'msg':shopMsg,
    }
    


def bbValidate(data, max_len=32, min_len=1,vType=str):
    if(len(data)>max_len):
        return -1

    if(len(data)<min_len):
        return -1

    if(vType!=type(data)):
        return -1

    return 0

def bbError(err = ''):
    print('[Error]: '+str(err))

def bbCustomFormatter(entry):
    output = "-------------------------------"
    output = ' '+entry['itemName'] #1
    output += ' '*(14-len(output))

    s_qty = str(entry['qty'])
    output += ' '*(3-len(s_qty))+s_qty #14
    output += ' '*(18-len(output))

    s_rate = "%.2f"%(entry['rate'])
    output += ' '*(6-len(s_rate))+s_rate #18
    output += ' '*(25-len(output))

    s_total = "%.2f"%(float(entry['qty'])*entry['rate'])
    output += ' '*(6-len(s_total))+s_total
#    output +=  # 25

    return output

def bbPrintBillDbg(printer, d_billEntry):
    print('<JC>')
    print('<U>',end='')
    print('<H1>',end='')
    print(d_billEntry['shopName'],end='')
    print('</H1>',end='')
    print('</U>')
    print('<JL>')

    print("-------------------------------")
    print(" Item       Qty   Rate   Price ")
    print("-------------------------------")

    total = 0
    for item in d_billEntry['items']:
        print(bbCustomFormatter(item))
        total += (item['qty']*item['rate'])
    
    print("-------------------------------")
    print(" Total:                  %s"%(s_total))
    print("-------------------------------")
    print(d_billEntry['msg'])

    print(">")
    print(">")


def bbPrintBill(printer, d_billEntry):
    printer.justify('C')
    printer.setSize('L')
    printer.println(d_billEntry['shopName'])
    printer.setSize('S')
    printer.println(d_billEntry['shopAdr'])
    printer.justify('L')

    printer.println("-------------------------------")
    printer.println(" Item         Qty Rate   Price ")
    printer.println("-------------------------------")

    total = 0
    for item in d_billEntry['items']:
        printer.println(bbCustomFormatter(item))
        total += (float(item['qty'])*float(item['rate']))
    s_total = "%.2f"%(total)
    s_total = ' '*(6-len(s_total))+s_total

    printer.println("-------------------------------")
    printer.println(" Total:                  %.2f"%(total))
    printer.println("-------------------------------")

    printer.justify('C')
    printer.println(d_billEntry['msg'])
    printer.justify('L')

    printer.feed(3)

    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults

if __name__ == '__main__':
    main()
